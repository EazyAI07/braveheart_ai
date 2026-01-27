from fastapi import APIRouter
import openai
import os

from app.core.language import detect_language
from app.core.safety import detect_crisis, crisis_response
from app.core.prompts import system_prompt, user_prompt
from app.rag.retriever import retrieve_context
from app.core.config import CHAT_MODEL
from app.utils.logger import log_event
from app.core.memory import get_session, update_session

openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()


@router.post("/chat")
async def chat(payload: dict):
    user_input = payload.get("message", "")
    session_id = payload.get("session_id", "anon")

    log_event("Incoming chat request")

    # Input validation
    if not user_input or len(user_input.strip()) < 3:
        return {"response": "Please ask a complete question so I can try to help.", "crisis": False}

    # Language detection
    language = detect_language(user_input)

    # Crisis detection
    if detect_crisis(user_input):
        log_event("Crisis detected")
        return {"response": crisis_response(language), "crisis": True}

    # Retrieve session history
    history = get_session(session_id)

    # Retrieve RAG context
    context = retrieve_context(user_input)

    # Merge memory + RAG context
    if history:
        history_text = "\n".join(f"User: {h['user']}\nBHat: {h['bot']}" for h in history)
        context = history_text + "\n\n" + context

    # Build messages
    messages = [
        {"role": "system", "content": system_prompt(language)},
        {"role": "user", "content": user_prompt(context, user_input)}
    ]

    # Call OpenAI
    completion = openai.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.3
    )

    response_text = completion.choices[0].message.content

    # Safety disclaimer for UI only
    footer = (
        "\n\n—\n"
        "⚠️ I’m not a medical professional. "
        "If substance use is causing harm, consider seeking help "
        "from a qualified health provider."
    )
    final_response = response_text

    # Update session memory (clean, without disclaimer)
    update_session(session_id, user_input, response_text)

    return {"response": final_response, "crisis": False}
