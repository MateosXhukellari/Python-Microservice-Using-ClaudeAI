from fastapi import APIRouter, HTTPException
from models.schemas import ExtractRequest, ExtractResponse
from service.claude_service import extract

router = APIRouter()

@router.post("", response_model=ExtractResponse)
def extract_data(request: ExtractRequest):
    try:
        result = extract(request.document_text)
        return ExtractResponse(
            dates=result.get("dates", []),
            parties=result.get("parties", []),
            amounts=result.get("amounts", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))