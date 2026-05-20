import pybreaker

from services.llm_service import call_external_llm


llm_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=15
)


def call_llm_with_circuit_breaker(prompt: str) -> str:

    try:
        print("\n[CIRCUIT] Calling external LLM service...")

        response = llm_circuit_breaker.call(
            call_external_llm,
            prompt
        )

        print("[CIRCUIT] Request succeeded!")

        return response

    except pybreaker.CircuitBreakerError:

        print("[CIRCUIT] CIRCUIT OPENED!")
        print("[CIRCUIT] Blocking requests to failed service!")

        return (
            "Fallback response: LLM service unavailable."
        )

    except Exception as e:

        print(f"[CIRCUIT] FAILURE DETECTED: {e}")

        return (
            "Fallback response: LLM request failed safely."
        )