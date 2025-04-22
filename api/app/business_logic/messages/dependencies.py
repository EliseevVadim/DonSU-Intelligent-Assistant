import torch
from langchain_postgres import PGVector
from transformers import AutoTokenizer, AutoModel

from app.config import get_embeddings_model_name, get_knowledge_base_connection_string, get_collection_name
from app.utils.embeddings import get_embeddings

embeddings_model_name = get_embeddings_model_name()

vector_db_connection_string = get_knowledge_base_connection_string()
collection_name = get_collection_name()

device = 'cuda' if torch.cuda.is_available() else 'cpu'

embeddings_tokenizer = AutoTokenizer.from_pretrained(embeddings_model_name)
embeddings_model = AutoModel.from_pretrained(embeddings_model_name, trust_remote_code=True, device_map=device)

embeddings = get_embeddings(embeddings_model)

vector_db = PGVector.from_existing_index(
    embedding=embeddings,
    collection_name=collection_name,
    connection=vector_db_connection_string
)


def get_vector_db() -> PGVector:
    return vector_db
