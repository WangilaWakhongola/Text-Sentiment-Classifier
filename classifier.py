"""
Sentiment Classifier using Anthropic Claude API
Classifies text as: positive, negative, or neutral
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a sentiment analysis engine.
Analyze the sentiment of the given text and respond ONLY with a JSON object in this exact format:
{
  "sentiment": "positive" | "negative" | "neutral",
  "confidence": 0.0 to 1.0,
  "reason": "one short sentence explaining the classification"
}
Do not include any other text or markdown."""


def classify_text(text: str) -> dict:
    """
    Classify the sentiment of a single text string.

    Args:
        text: The input text to classify.

    Returns:
        A dict with keys: sentiment, confidence, reason
    """
    if not text or not text.strip():
        return {"sentiment": "neutral", "confidence": 1.0, "reason": "Empty input."}

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Fast & cost-efficient for classification
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text.strip()}],
    )

    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    result = json.loads(raw)
    return result


def classify_batch(texts: list[str]) -> list[dict]:
    """
    Classify a list of texts.

    Args:
        texts: List of input strings.

    Returns:
        List of result dicts, one per input text.
    """
    results = []
    for text in texts:
        try:
            result = classify_text(text)
        except Exception as e:
            result = {
                "sentiment": "error",
                "confidence": 0.0,
                "reason": f"Classification failed: {e}",
            }
        results.append(result)
    return results
