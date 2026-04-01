from pydantic import BaseModel
from typing import Optional

class ParseRequest(BaseModel):
    file_url: str
    file_type: str

class ParseResponse(BaseModel):
    extracted_text: str
    page_count: int

class SummarizeRequest(BaseModel):
    extracted_text: str
    document_id: str

class SummarizeResponse(BaseModel):
    summary_text: str
    key_topics: list[str]
    model_used: str

class ChatHistoryItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    document_text: str
    history: list[ChatHistoryItem] = []

class CompareRequest(BaseModel):
    document_a_text: str
    document_b_text: str

class CompareResponse(BaseModel):
    comparison_text: str

class ExtractRequest(BaseModel):
    document_text: str

class ExtractResponse(BaseModel):
    dates: list[str] = []
    parties: list[str] = []
    amounts: list[str] = []