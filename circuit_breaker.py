import pybreaker

from services.llm_service import call_external_llm


llm_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=10
)


def call_llm_with_circuit_breaker(prompt: str) -> str:
    try:
        return llm_circuit_breaker.call(call_external_llm, prompt)

    except pybreaker.CircuitBreakerError:
        return (
            "Fallback response: The LLM service is temporarily unavailable. "
            "Please try again later."
        )

    except Exception:
        return (
            "Fallback response: The LLM request failed, but the application "
            "is still running safely."
        )