import os
import re
import json
from datetime import datetime
from typing import Generator, List, Optional
from urllib.parse import urlparse

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from langchain_openai import AzureChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///socialmedia.db")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.4-nano")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "azure").lower()

SUPPORTED_PLATFORMS = {"LinkedIn", "X", "Instagram", "Facebook", "TikTok"}
PLATFORM_MAX_LENGTH = {
    "X": 280,
    "LinkedIn": 3000,
    "Instagram": 2200,
}

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

app = FastAPI(title="Generador de Contenidos IA", version="1.0")


class Base(DeclarativeBase):
    pass


class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    tone: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    hashtags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    variants: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SocialMediaPostSchema(BaseModel):
    id: Optional[int] = None
    platform: str
    title: str
    tone: str
    content: str
    hashtags: Optional[List[str]] = Field(default_factory=list)
    link: Optional[str] = None
    language: Optional[str] = None
    variants: Optional[List[str]] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SocialMediaPostsSchema(BaseModel):
    items: List[SocialMediaPostSchema]

    model_config = ConfigDict(from_attributes=True)


class SocialMediaPostCreateSchema(BaseModel):
    platform: str = Field(..., description="Red social admitida")
    title: str = Field(..., max_length=200)
    tone: str = Field(..., max_length=100)
    content: str = Field(...)
    hashtags: Optional[List[str]] = Field(default_factory=list)
    link: Optional[str] = None
    language: Optional[str] = None
    variants: Optional[List[str]] = Field(default_factory=list)


class SocialMediaPostUpdateSchema(BaseModel):
    platform: Optional[str] = None
    title: Optional[str] = Field(default=None, max_length=200)
    tone: Optional[str] = Field(default=None, max_length=100)
    content: Optional[str] = None
    hashtags: Optional[List[str]] = None
    link: Optional[str] = None
    language: Optional[str] = None
    variants: Optional[List[str]] = None


class GeneratePostRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    platform: str
    tone: str
    language: Optional[str] = None
    variants: Optional[int] = Field(default=1, ge=1, le=5)


class GeneratePostResponse(BaseModel):
    post: SocialMediaPostSchema

    model_config = ConfigDict(from_attributes=True)


def validate_platform(platform: str) -> str:
    if platform not in SUPPORTED_PLATFORMS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Plataforma no admitida: {platform}. Debe ser una de {sorted(SUPPORTED_PLATFORMS)}.",
        )
    return platform


def validate_link(link: Optional[str]) -> Optional[str]:
    if not link:
        return None
    parsed = urlparse(link)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El link debe ser una URL válida con http:// o https://.",
        )
    return link


def normalize_hashtags(hashtags: Optional[List[str]]) -> List[str]:
    if not hashtags:
        return []
    normalized = []
    for tag in hashtags:
        if not tag:
            continue
        cleaned = tag.strip()
        if not cleaned.startswith("#"):
            cleaned = f"#{cleaned}"
        normalized.append(cleaned)
    unique = []
    for tag in normalized:
        if tag.lower() not in {existing.lower() for existing in unique}:
            unique.append(tag)
    if len(unique) > 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Máximo 10 hashtags permitidos.",
        )
    return unique


def validate_content_length(platform: str, content: str) -> None:
    max_length = PLATFORM_MAX_LENGTH.get(platform)
    if max_length and len(content) > max_length:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El contenido para {platform} no puede superar {max_length} caracteres.",
        )


def normalize_variants(variants: Optional[List[str]]) -> List[str]:
    if variants is None:
        return []
    if not 1 <= len(variants) <= 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Se requieren entre 1 y 5 variantes.",
        )
    return [variant.strip() for variant in variants if variant and variant.strip()]


def create_database() -> None:
    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_llm_client():
    if LLM_PROVIDER == "ollama" or (LLM_PROVIDER != "azure" and OLLAMA_URL):
        if not OLLAMA_URL:
            raise RuntimeError("OLLAMA_URL no está configurado para ChatOllama.")
        return ChatOllama(base_url=OLLAMA_URL, model=MODEL_NAME)

    if not all([AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT]):
        raise RuntimeError("Azure OpenAI no está completamente configurado. Verifique las variables de entorno.")

    return AzureChatOpenAI(
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
        openai_api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_key=AZURE_OPENAI_API_KEY,
        model=MODEL_NAME,
    )


def build_generate_prompt(request: GeneratePostRequest) -> str:
    language = request.language or "es"
    return (
        "Genera un post para redes sociales en formato JSON válido. "
        "Devuelve sólo el objeto JSON sin texto adicional. "
        "El post debe incluir platform, title, tone, content, hashtags, link, language y variants. "
        "Asegúrate de que hashtags sea una lista de hasta 10 etiquetas sin duplicados. "
        "Asegúrate de que variants sea una lista de hasta 5 textos. "
        f"Plataforma: {request.platform}. "
        f"Tono: {request.tone}. "
        f"Idioma: {language}. "
        f"Prompt: {request.prompt}. "
        f"Number of variants: {request.variants}."
    )


def parse_post_output(raw_text: str) -> SocialMediaPostSchema:
    try:
        parsed_dict = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError("Respuesta de IA inválida: no es JSON válido.") from exc

    try:
        return SocialMediaPostSchema.model_validate(parsed_dict)
    except ValidationError as exc:
        raise ValueError("Respuesta de IA inválida o no ajustada al esquema esperado.") from exc


@retry(
    retry=retry_if_exception_type(Exception),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)
