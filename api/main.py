from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.business_logic.users.router import router as users_router
from app.config import get_secret_key

app = FastAPI(title='DonSU Intelligent Assistant', description='The official API of DonSU Intelligent Assistant.',
              version='1.0.0')

app.add_middleware(SessionMiddleware, secret_key=get_secret_key())

app.include_router(users_router)
