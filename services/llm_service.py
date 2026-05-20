import time
import random


LLM_FAILURE_MODE = True


def call_external_llm(prompt: str) -> str:

    print("\n[LLM] Sending request to external API...")

    if LLM_FAILURE_MODE:

        should_fail = random.choice([True, True, True, False])

        if should_fail:

            print("[LLM] External API is hanging...")

            # simulate huge timeout
            time.sleep(8)

            print("[LLM] External API crashed!")

            raise Exception("External LLM API failed or timed out Ammar Khan Bscs23059")

    print("[LLM] External API succeeded!")

    time.sleep(1)

    return f"LLM response for: {prompt} "