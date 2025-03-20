from fastapi import FastAPI

from app.business_logic.users.router import router as users_router

app = FastAPI(title='DonSU Intelligent Assistant', description='The official API of DonSU Intelligent Assistant.',
              version='1.0.0')

app.include_router(users_router)
