# Application de Standardisation de CV

Ce projet est une application web qui permet :
- d’importer un CV (PDF, DOCX, image),
- d’extraire ses informations principales (coordonnées, expériences, formations, compétences, langues, etc.),
- de générer un CV standardisé au format PDF, selon un modèle pré-défini.

## **Fonctionnalités**

- Import direct de fichier
- Détection multiformat (PDF, Word, image)
- Analyse du contenu avec **Claude AI**
- OCR pour les CV scannés ou images
- Option **standardisation anonyme** (suppression des infos personnelles)
- CV final respectant un **template PDF professionnel**
- Téléchargement immédiat du CV standardisé
- Déploiement facile grâce à **Docker**

## **Installation**

### Build et démarrage avec Docker Compose

Dans le terminal à la racine du projet :

`docker-compose up --build`

### Configurer l'environnement Python

```
cd backend 

python -m venv venv  

venv\Scripts\activate

pip install -r requirements.txt
```   

### Configurer Claude API

Créer un fichier .env dans backend/ :

CLAUDE_API_KEY=cle_api
CLAUDE_MODEL=claude-3-opus-20240229
TESSERACT_PATH=chemin/vers/tesseract.exe

#### Lancer le backend

`uvicorn main:app --reload`

#### Lancer le frontend

Dans un autre terminal :

```
npm install
npm start
```

### Utilisation

- Ouvrir la page http://localhost:3000.

- Déposer ou importer un CV.

- Cliquer sur Standardiser ou Standardiser de manière anonyme, en fonction des besoins.

- Télécharger le CV final standardisé.

### Points Techniques

Claude extrait un JSON structuré des infos principales.

pdf_generator.py applique un rendu conforme au template PDF.

OCR automatique pour les images ou PDF scannés.

Détection améliorée pour langues (CEFR), projets, périodes.

Option anonymisation dynamique côté API.  
  
### Auteur

Développé par Alex Montagne pour la société Aprogsys.
