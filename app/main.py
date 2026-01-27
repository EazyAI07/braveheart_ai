from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.chat import router as chat_router


app = FastAPI(title="BraveHeart API")

app.include_router(chat_router)

app.mount(
    "/",
    StaticFiles(directory="app/frontend", html=True),
    name="frontend"
)

@app.get("/health")
def health():
    return {"status": "ok"}
