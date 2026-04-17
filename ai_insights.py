"""
ai_insights.py — Groq API integration for Life Dashboard.

Takes computed statistics and returns 3–5 human-readable,
actionable insights about the user's habits.
"""

import os
import json
import asyncio
from typing import Any
from groq import Groq, APIError
from dotenv import load_dotenv

# Load .env file automatically (reads GROQ_API_KEY from .env)
load_dotenv()


async def generate_insights(stats: dict[str, Any]) -> list[str]:
    """
    Send computed stats to Groq LLM and get back insight bullets.

    Args:
        stats: The statistics dict from analysis.compute_stats()

    Returns:
        A list of 3–5 insight strings.
    """

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return [
            "⚠️ GROQ_API_KEY not set.",
            "Add it to your .env file: GROQ_API_KEY=your-key-here",
        ]

    # Edge case: not enough data yet
    if stats.get("entry_count", 0) < 3:
        return ["📊 Add at least 3 days of data to generate insights."]

    prompt = _build_prompt(stats)

    try:
        client = Groq(api_key=api_key)

        # Use get_running_loop() — correct modern approach inside async functions
        loop = asyncio.get_running_loop()

        message = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            ),
        )

        insights = _parse_insights(message.choices[0].message.content)

        # Ensure we always return at least 3 insights
        if len(insights) < 3:
            insights.append("📊 Add more data entries for richer insights.")

        return insights

    except APIError as e:
        return [f"⚠️ Groq API error: {str(e)}"]
    except Exception as e:
        return [f"⚠️ Unexpected error: {str(e)}"]


def _build_prompt(stats: dict[str, Any]) -> str:
    """Build the prompt that gives the LLM all context it needs."""

    return f"""You are a personal data analyst. A user has been tracking their daily habits 
(study hours, sleep hours, screen time, and mood on a 1-10 scale).

Here are their computed statistics:

{json.dumps(stats, indent=2)}

Based on this data, provide exactly 3 to 5 bullet-point insights. Each insight should:
- Be specific and reference actual numbers from the data
- Be actionable (suggest what the user could do differently)
- Be written in a friendly, encouraging tone
- Start with a relevant emoji

Examples of good insights:
- "😴 Your mood is 40% higher on days you sleep 7+ hours — prioritize rest!"
- "📱 High screen time correlates with lower study output (r=-0.6)"
- "📈 Your productivity peaks mid-week — plan big tasks for Tuesday-Thursday"

Return ONLY the bullet points, one per line, starting each with "- ".
Do not include any other text, headers, or explanations."""


def _parse_insights(response_text: str) -> list[str]:
    """Parse LLM response into a clean list of insight strings."""

    lines = response_text.strip().split("\n")
    insights = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Strip leading bullet markers
        if line.startswith("- "):
            line = line[2:]
        elif line.startswith("• "):
            line = line[2:]
        if line:
            insights.append(line)

    return insights


async def chat_with_data(message: str, data: list[dict[str, Any]], stats: dict[str, Any]) -> str:
    """
    Allow the user to converse with the AI about their data.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "⚠️ GROQ_API_KEY not set. Please set the environment variable to enable the AI chat."

    prompt = f"""You are a personal data analyst and life coach. A user has been tracking their daily habits 
(study hours, sleep hours, screen time, and mood on a 1-10 scale).

Here are their computed statistics:
{json.dumps(stats, indent=2)}

Here is their raw data:
{json.dumps(data, indent=2)}

The user asks: "{message}"

Address the user directly. Keep your response concise, helpful, and friendly.
Use specific data points to support your answer if relevant.
Do NOT use markdown headers or lists, keep it conversational and short.
"""

    try:
        client = Groq(api_key=api_key)
        loop = asyncio.get_running_loop()

        reply = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            ),
        )

        return reply.choices[0].message.content

    except APIError as e:
        return f"⚠️ Groq API error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error in chat: {str(e)}"


# ── Standalone test ────────────────────────────────────────
if __name__ == "__main__":
    sample_stats = {
        "total_entries": 10,
        "avg_sleep": 6.2,
        "avg_study": 3.8,
        "avg_mood": 6.1,
        "avg_screen_time": 4.5,
        "sleep_mood_correlation": 0.82,
        "sleep_study_correlation": 0.61,
        "screen_mood_correlation": -0.74,
        "best_day": "2024-01-15",
        "worst_day": "2024-01-12",
        "mood_trend": "declining",
    }

    # Test code removed for production