def generate_post_with_llm(request: GeneratePostRequest) -> SocialMediaPostSchema:
    llm = get_llm_client()

    system_text = (
        "Eres un asistente experto en creación de publicaciones para redes sociales. "
        "Genera siempre JSON válido de acuerdo al esquema Pydantic."
    )
    human_text = build_generate_prompt(request)
    messages = [SystemMessage(content=system_text), HumanMessage(content=human_text)]

    response = llm.invoke(messages)
    raw_output = response.content if hasattr(response, "content") else str(response)
    try:
        return parse_post_output(raw_output)
    except ValueError:
        # En caso de JSON inválido, reintentar
        raise


def build_post_entity(data: SocialMediaPostCreateSchema) -> SocialMediaPost:
    hashtags = normalize_hashtags(data.hashtags)
    validate_platform(data.platform)
    validate_link(data.link)
    validate_content_length(data.platform, data.content)
    variants = normalize_variants(data.variants)
    return SocialMediaPost(
        platform=data.platform,
        title=data.title.strip(),
        tone=data.tone.strip(),
        content=data.content.strip(),
        hashtags=json.dumps(hashtags, ensure_ascii=False) if hashtags else None,
        link=data.link.strip() if data.link else None,
        language=data.language.strip() if data.language else None,
        variants=json.dumps(variants, ensure_ascii=False) if variants else None,
    )


def load_post_entity(post: SocialMediaPost) -> SocialMediaPostSchema:
    return SocialMediaPostSchema(
        id=post.id,
        platform=post.platform,
        title=post.title,
        tone=post.tone,
        content=post.content,
        hashtags=json.loads(post.hashtags) if post.hashtags else [],
        link=post.link,
        language=post.language,
        variants=json.loads(post.variants) if post.variants else [],
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@app.on_event("startup")
def on_startup() -> None:
    create_database()


@app.get("/api/contents", response_model=SocialMediaPostsSchema)
def list_posts(session: Session = Depends(get_session)) -> SocialMediaPostsSchema:
    posts = session.query(SocialMediaPost).order_by(SocialMediaPost.created_at.desc()).all()
    return SocialMediaPostsSchema(items=[load_post_entity(post) for post in posts])


@app.get("/api/contents/{post_id}", response_model=SocialMediaPostSchema)
def get_post(post_id: int, session: Session = Depends(get_session)) -> SocialMediaPostSchema:
    post = session.get(SocialMediaPost, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publicación no encontrada.")
    return load_post_entity(post)


@app.post("/api/contents", response_model=SocialMediaPostSchema, status_code=status.HTTP_201_CREATED)
def create_post(request: SocialMediaPostCreateSchema, session: Session = Depends(get_session)) -> SocialMediaPostSchema:
    post = build_post_entity(request)
    session.add(post)
    session.commit()
    session.refresh(post)
    return load_post_entity(post)


@app.put("/api/contents/{post_id}", response_model=SocialMediaPostSchema)
def update_post(post_id: int, request: SocialMediaPostUpdateSchema, session: Session = Depends(get_session)) -> SocialMediaPostSchema:
    post = session.get(SocialMediaPost, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publicación no encontrada.")

    update_data = request.model_dump(exclude_unset=True)
    if "platform" in update_data:
        validate_platform(update_data["platform"])
        post.platform = update_data["platform"].strip()
    if "title" in update_data:
        post.title = update_data["title"].strip()
    if "tone" in update_data:
        post.tone = update_data["tone"].strip()
    if "content" in update_data:
        validate_content_length(post.platform, update_data["content"])
        post.content = update_data["content"].strip()
    if "hashtags" in update_data:
        post.hashtags = json.dumps(normalize_hashtags(update_data["hashtags"]), ensure_ascii=False)
    if "link" in update_data:
        post.link = validate_link(update_data["link"])
    if "language" in update_data:
        post.language = update_data["language"].strip() if update_data["language"] else None
    if "variants" in update_data:
        post.variants = json.dumps(normalize_variants(update_data["variants"]), ensure_ascii=False)

    post.updated_at = datetime.utcnow()
    session.add(post)
    session.commit()
    session.refresh(post)
    return load_post_entity(post)


@app.delete("/api/contents/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: Session = Depends(get_session)) -> None:
    post = session.get(SocialMediaPost, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publicación no encontrada.")
    session.delete(post)
    session.commit()


@app.post("/api/contents/generate", response_model=SocialMediaPostSchema)
def generate_content(request: GeneratePostRequest, session: Session = Depends(get_session)) -> SocialMediaPostSchema:
    validate_platform(request.platform)
    llm_result = generate_post_with_llm(request)

    # Override platform and tone with requested values when the model omits them or returns inconsistent data.
    llm_result.platform = request.platform
    llm_result.tone = request.tone
    llm_result.language = request.language or llm_result.language
    llm_result.hashtags = normalize_hashtags(llm_result.hashtags)
    if llm_result.variants:
        llm_result.variants = normalize_variants(llm_result.variants)

    validate_content_length(request.platform, llm_result.content)
    post = SocialMediaPost(
        platform=llm_result.platform,
        title=llm_result.title.strip(),
        tone=llm_result.tone.strip(),
        content=llm_result.content.strip(),
        hashtags=json.dumps(llm_result.hashtags, ensure_ascii=False) if llm_result.hashtags else None,
        link=validate_link(llm_result.link),
        language=llm_result.language.strip() if llm_result.language else request.language,
        variants=json.dumps(llm_result.variants, ensure_ascii=False) if llm_result.variants else None,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return load_post_entity(post)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
