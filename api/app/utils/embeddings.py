import numpy as np
import torch.nn.functional as F

from langchain_core.embeddings import Embeddings
from numpy import ndarray, dtype
from typing import Any

from app.utils.common import free_memory


class GigaEmbeddings(Embeddings):
    def __init__(self, model):
        self.model = model
        self.task_name_to_instruct = {
            "example": "Given a question, retrieve passages that answer the question"
        }
        self.query_prefix = self.task_name_to_instruct["example"] + "\nquestion: "
        self.passage_prefix = ""

    def embed_documents(self, texts: list[str]) -> ndarray[Any, dtype[Any]]:
        embeddings = []
        for text in texts:
            embedding = self.model.encode([text], instruction=self.passage_prefix).cpu()
            embedding = F.normalize(embedding, p=2, dim=1)
            embeddings.append(embedding)
            free_memory()

        return np.vstack([embedding.numpy() for embedding in embeddings])

    def embed_query(self, text: str) -> list[float]:
        embeddings = self.model.encode([text], instruction=self.query_prefix).cpu()
        embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings[0].tolist()


def get_embeddings(model):
    return GigaEmbeddings(model)
