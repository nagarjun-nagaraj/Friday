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

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        error = str(e)
        if "429" in error:
            return "✗ Rate limit hit — too many requests. Wait a minute and try again."
        elif "401" in error or "403" in error:
            return "✗ Invalid API key — check your GROQ_API_KEY in .env"
        elif "404" in error:
            return "✗ Model not found — the AI model name may have changed."
        else:
            return f"✗ Something went wrong: {error}"