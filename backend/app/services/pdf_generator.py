import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import white, black
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

LEVEL_TRANSLATIONS = {
    "beginner": "Débutant",
    "intermediate": "Intermédiaire",
    "advanced": "Avancé",
    "expert": "Expert"
}

def translate_level(level):
    if not level:
        return "Non précisé"
    level = level.strip().lower()
    return LEVEL_TRANSLATIONS.get(level, level.capitalize())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)

TEMPLATE_BASE = os.path.join(APP_DIR, "templates", "Template_CV_Base.pdf")

def clean_data(data):
    defaults = {
        "name": "Nom Prénom",
        "phone": "Pas de téléphone précisé",
        "email": "Pas d'email précisé",
        "address": "Pas d'adresse précisée",
        "license": "Pas de permis précisé",
        "about": "Pas de description",
        "links": []
    }
    for k, v in defaults.items():
        if not data.get(k):
            data[k] = v
    for k in ["languages", "skills", "interests", "education", "experience", "projects"]:
        if k not in data or not isinstance(data[k], list):
            data[k] = []
    return data

def draw_wrapped_text(can, x, y, text, max_width, font_name="Helvetica", font_size=10, color=black):
    text = str(text) if text else ""
    can.setFont(font_name, font_size)
    can.setFillColor(color)
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if can.stringWidth(test_line, font_name, font_size) < max_width:
            line = test_line
        else:
            can.drawString(x, y, line)
            y -= font_size + 2
            line = word
    if line:
        can.drawString(x, y, line)
        y -= font_size + 2
    return y

