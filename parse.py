from openai import OpenAI
from dotenv import load_dotenv

import os
import json

# ---------------- LOAD ENV ----------------

load_dotenv()

# ---------------- OPENROUTER CLIENT ----------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# ---------------- PROMPT TEMPLATE ----------------

template = """
You are an intelligent AI website analyzer.

Analyze the website content carefully.

Generate:

1. A short website summary in EXACTLY 3 lines
2. Exactly 10 important questions with answers
3. Important keywords grouped into categories

WEBSITE CONTENT:
{dom_content}

RETURN ONLY VALID JSON.

FORMAT:

{{
    "website_summary": [
        "Line 1",
        "Line 2",
        "Line 3"
    ],

    "questions_answers": [
        {{
            "question": "Question here",
            "answer": "Answer here"
        }}
    ],

    "keywords": {{
        "business": [],
        "technology": [],
        "features": [],
        "audience": [],
        "knowledge": []
    }}
}}

RULES:
- Return ONLY JSON
- No markdown
- No explanations
- No extra text
"""

# ---------------- AI FUNCTION ----------------

def generate_qa_from_content(dom_content):

    try:

        shortened_content = dom_content[:12000]

        prompt = template.format(
            dom_content=shortened_content
        )

        completion = client.chat.completions.create(
            model=os.getenv("AI_MODEL"),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        response = completion.choices[0].message.content

        # ---------------- CLEAN RESPONSE ----------------

        response = clean_json_response(response)

        # ---------------- VALIDATE JSON ----------------

        parsed_json = json.loads(response)

        # Ensure correct structure
        if isinstance(parsed_json, list):

            parsed_json = {
                "questions_answers": parsed_json,
                "keywords": {
                    "business": [],
                    "technology": [],
                    "features": [],
                    "audience": [],
                    "knowledge": []
                }
            }

        return json.dumps(parsed_json)

    except Exception as e:

        print(f"AI Error: {e}")

        return json.dumps({
            "questions_answers": [],
            "keywords": {
                "business": [],
                "technology": [],
                "features": [],
                "audience": [],
                "knowledge": []
            }
        })
        
def clean_json_response(response):

    response = response.strip()

    response = response.replace(
        "```json",
        ""
    )

    response = response.replace(
        "```",
        ""
    )

    return response.strip()