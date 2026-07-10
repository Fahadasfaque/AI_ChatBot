# backend/intent.py
import random

"""
Purpose:
    This file handles Intent Detection for our chatbot. It maps the user's
    message to predefined categories (intents) such as Pricing, Support, Contact,
    Password Reset, or Product Information using simple keyword matching.

Why this file exists:
    In conversational AI, "Intent" represents what the user wants to achieve.
    This file enables the chatbot to categorize user requests and deliver
    specific, helpful answers instead of just echoing the user's message.

How it works:
    1. We define dictionary mapping intents to list of keywords.
    2. We convert the user's message to lowercase.
    3. We check if any of the keywords for an intent exist in the user's message.
    4. If a match is found, we return the intent name and its hardcoded response.
    5. If no keywords match, we return the intent "UNKNOWN" with a fallback response.

Input:
    A string (the user's text message).

Output:
    A tuple of (intent_name: str, response_text: str).
"""

# Dictionary mapping each intent category to its list of matching keywords (ordered by specificity/priority)
INTENT_KEYWORDS = {
    "loan_products": ["loan product", "loan products", "type of loan", "types of loans", "what loans", "product details", "loan types", "loan offering", "loan offerings", "tell me about loans", "tell me about loan", "explain loans", "loan catalog"],
    "loan_eligibility": ["eligibility", "eligible", "criteria", "qualify", "qualification", "cibil", "credit score", "credit rating", "cibil score", "minimum cibil", "credit check"],
    "required_documents": ["document", "documents", "doc", "docs", "paperwork", "proof of income", "salary slips", "pan card", "aadhaar card", "itr", "title deed", "papers", "proof", "kyc proof", "required papers", "address proof"],
    "interest_rates": ["interest rate", "interest rates", "rate of interest", "roi", "rates", "interest percentage", "interest charges", "repo", "repo rate", "eblr", "mclr", "floating rate", "fixed rate"],
    "emi": ["emi", "installment", "installments", "repayment", "monthly payment", "emi calculation", "emi calculator"],
    "loan_workflow": ["workflow", "process", "procedure", "how to apply", "application steps", "origination process", "sanction steps", "stages"],
    "application_status": ["status", "track", "progress", "application id", "app id", "application status", "check status"],
    "loan_application": ["apply for", "start application", "new application", "register loan", "apply loan", "loan form", "fill application", "apply", "register", "fill form", "want to apply", "how do i apply", "loan form"],
    "customer_support": ["support", "help", "contact", "email", "phone", "branch", "manager", "helpline", "toll free", "nodal officer", "customer care", "call center", "complaints", "support number"],
    "thank_you": ["thank you", "thanks", "thx", "appreciate it", "thankyou"]
}

# Dictionary mapping each intent category to its hardcoded answer
INTENT_RESPONSES = {
    "loan_products": "We offer Home Loans, Personal Loans, Vehicle Loans, Education Loans, and Business Loans.",
    "loan_eligibility": "To qualify for a loan, we evaluate your age, income, employment stability, and CIBIL score.",
    "required_documents": "The required documents typically include KYC (PAN/Aadhaar), income proof, and bank statements.",
    "interest_rates": "Our loan interest rates start from competitive market benchmarks.",
    "emi": "You can calculate your Equated Monthly Installment (EMI) based on your loan amount, interest rate, and tenure.",
    "loan_workflow": "The loan origination process includes Application, Verification, Credit Underwriting, Sanction, and Disbursement.",
    "application_status": "You can track your application status using your Application ID (e.g. APP-123456).",
    "loan_application": "To start your loan application, please provide your name, monthly income, employment type, and desired loan type.",
    "customer_support": "You can contact our loan support team at loansupport@abclending.com or call 1800-102-2233.",
    "thank_you": [
        "You are welcome. Please don't hesitate to reach out if you have further questions.",
        "Happy to help. Is there anything else I can assist you with today?",
        "Glad I could be of assistance. Have a great day.",
        "It was my pleasure to help."
    ],
    "UNKNOWN": [
        "I couldn't understand your request. Please ask your loan-related question again.",
        "I don't have information on that topic. Please ask about loan products, eligibility, EMI, or application status.",
        "I am unable to process that specific loan request. Can you provide more details?",
        "That topic is currently outside of my capabilities as a Loan Origination Assistant."
    ]
}

# =====================================================================
# detect_intent Function
# =====================================================================
def detect_intent(message: str) -> tuple[str, str]:
    """
    Why it exists:
        This is the main function of the module. It inspects the user message
        for keywords to classify their intent, then retrieves the corresponding
        pre-written response.

    What it receives:
        message (str): The text message submitted by the user.

    What it returns:
        tuple[str, str]: A tuple containing:
            1. The name of the matched intent (e.g. "pricing", "UNKNOWN").
            2. The hardcoded response text for that intent.
    """
    print(f"      ▶ [intent.py:detect_intent] Called with message={message!r}")
    # 1. Convert the user's message to lowercase to ensure case-insensitive matching
    cleaned_message = message.strip().lower()

    # 2. Iterate through each intent and its list of keywords
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            # If the keyword exists as a substring in the user's message, we match it
            if keyword in cleaned_message:
                # SPECIAL EXCEPTION: If intent is "customer_support" and keyword is "email" or "phone",
                # but the user is actually PROVIDING their email or phone number, do not match.
                if intent == "customer_support" and keyword == "email":
                    import re
                    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
                    if re.search(email_pattern, cleaned_message):
                        continue
                if intent == "customer_support" and keyword == "phone":
                    import re
                    phone_pattern = r"\b\d{10}\b"
                    if re.search(phone_pattern, cleaned_message):
                        continue

                response = INTENT_RESPONSES[intent]
                if isinstance(response, list):
                    response = random.choice(response)
                print(f"        - Matched Keyword: {keyword!r} -> Intent: {intent!r}")
                print(f"      ◀ [intent.py:detect_intent] Returning: (intent={intent!r}, response={response!r})")
                return intent, response

    # 3. Fallback: if no keywords matched, return UNKNOWN
    unknown_response = random.choice(INTENT_RESPONSES["UNKNOWN"])
    print("        - No keywords matched in message.")
    print(f"      ◀ [intent.py:detect_intent] Returning Fallback: (intent='UNKNOWN', response={unknown_response!r})")
    return "UNKNOWN", unknown_response
