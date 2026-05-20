import time
import random


LLM_FAILURE_MODE = True


def call_external_llm(prompt: str) -> str:
    """
    This function simulates an external LLM API.

    If LLM_FAILURE_MODE is True, the service fails randomly.
    This represents an unreliable external API.
    """

    if LLM_FAILURE_MODE:
        should_fail = random.choice([True, True, True, False])

        if should_fail:
            time.sleep(2)
            raise Exception("External LLM API failed or timed out")

    time.sleep(1)

    return f"LLM response for: {prompt}"