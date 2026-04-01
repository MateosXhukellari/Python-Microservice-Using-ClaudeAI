from fastapi import APIRouter, HTTPException
from models.schemas import CompareRequest, CompareResponse
from service.claude_service import compare

router = APIRouter()

@router.post("", response_model=CompareResponse)
def compare_docs(request: CompareRequest):
    try:
        result = compare(request.document_a_text, request.document_b_text)
        return CompareResponse(comparison_text=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))