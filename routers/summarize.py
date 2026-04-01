from fastapi import APIRouter, HTTPException
from models.schemas import SummarizeRequest, SummarizeResponse
from service.claude_service import summarize

router = APIRouter()

@router.post("", response_model=SummarizeResponse)
def summarize_doc(request: SummarizeRequest):
    try:
        result = summarize(request.extracted_text)
        return SummarizeResponse(
            summary_text=result["summary_text"],
            key_topics=result["key_topics"],
            model_used=result["model_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))