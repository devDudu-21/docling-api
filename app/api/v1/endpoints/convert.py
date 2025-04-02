from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Response
from fastapi.responses import HTMLResponse, JSONResponse
from app.services.converter import parse_document
import os
import uuid
import json

router = APIRouter()

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
def convert_document(
    file: UploadFile = File(...),
    output_format: str = Form("markdown")
):
    # Tipos suportados
    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff"]

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Formato não suportado: {ext}. Tipos aceitos: {', '.join(allowed_extensions)}"
        )

    file_id = str(uuid.uuid4())
    temp_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")

    contents = file.file.read()
    with open(temp_path, "wb") as f:
        f.write(contents)

    try:
        output = parse_document(temp_path, output_format=output_format)

        format_lower = output_format.lower()
        if format_lower == "json":
            try:
                return JSONResponse(content=json.loads(output))
            except json.JSONDecodeError:
                return JSONResponse(content={"content": output})
        elif format_lower == "html":
            return HTMLResponse(content=output)
        else:
            # Isso força o FastAPI/Uvicorn a não tentar adivinhar o tamanho
            return Response(content=output.encode("utf-8"), media_type="text/plain")
    finally:
        os.remove(temp_path)
