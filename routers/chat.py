from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.schemas import ChatRequest
from service.claude_service import chat_stream

router = APIRouter()

@router.post("")
def chat(request: ChatRequest):
    try:
        def generate():
            for chunk in chat_stream(
                request.question,
                request.document_text,
                [h.model_dump() for h in request.history]
            ):
                yield f"data: {chunk}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))