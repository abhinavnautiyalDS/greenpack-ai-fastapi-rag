from langchain_cohere import CohereEmbeddings
from app.config.settings import settings

embedding_model = CohereEmbeddings(
    cohere_api_key=settings.COHERE_API_KEY,
    model="embed-english-v3.0"
)