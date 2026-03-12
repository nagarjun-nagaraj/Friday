import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(question: str, context: str = "", history: list = None) -> tuple:
    """Send a question to Groq with chat history and return the response + updated history."""
    if history is None:
        history = []

    # Build the user message
    if context:
        user_message = f"""Here is the codebase context:
{context}

Question: {question}

Answer clearly and concisely."""
    else:
        user_message = question

    # Append new user turn to history
    messages = [
        {"role": "system", "content": "You are Friday, a helpful coding assistant."}
    ] + history + [
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        reply = response.choices[0].message.content

        # Save clean question to history, not the context-stuffed prompt
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
            return "✗ Model not found — the AI model name may have changed.", history
        else:
            return f"✗ Something went wrong: {error}", history