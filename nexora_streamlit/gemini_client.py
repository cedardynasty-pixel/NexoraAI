"""
gemini_client.py — thin wrapper around Google's Gemini API for the
student AI Study Tools (notes, worksheets, study plans, flashcards).

Requires: pip install google-genai
Get a free API key at https://aistudio.google.com/apikey
"""

import json
import re

from google import genai

# Change this if Google renames or retires this model in the future.
DEFAULT_MODEL = "gemini-3.6-flash"


def _client(api_key: str) -> genai.Client:
    if not api_key:
        raise ValueError("No Gemini API key configured. Ask an admin to add one in the Admin panel.")
    return genai.Client(api_key=api_key)


def _generate(prompt: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    client = _client(api_key)
    response = client.models.generate_content(model=model, contents=prompt)
    return (response.text or "").strip()


def _extract_json(text: str):
    """Gemini sometimes wraps JSON in ```json fences — strip them before parsing."""
    cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)


def generate_notes(topic: str, grade: str, api_key: str) -> str:
    prompt = (
        f"You are a helpful teacher creating study notes for a {grade} student. "
        f"Write clear, well-organized study notes on the topic: '{topic}'. "
        "Use markdown headings and bullet points, with simple language appropriate for "
        "this grade level. End with a short summary."
    )
    return _generate(prompt, api_key)


def generate_worksheet(topic: str, grade: str, num_questions: int, api_key: str) -> str:
    prompt = (
        f"Create a practice worksheet for a {grade} student on the topic: '{topic}'. "
        f"Include exactly {num_questions} numbered questions of mixed difficulty "
        "(easy, medium, hard). After the questions, add a separate 'Answer Key' section "
        "with the correct answers and brief explanations. Format the whole thing in markdown."
    )
    return _generate(prompt, api_key)


def generate_study_plan(subject: str, grade: str, duration: str, goal: str, api_key: str) -> str:
    prompt = (
        f"Create a structured study plan for a {grade} student studying {subject}. "
        f"The plan should span {duration} and help the student achieve this goal: '{goal}'. "
        "Break it down day-by-day (or week-by-week if the duration is long), with specific "
        "topics, tasks, and short revision checkpoints. Format it as a clear markdown table or list."
    )
    return _generate(prompt, api_key)


def generate_flashcards(topic: str, grade: str, count: int, api_key: str) -> list[dict]:
    """Returns a list of {"question": ..., "answer": ...} dicts."""
    prompt = (
        f"Create exactly {count} flashcards for a {grade} student studying '{topic}'. "
        'Respond ONLY with a JSON array, no other text, in this exact format: '
        '[{"question": "...", "answer": "..."}, ...]'
    )
    raw = _generate(prompt, api_key)
    try:
        cards = _extract_json(raw)
        if isinstance(cards, list) and cards:
            return cards
    except (json.JSONDecodeError, ValueError):
        pass
    # Fallback so nothing is silently lost if the model didn't return clean JSON
    return [{"question": "Raw model output (couldn't be parsed as flashcards)", "answer": raw}]
