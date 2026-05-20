# Ammar Khan — BSCS23059

# PDC Assignment 4 — Resilient Distributed System

This project implements a minimal FastAPI backend for the StudySync scenario described in the assignment.

The implemented distributed systems solution is the **Circuit Breaker Pattern** for handling failures in an external LLM API dependency.

The goal is to improve:
- fault tolerance
- resilience
- graceful degradation
- dependency isolation

when an external service becomes unreliable.

---

# Implemented Distributed Systems Concepts

- Circuit Breaker Pattern
- Fault Tolerance
- Graceful Degradation
- Failure Isolation
- Middleware
- Simulated External API Failures
- Automated Testing using Pytest

---

# Features

- FastAPI backend
- Simulated unreliable external LLM API
- Circuit Breaker protection
- Fallback responses during failure
- Required `X-Student-ID` response header
- Automated test cases using pytest
- Failure simulation for demo purposes

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Server

```bash
uvicorn main:app --reload
```

Server will run at:

```txt
http://127.0.0.1:8000
```

---

# Open Swagger UI

Open:

```txt
http://127.0.0.1:8000/docs
```

This allows testing the API interactively.

---

# Test Home Route and Student Header

Run:

```bash
curl -i http://127.0.0.1:8000/
```

Expected header:

```txt
X-Student-ID: BSCS23059
```

---

# Test LLM API Through Circuit Breaker

Run:

```bash
curl -i -X POST "http://127.0.0.1:8000/chat" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"prompt\":\"hello\"}"
```

---

# Expected Successful Response

```json
{
  "prompt": "hello",
  "response": "LLM response for: hello"
}
```

---

# Expected Fallback Response During Failure

```json
{
  "prompt": "hello",
  "response": "Fallback response: LLM request failed safely."
}
```

---

# Expected Response When Circuit Opens

```json
{
  "prompt": "hello",
  "response": "Fallback response: LLM service unavailable."
}
```

---

# Run Tests

Run:

```bash
pytest -v
```

The tests verify:
- API functionality
- middleware header injection
- fault tolerance behavior
- circuit breaker handling

---

# Project Structure

```txt
PDC-Sp24-BSCS23059-AmmarKhan/
│
├── main.py
├── circuit_breaker.py
├── requirements.txt
├── README.md
│
├── services/
│   ├── __init__.py
│   └── llm_service.py
│
└── tests/
    ├── conftest.py
    └── test_failures.py
```

---

# File Descriptions

## `main.py`

Contains:
- FastAPI application
- API endpoints
- middleware
- request handling

---

## `circuit_breaker.py`

Implements the Circuit Breaker pattern using:

```python
pybreaker.CircuitBreaker
```

This file:
- monitors repeated failures
- opens the circuit after repeated crashes
- blocks unhealthy requests
- returns fallback responses

---

## `services/llm_service.py`

Simulates an unreliable external LLM API.

The file intentionally introduces:
- random failures
- artificial delay
- timeout behavior

to simulate real distributed system failures.

---

## `tests/test_failures.py`

Contains automated pytest test cases for:
- API routes
- middleware validation
- circuit breaker functionality

---

# Additional Notes

## Disable Simulated Failures

The simulated external LLM API behavior is controlled inside:

```python
services/llm_service.py
```

By default:

```python
LLM_FAILURE_MODE = True
```

This intentionally simulates:
- external API crashes
- timeout behavior
- unreliable network conditions

To disable simulated failures and make the LLM service always succeed, change it to:

```python
LLM_FAILURE_MODE = False
```

---

# Demonstrating the "Before Fix" Scenario

The `/chat` endpoint currently routes requests through the Circuit Breaker:

```python
response = call_llm_with_circuit_breaker(request.prompt)
```

inside:

```python
main.py
```

To directly call the external LLM service without fault tolerance protection, replace it with:

```python
from services.llm_service import call_external_llm

response = call_external_llm(request.prompt)
```

This bypasses the Circuit Breaker and demonstrates the "before fix" behavior where failures propagate directly to FastAPI and may produce:

```txt
Internal Server Error
```

---

# Circuit Breaker Behavior

The Circuit Breaker is configured in:

```python
circuit_breaker.py
```

Current configuration:

```python
llm_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=15
)
```

Meaning:
- after 3 consecutive failures, the circuit opens
- requests stop reaching the failing LLM service
- fallback responses are returned immediately
- after 15 seconds, the breaker attempts recovery

---

# Distributed Systems Explanation

The external LLM service acts as a distributed dependency.

Without protection:
- failures propagate upward
- requests hang or crash
- the dependency becomes a single point of failure

The Circuit Breaker prevents repeated requests from reaching an unhealthy dependency.

Instead of crashing, the system:
- isolates the failure
- returns fallback responses
- degrades gracefully
- remains available to users

This improves:
- fault tolerance
- resilience
- availability

in the distributed system.