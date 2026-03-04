import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(question: str, context: str = "") -> str:
    """Send a question to Groq and return the response."""

    if context:
        prompt = f"""You are a helpful coding assistant.

Here is the codebase context:
{context}

Question: {question}

Answer clearly and concisely."""
    else:
        prompt = question

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content