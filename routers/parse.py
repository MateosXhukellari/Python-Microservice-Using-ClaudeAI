from fastapi import APIRouter, HTTPException
from models.schemas import ParseRequest, ParseResponse
from service.parser import download_and_parse

router = APIRouter()

@router.post("", response_model=ParseResponse)
async def parse(request: ParseRequest):
    try:
        text, page_count = await download_and_parse(
            request.file_url,
            request.file_type
        )
        return ParseResponse(
            extracted_text=text,
            page_count=page_count
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))