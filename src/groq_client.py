import os
from groq import Groq


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not set.")

    return Groq(api_key=api_key)


def generate_answer(question, context):
    client = get_groq_client()

    prompt = f"""
You are WasteWise AI, a manufacturing waste intelligence assistant.

Answer the user's question using ONLY the provided SOP evidence.

If the evidence does not contain enough information to answer,
say that the SOP does not provide enough information.

SOP evidence:
{context}

User question:
{question}

Provide a concise, practical answer for a manufacturing supervisor.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a precise manufacturing waste intelligence assistant."
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content