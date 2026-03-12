import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DEFAULT_MODEL = "llama-3.3-70b-versatile"

def ask_ai(question: str, context: str = "", history: list = None, model: str = DEFAULT_MODEL) -> tuple:
    """Send a question to Groq with chat history and return the response + updated history."""
    if history is None:
        history = []

    if context:
        user_message = f"""Here is the codebase context:
{context}

Question: {question}

Answer clearly and concisely."""
    else:
        user_message = question

    messages = [
        {"role": "system", "content": "You are Friday, a helpful coding assistant."}
    ] + history + [
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        reply = response.choices[0].message.content

        updated_history = history + [
            {"role": "user", "content": question},
            {"role": "assistant", "content": reply}
        ]
        return reply, updated_history

    except Exception as e:
        error = str(e)
        if "429" in error:
            return "✗ Rate limit hit — too many requests. Wait a minute and try again.", history
        elif "401" in error or "403" in error:
            return "✗ Invalid API key — check your GROQ_API_KEY in .env", history
        elif "404" in error:
            return "✗ Model not found — run 'friday models' to see available options.", history
        else:
            return f"✗ Something went wrong: {error}", history