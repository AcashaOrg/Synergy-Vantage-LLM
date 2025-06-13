"""Run empathy benchmark prompts through an OpenAI model."""

import json
import logging
import os

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - fallback for minimal envs
    import openai_stub as openai  # type: ignore

logging.basicConfig(level=logging.INFO)


def load_prompts(path: str) -> list[str]:
    """Load prompts from a JSON file."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def run_model(prompt: str) -> str:
    """Call the OpenAI API and return the response text."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=prompt)
    return response.choices[0].text.strip()


def main() -> None:
    """Execute the benchmark and log frequency tags."""
    prompts = load_prompts("prompts.json")
    for prompt in prompts:
        logging.info("Prompt: %s", prompt)
        result = run_model(prompt)
        logging.info("Result: %s [freq]", result)


if __name__ == "__main__":
    main()
