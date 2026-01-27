from fastapi import APIRouter, Form
from twilio.twiml.messaging_response import MessagingResponse
from app.api.chat import chat  # reuse existing chat logic

router = APIRouter()

@router.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),  # sender phone number
    Body: str = Form(...)    # message text
):
    """
    Twilio webhook to receive WhatsApp messages
    """
    # session_id = user phone number
    payload = {"message": Body, "session_id": From}
    
    # Use existing chat function
    response = await chat(payload)
    
    # Build Twilio response
    twilio_resp = MessagingResponse()
    twilio_resp.message(response["response"])
    
    return str(twilio_resp)
