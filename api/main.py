from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.business_logic.users.router import router as users_router
from app.business_logic.chats.router import router as chats_router
from app.business_logic.messages.router import router as messages_router
from app.config import get_secret_key

app = FastAPI(title='DonSU Intelligent Assistant', description='The official API of DonSU Intelligent Assistant.',
              version='1.0.0')

app.add_middleware(SessionMiddleware, secret_key=get_secret_key())

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(chats_router)
app.include_router(messages_router)
