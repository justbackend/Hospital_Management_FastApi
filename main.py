from fastapi import FastAPI
from database import Base, engine
from routes import users, temp_patients, admin, login, screen
from routes.login import get_password_hash
from starlette.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"])


app.include_router(login.login_router)
app.include_router(users.users_router)
app.include_router(temp_patients.temp_patients_router)
app.include_router(admin.admin_router)
app.include_router(screen.screen_router)




