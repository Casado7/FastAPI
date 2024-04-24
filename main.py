from fastapi import FastAPI
from routers import users


# Start Server: uvicorn main:app --reload
app = FastAPI()

# Routers
app.include_router(users.router)

@app.get("/")
async def root():
    return "Hello"

