from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health, parse, summarize, chat, compare, extract

app = FastAPI(title="DocuMind AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(parse.router, prefix="/parse")
app.include_router(summarize.router, prefix="/summarize")
app.include_router(chat.router, prefix="/chat")
app.include_router(compare.router, prefix="/compare")
app.include_router(extract.router, prefix="/extract")