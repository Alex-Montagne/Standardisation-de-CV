import os
import re
import uuid
import shutil
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services import parser, ocr, ai_claude, pdf_generator

router = APIRouter()

@router.post("/upload")
async def upload_cv(
    file: UploadFile = File(...),
    anonymous: bool = Form(False)
):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            content = f.read()

        if file.filename.endswith('.pdf'):
            text = parser._parse_pdf(content)
        elif file.filename.endswith('.docx'):
            text = parser._parse_docx(content)
        elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
            text = ocr.extract_text_from_image(content)
        else:
            raise HTTPException(status_code=400, detail="Format non supporté")
        
        def extract_contacts(text):
            phone = None
            email = None
            address = None

            phone_match = re.search(r"(\+33\s?|\b0)[1-9](\s?\d{2}){4}", text)
            if phone_match:
                phone = phone_match.group().strip()

            email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
            if email_match:
                email = email_match.group().strip()

            return {
                "phone": phone,
                "email": email,
            }

        contacts = extract_contacts(text)
        structured_data = ai_claude.ask_claude(text)

        if contacts["phone"] and not structured_data.get("phone"):
            structured_data["phone"] = contacts["phone"]

        if contacts["email"] and not structured_data.get("email"):
            structured_data["email"] = contacts["email"]

        structured_data = ai_claude.ask_claude(text)

        if anonymous:
            structured_data["phone"] = "Anonyme"
            structured_data["email"] = "Anonyme"
            structured_data["address"] = "Anonyme"
            structured_data["license"] = "Anonyme"
            name = structured_data.get("name", "")
            structured_data["name"] = name.split()[0] if name else "Anonyme"

        person_name = structured_data.get("name", "cv").replace(" ", "_").lower()
        filename = f"standardized_cv_{person_name}_{uuid.uuid4().hex[:8]}.pdf"

        output_dir = os.path.join("app", "outputs")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, filename)
        pdf_generator.generate_pdf(structured_data, output_path)

        output_url = f"http://localhost:8000/outputs/{filename}"

        return {"message": "Traitement réussi", "output_pdf": output_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur : {e}")

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)