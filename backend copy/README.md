# AI Mental Health Chatbot Backend

## Final Year Project (FYP)

This repository contains the backend implementation of the AI Mental Health Chatbot developed as a Final Year Project.

---

## Features

- Emotion Detection
- Stress Detection
- Depression Detection
- FastAPI Backend
- REST API
- Swagger Documentation
- Modular Backend Architecture

---

## Project Structure

```
backend/

app/
    api/
    services/
    ai/
        emotion_detection/
        stress_detection/
        depression_detection/
        rag/
        llm/
    database/
    utils/
    voice/

datasets/
evaluation/
knowledge_base/
models/
tests/
```

---

## Technologies Used

- Python 3.10
- FastAPI
- Hugging Face Transformers
- PyTorch
- Scikit-learn
- Pandas
- NumPy
- Uvicorn

---

## Installation

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Backend

```bash
uvicorn app.main:app --reload
```

Backend

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## Current Modules

Completed

- Emotion Detection
- Stress Detection
- Depression Detection
- Prediction API

Under Development

- RAG
- LLM Integration
- Authentication
- Mood Tracking
- Voice Support

---

## Authors

Final Year Project Team

National University of Modern Languages (NUML)