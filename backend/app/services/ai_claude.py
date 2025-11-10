from app.core.config import settings
import requests
import re
import json
from app.services.parser import extract_periods

def extract_json_from_claude_response(json_result):
    raw_text = json_result['content'][0]['text']
    match = re.search(r"\s*```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if not match:
        match = re.search(r"(\{.*\})", raw_text, re.DOTALL)
        if not match:
            raise ValueError("Format JSON non trouvé")

    json_str = match.group(1)
    return json.loads(json_str)

def ask_claude(text: str) -> dict:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": settings.CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    periods = extract_periods(text)
    periods_str = "; ".join(periods) if periods else "Aucune période détectée"

    data = {
        "model": settings.CLAUDE_MODEL,
        "max_tokens": 2000,
        "messages": [
            {
                "role": "user",
                "content": f"""
Tu es un assistant spécialisé dans l'analyse de CV. Extrait les informations suivantes au format JSON clair, structuré et minimal :
- name
- phone
- email
- address
- license
- about (texte introductif ou profil s’il existe)
- languages (liste de dictionnaires avec name et level, le niveau doit être en français)
- skills (liste de chaînes)
- interests (liste de chaînes)
- education (liste de dictionnaires avec title, location et period)
- experience (liste de dictionnaires avec title, location, tasks[] et period)
- projects (optionnel : liste de dictionnaires avec title, description et period)

Pour chaque élément de education et experience, ajoute un champ period s’il est connu.

Voici des périodes détectées automatiquement : {periods_str}

Si le CV contient une section « Projets » distincte de l'expérience, mets-la dans "projects". Cela ne doit PAS remplacer ni réduire la section "experience".

Si pas de section "À propos", prends le premier paragraphe comme "about".

Analyse tout le texte, même sans titres clairs. Corrige les fautes d'orthographe et garde les majuscules au début des phrases.

IMPORTANT : Si un niveau est indiqué avec des barres | ou des étoiles *, interprète-le en niveau clair : beginner, intermediate, advanced ou expert. S'il y en a, tu essayeras aussi d'interpréter les barres de progression de la même manière.

Voici le texte :
{text}

Tiens compte des périodes pour remplir "period" dans education, experience et projects.

Réponds UNIQUEMENT en JSON, encadré par ```json si tu veux.
"""
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    json_result = response.json()

    try:
        data = extract_json_from_claude_response(json_result)
    except Exception as e:
        raise RuntimeError(f"Erreur d'extraction JSON : {e}")

    required_keys = ['name', 'email', 'skills']
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Clé manquante dans les données : {key}")

    return data