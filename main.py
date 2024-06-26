# Install FastAPI pip install "fastapi[all]"
from fastapi import FastAPI
from routers import users, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles


# Start Server: uvicorn main:app --reload
app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

# Static files. Example http://127.0.0.1:8000/static/images/screenshot.png
app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/")
async def root():
    return "Hello"

