from docling.document_converter import DocumentConverter, InputFormat
from typing import Optional
import os

def parse_document(file_path: str, output_format: str = "markdown") -> str:
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        input_format = InputFormat.PDF
    elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        input_format = InputFormat.IMAGE
    else:
        raise ValueError(f"Formato de entrada não suportado: {ext}")

    output_format_normalized = output_format.lower()
    if output_format_normalized not in {"markdown", "html", "json"}:
        raise ValueError(f"Formato de saída não suportado: {output_format}")

    converter = DocumentConverter()
    result = converter.convert(source=file_path)

    doc = result.document

    if output_format_normalized == "markdown":
        return doc.export_to_markdown()
    elif output_format_normalized == "html":
        return doc.export_to_html()
    elif output_format_normalized == "json":
        return doc.model_dump_json(indent=2)

    raise RuntimeError(f"O formato {output_format} não pôde ser montado.")
