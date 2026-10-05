# AI Mental Health Chatbot Backend API Documentation

## Base URL

```
http://127.0.0.1:8000
```

---

# API Endpoints

## 1. Home Endpoint

### GET /

### Description

Checks whether the backend server is running.

### Response

```json
{
  "message": "AI Mental Health Chatbot Backend Running Successfully!"
}
```

---

## 2. Predict Mental Health Analysis

### POST /predict

### Description

Analyzes the user's text and predicts:

- Emotion
- Stress
- Depression

### Request Body

```json
{
  "text": "I feel very lonely and sad. I have lost interest in everything and I feel stressed."
}
```

### Successful Response (200)

```json
{
  "emotion": "sadness",
  "emotion_confidence": 88.69,
  "stress": "Stress",
  "stress_confidence": 98.51,
  "depression": "Depression",
  "depression_confidence": 99.97
}
```

---

### Error Response (422)

Occurs when the request body is invalid.

Example:

```json
{
  "detail": [
    {
      "msg": "Field required"
    }
  ]
}
```

---

# Testing

Run the backend:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# Current API Version

Version: 1.0.0

---

# Planned Future APIs

The following APIs will be implemented in upcoming development phases:

- POST /chat
- POST /voice
- POST /journal
- GET /mood-history
- POST /login
- POST /register