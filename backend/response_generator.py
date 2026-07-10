# backend/response_generator.py
"""
Purpose:
    This file handles Response Generation for our chatbot. It takes the outputs
    from Intent Detection, Entity Extraction, and Context Processing, and compiles
    the final user-facing text response.

Why this file exists:
    By separating response generation into its own module, we decouple the chatbot's
    coordination logic (chatbot.py) from the specific formatting, templates, and
    fallbacks used to construct the final message.
"""

def generate_response(
    intent_name: str,
    intent_reply: str,
    entities: dict,
    context_reply: str | None,
    kb_reply: str | None
) -> tuple[str, str]:
    """
    Why it exists:
        Compiles the final chatbot response using rules based on intent,
        entities, context answers, and knowledge base replies.
    """
    print(f"      ▶ [response_generator.py:generate_response] Called with intent_name={intent_name!r}, entities={entities!r}, context_reply={context_reply!r}, kb_reply={kb_reply!r}")
    
    if context_reply is not None:
        response_text = context_reply
        intent_name = "context"
        print(f"        - Using context response. Updated intent_name to 'context'.")
    elif kb_reply is not None:
        response_text = kb_reply
        print(f"        - Using knowledge base response.")
    else:
        # Compile standard response based on detected intent and entities
        if intent_name == "UNKNOWN":
            if entities:
                # Conversational fallback: Check if the user is asking about a loan
                loan_type = entities.get("loan_type") or entities.get("product")
                amount = entities.get("loan_amount") or entities.get("amount")
                income = entities.get("monthly_income")
                
                if loan_type and "loan" in loan_type.lower():
                    response_text = "I noticed you are asking about a loan. Could you please specify what type of loan (such as Home, Car, Personal, Education, or Gold Loan) you are looking for?"
                elif amount:
                    response_text = f"I see you mentioned an amount of {amount}. Could you please clarify which type of loan or inquiry this relates to?"
                elif income:
                    response_text = f"I noted your monthly income is ₹{income}. Could you please tell me which loan product you are interested in?"
                else:
                    response_text = "I noticed some details in your message, but I couldn't understand your request. Could you please ask a question about our loan products, eligibility, or EMI?"
                print("        - Intent is UNKNOWN but entities extracted. Using conversational fallback.")
            else:
                response_text = intent_reply
                print("        - Intent is UNKNOWN and no entities. Using default fallback response.")
        else:
            response_text = intent_reply
            print(f"        - Intent matched: {intent_name!r}. Using standard response.")

    print(f"      ◀ [response_generator.py:generate_response] Returning: (response_text={response_text!r}, intent_name={intent_name!r})")
    return response_text, intent_name
