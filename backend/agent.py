import os
import re
import json
from groq import Groq
from dotenv import load_dotenv
from memory import get_latest_identity, get_latest_log, save_reinforcement

load_dotenv()

def ask_ai(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ----------------------------
# LOGIC ENGINE (Deterministic)
# ----------------------------

def extract_metrics(log_text):
    """
    Very basic extraction:
    Example log:
    'Today I worked 3 hours but got distracted twice.'
    """

    hours_match = re.search(r'(\d+)\s*hour', log_text.lower())
    distraction_match = re.search(r'(\d+)\s*(distraction|times|time)', log_text.lower())

    hours = int(hours_match.group(1)) if hours_match else 1
    distractions = int(distraction_match.group(1)) if distraction_match else 0

    return hours, distractions


def compute_score(hours, distractions):
    distraction_ratio = distractions / max(hours, 1)

    if distraction_ratio == 0:
        score = 5
        discipline_level = "elite"
        performance_flag = "excellent"
    elif distraction_ratio < 0.3:
        score = 4
        discipline_level = "good"
        performance_flag = "stable"
    elif distraction_ratio < 0.6:
        score = 3
        discipline_level = "average"
        performance_flag = "warning"
    else:
        score = 2
        discipline_level = "low"
        performance_flag = "critical"

    strictness_mode = "high" if score <= 2 else "moderate"

    return score, distraction_ratio, discipline_level, performance_flag, strictness_mode


# ----------------------------
# CORE DISCIPLINE ENGINE
# ----------------------------

def generate_reinforcement():

    identity = get_latest_identity()
    log = get_latest_log()

    if not identity:
        return {"error": "No identity profile found."}

    if not log:
        return {"error": "No daily reflection found."}

    wake_time, non_negotiables, ideal_self = identity
    log_text = log[0]

    # Step 1: Extract metrics
    hours, distractions = extract_metrics(log_text)

    # Step 2: Compute deterministic score
    score, ratio, level, flag, strictness = compute_score(hours, distractions)

    # Step 3: Ask Ollama only for correction tone
    prompt = f"""
You are a strict Personal Discipline AI.

User Identity:
- Target Wake Time: {wake_time}
- Non-Negotiables: {non_negotiables}
- Ideal Self: {ideal_self}

Performance Metrics:
- Hours Worked: {hours}
- Distractions: {distractions}
- Score: {score}
- Discipline Level: {level}
- Performance Flag: {flag}

Generate:

1. A short correction statement.
2. One clear corrective instruction.

Respond ONLY in JSON format:

{{
  "correction": "...",
  "instruction": "..."
}}
"""

    raw_output = ask_ai(prompt)

    try:
        parsed = json.loads(raw_output)
    except:
        return {
            "error": "Invalid JSON from model.",
            "raw_output": raw_output
        }

    structured_result = {
        "score": score,
        "distraction_ratio": ratio,
        "discipline_level": level,
        "performance_flag": flag,
        "strictness_mode": strictness,
        "correction": parsed["correction"],
        "instruction": parsed["instruction"]
    }

    # Save FULL structured result
    save_reinforcement(json.dumps(structured_result))

    return structured_result


if __name__ == "__main__":
    result = generate_reinforcement()
    print(result)