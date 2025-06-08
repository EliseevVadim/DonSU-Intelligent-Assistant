import torch

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_postgres import PGVector

from transformers import AutoTokenizer, AutoModel

from app.config import get_embeddings_model_name, get_knowledge_base_connection_string, get_collection_name, \
    get_generator_model_name, get_generator_base_endpoint, get_embeddings_model_revision
from app.constants import QA_PROMPT, CONTEXTUALIZE_QUESTION_PROMPT
from app.utils.embeddings import get_embeddings

embeddings_model_name = get_embeddings_model_name()
embeddings_model_revision = get_embeddings_model_revision()

vector_db_connection_string = get_knowledge_base_connection_string()
collection_name = get_collection_name()

device = 'cuda' if torch.cuda.is_available() else 'cpu'

embeddings_tokenizer = AutoTokenizer.from_pretrained(embeddings_model_name)
embeddings_model = AutoModel.from_pretrained(embeddings_model_name, trust_remote_code=True,
                                             device_map=device, revision=embeddings_model_revision)

embeddings = get_embeddings(embeddings_model)

vector_db = PGVector.from_existing_index(
    embedding=embeddings,
    collection_name=collection_name,
    connection=vector_db_connection_string
)

llm = ChatOpenAI(
    model=get_generator_model_name(),
    base_url=get_generator_base_endpoint(),
    api_key='not needed atm'
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", CONTEXTUALIZE_QUESTION_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

retriever = create_history_aware_retriever(
    llm=llm,
    retriever=vector_db.as_retriever(),
    prompt=contextualize_q_prompt
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", QA_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

document_prompt = PromptTemplate(
    input_variables=["page_content", "filename", "last_updated"],
    template=(
        "[METADATA]\n"
        "filename: {filename}\n"
        "last_updated: {last_updated}\n\n"
        "[CONTENT]\n"
        "{page_content}"
    )
)

qa_chain = create_stuff_documents_chain(llm=llm, prompt=qa_prompt, document_prompt=document_prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)


def get_vector_db() -> PGVector:
    return vector_db


def get_chain():
    return rag_chain