def generate_text_layer(data):
    buffer = BytesIO()
    can = canvas.Canvas(buffer, pagesize=A4)

    line_height = 12
    col_left_x = 15
    col_left_width = 160
    col_right_x = 250
    col_right_width = 300

    color_left = white
    color_right = black

    y_left = 825

    can.setFont("Helvetica-Bold", 12)
    can.setFillColor(color_left)
    can.drawString(col_left_x, y_left, "A PROPOS")
    y_left -= 20
    y_left = draw_wrapped_text(can, col_left_x, y_left, data["about"], col_left_width, color=color_left)

    y_left -= 15
    can.setFont("Helvetica-Bold", 12)
    can.drawString(col_left_x, y_left, "COORDONNÉES")
    y_left -= 20

    coords = ["phone", "email", "address", "license"]
    for idx, label in enumerate(coords):
        if idx > 0:
            y_left -= 5
        y_left = draw_wrapped_text(can, col_left_x, y_left, data[label], col_left_width, color=color_left)

    for link in data["links"]:
        link_type = link.get("type", "Lien")
        url = link.get("url", "")

        if url:
            y_left -= 5
            can.setFont("Helvetica", 10)
            can.setFillColor(color_left)
            can.drawString(col_left_x, y_left, link_type)

            text_width = can.stringWidth(link_type, "Helvetica", 10)
            can.linkURL(
                url,
                (col_left_x, y_left - 2, col_left_x + text_width, y_left + 10),
                relative=0
            )
            y_left -= 5
    
    y_left -= 15
    can.setFont("Helvetica-Bold", 12)
    can.drawString(col_left_x, y_left, "LANGUES")
    y_left -= 20
    for lang in data["languages"]:
        line = f"{lang.get('name', '')} : {lang.get('level', '')}"
        y_left = draw_wrapped_text(can, col_left_x, y_left, line, col_left_width, color=color_left)
        y_left -= 5

    y_left -= 15
    can.setFont("Helvetica-Bold", 12)
    can.drawString(col_left_x, y_left, "COMPÉTENCES")
    y_left -= 20
    for skill in data["skills"]:
        y_left = draw_wrapped_text(can, col_left_x, y_left, f"- {skill}", col_left_width, color=color_left)
        y_left -= 3

    y_left -= 15
    can.setFont("Helvetica-Bold", 12)
    can.drawString(col_left_x, y_left, "CENTRES D’INTÉRÊT")
    y_left -= 20
    for interest in data["interests"]:
        y_left = draw_wrapped_text(can, col_left_x, y_left, f"- {interest}", col_left_width, color=color_left)
        y_left -= 5

    y_right = 825
    can.setFont("Helvetica-Bold", 20)
    can.setFillColor(color_right)
    can.drawString(col_right_x, y_right, data["name"].upper())
    y_right -= 30

    can.setFont("Helvetica-Bold", 12)
    can.drawString(col_right_x, y_right, "FORMATION")
    y_right -= 25

    for edu in data["education"]:
        y_right = draw_wrapped_text(
            can, col_right_x, y_right,
            edu.get("title", ""),
            col_right_width,
            font_name="Helvetica-Bold",
            color=color_right
        )
        y_right = draw_wrapped_text(
            can, col_right_x + 10, y_right,
            edu.get("location", ""),
            col_right_width,
            font_name="Helvetica",
            color=color_right
        )
        y_right = draw_wrapped_text(
            can, col_right_x + 10, y_right,
            edu.get("period", ""),
            col_right_width,
            font_name="Helvetica-Oblique",
            color=color_right
        )
        y_right -= 10

    y_right -= 15
    can.setFont("Helvetica-Bold", 12)
    can.drawString(col_right_x, y_right, "EXPÉRIENCE PROFESSIONNELLE")
    y_right -= 25
    can.setFont("Helvetica", 10)
    for exp in data["experience"]:
        y_right = draw_wrapped_text(
            can, col_right_x, y_right,
            exp.get("title", ""),
            col_right_width,
            font_name="Helvetica-Bold",
            color=color_right
        )
        y_right = draw_wrapped_text(
            can, col_right_x + 10, y_right,
            exp.get("location", ""),
            col_right_width,
            font_name="Helvetica",
            color=color_right
        )
        y_right = draw_wrapped_text(
            can, col_right_x + 10, y_right,
            exp.get("period", ""),
            col_right_width,
            font_name="Helvetica-Oblique",
            color=color_right
        )
        for task in exp.get("tasks", []):
            y_right = draw_wrapped_text(
                can, col_right_x + 20, y_right,
                f"- {task}",
                col_right_width,
                font_name="Helvetica",
                color=color_right
            )
        y_right -= 10

    if data.get("projects"):
        y_right -= 5
        can.setFont("Helvetica-Bold", 11)
        can.drawString(col_right_x, y_right, "PROJETS")
        y_right -= 25
        for proj in data["projects"]:
            y_right = draw_wrapped_text(
                can, col_right_x, y_right,
                proj.get("title", ""),
                col_right_width,
                font_name="Helvetica-Bold",
                color=color_right
            )
            y_right = draw_wrapped_text(
                can, col_right_x + 10, y_right,
                proj.get("description", ""),
                col_right_width,
                font_name="Helvetica",
                color=color_right
            )
            y_right = draw_wrapped_text(
                can, col_right_x + 10, y_right,
                proj.get("period", ""),
                col_right_width,
                font_name="Helvetica-Oblique",
                color=color_right
            )
            y_right -= 15

    can.save()
    buffer.seek(0)
    return buffer

def generate_pdf(data: dict, output_path: str):
    for lang in data.get("languages", []):
        lang["level"] = translate_level(lang.get("level"))
    if isinstance(data.get("license"), bool):
        data["license"] = "Permis B" if data["license"] else "Pas de permis précisé"
    elif isinstance(data.get("license"), str) and data["license"].strip().lower() in ["true", "yes"]:
        data["license"] = "Permis B"
    elif not data.get("license"):
        data["license"] = "Pas de permis précisé"

    data = clean_data(data)
    text_layer = generate_text_layer(data)
    base_pdf = PdfReader(open(TEMPLATE_BASE, "rb"))
    text_pdf = PdfReader(text_layer)
    output = PdfWriter()
    base_page = base_pdf.pages[0]
    text_page = text_pdf.pages[0]
    base_page.merge_page(text_page)
    output.add_page(base_page)
    with open(output_path, "wb") as f:
        output.write(f)