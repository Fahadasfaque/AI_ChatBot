# backend/entity.py
"""
Purpose:
    This file handles Entity Extraction for our Loan Origination System chatbot.
    It identifies and extracts specific pieces of structured data (like names,
    PAN, Aadhaar, loan amount, monthly income, employment type, loan type,
    application ID, phone, email, occupation, employer, tenure, and property value)
    from user messages.

Why this file exists:
    Entities provide the specific parameters needed to evaluate loan applications
    and process requests. For example, to check eligibility, we need the applicant's
    monthly income and requested loan amount.

How it works:
    We use Python's built-in `re` (Regular Expressions) module to match specific
    alphanumeric and lexical patterns in the user's message.
"""

import re

# Pre-defined list of loan types
LOAN_TYPE_ENTITIES = {"home", "personal", "vehicle", "car", "education", "student", "business", "gold"}

# Pre-defined list of employment types
EMPLOYMENT_TYPES = {"salaried", "self-employed", "business owner", "student"}

# Pre-defined list of common occupations
OCCUPATION_ENTITIES = {
    "software engineer", "engineer", "doctor", "teacher", "manager", 
    "officer", "clerk", "consultant", "accountant", "lawyer", "student", 
    "mechanic", "nurse", "proprietor"
}

def extract_entities(message: str) -> dict:
    """
    Why it exists:
        Scans a user message and extracts all recognized loan-related entities.
        Returns a dictionary containing only the detected entities.
    """
    print(f"      ▶ [entity.py:extract_entities] Called with message={message!r}")
    detected = {}
    message_lower = message.lower()

    # 1. Extract Email Address
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    email_match = re.search(email_pattern, message)
    if email_match:
        detected["email"] = email_match.group(0)
        print(f"        - Extracted Email: {detected['email']!r}")

    # 2. Extract Phone Number
    phone_pattern = r"\b\d{10}\b"
    phone_match = re.search(phone_pattern, message)
    if phone_match:
        detected["phone_number"] = phone_match.group(0)
        detected["phone"] = phone_match.group(0)  # Compatibility
        print(f"        - Extracted Phone: {detected['phone']!r}")

    # 3. Extract PAN Card
    pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b"
    pan_match = re.search(pan_pattern, message)  # Check in original message case
    if not pan_match:
        pan_match = re.search(pan_pattern, message.upper())
    if pan_match:
        detected["pan_number"] = pan_match.group(0).upper()
        print(f"        - Extracted PAN: {detected['pan_number']!r}")

    # 4. Extract Aadhaar Card
    aadhaar_pattern = r"\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b"
    aadhaar_match = re.search(aadhaar_pattern, message)
    if aadhaar_match:
        raw_aadhaar = aadhaar_match.group(0)
        detected["aadhaar_number"] = raw_aadhaar.replace(" ", "")
        print(f"        - Extracted Aadhaar: {detected['aadhaar_number']!r}")

    # 5. Extract Application ID
    app_id_pattern = r"\bapp-\d{6}\b"
    app_id_match = re.search(app_id_pattern, message_lower)
    if app_id_match:
        detected["application_id"] = app_id_match.group(0).upper()
        print(f"        - Extracted Application ID: {detected['application_id']!r}")

    # 6. Extract Monthly Income
    income_pattern = r"(?:monthly\s+)?(income|salary|earnings)(?:\s+is|\s+of)?\s*(?:₹)?\s*(\b\d{4,8}\b)"
    income_match = re.search(income_pattern, message_lower)
    if income_match:
        detected["monthly_income"] = income_match.group(2)
        print(f"        - Extracted Monthly Income: {detected['monthly_income']!r}")

    # 7. Extract Property Value
    property_pattern = r"property\s+(?:worth|value)(?:\s+is)?\s*(?:₹)?\s*(\b\d{5,8}\b)"
    property_match = re.search(property_pattern, message_lower)
    if property_match:
        detected["property_value"] = property_match.group(1)
        print(f"        - Extracted Property Value: {detected['property_value']!r}")

    # 8. Extract Loan Amount
    # Match amounts with ₹ symbol or standalone numbers between 4 and 8 digits
    # Avoid overlapping with phone numbers, aadhaar numbers, income, or property value
    amount_matches = re.findall(r"₹\s*(\d+)|\b\d{4,8}\b", message)
    extracted_amount = None
    for amt in amount_matches:
        val_str = amt if isinstance(amt, str) else (amt[0] or amt[1])
        if not val_str:
            continue
        if phone_match and val_str in phone_match.group(0):
            continue
        if aadhaar_match and val_str in aadhaar_match.group(0):
            continue
        if income_match and val_str == income_match.group(2):
            continue
        if property_match and val_str == property_match.group(1):
            continue
        extracted_amount = f"₹{val_str}"
        break
    
    if extracted_amount:
        detected["loan_amount"] = extracted_amount
        detected["amount"] = extracted_amount  # Compatibility
        print(f"        - Extracted Loan Amount: {detected['loan_amount']!r}")

    # 9. Extract Loan Type
    found_loans = []
    for loan in LOAN_TYPE_ENTITIES:
        loan_pattern = r"\b" + re.escape(loan) + r"\b"
        if re.search(loan_pattern, message_lower):
            found_loans.append(loan)
            
    if found_loans:
        detected["loan_type"] = ", ".join(found_loans).capitalize()
        detected["product"] = detected["loan_type"]  # Compatibility
        print(f"        - Extracted Loan Type: {detected['loan_type']!r}")

    # 10. Extract Employment Type
    for emp in EMPLOYMENT_TYPES:
        emp_pattern = r"\b" + re.escape(emp) + r"\b"
        if re.search(emp_pattern, message_lower):
            detected["employment_type"] = emp.capitalize()
            print(f"        - Extracted Employment Type: {detected['employment_type']!r}")
            break

    # 11. Extract Occupation
    for occ in OCCUPATION_ENTITIES:
        occ_pattern = r"\b" + re.escape(occ) + r"\b"
        if re.search(occ_pattern, message_lower):
            detected["occupation"] = occ.capitalize()
            print(f"        - Extracted Occupation: {detected['occupation']!r}")
            break

    # 12. Extract Employer Name
    employer_pattern = r"(?:working\s+at|employed\s+by|employer\s+is)\s+([a-zA-Z0-9\s]{2,20})\b"
    employer_match = re.search(employer_pattern, message)  # Check original case
    if employer_match:
        detected["employer_name"] = employer_match.group(1).strip()
        print(f"        - Extracted Employer Name: {detected['employer_name']!r}")

    # 13. Extract Loan Tenure
    tenure_pattern = r"\b\d+\s*(?:years|months|yr|mo|yrs|mths)\b"
    tenure_match = re.search(tenure_pattern, message_lower)
    if tenure_match:
        detected["loan_tenure"] = tenure_match.group(0)
        print(f"        - Extracted Loan Tenure: {detected['loan_tenure']!r}")

    # 14. Extract Applicant Name
    name_pattern = r"\bmy name is\s+([a-zA-Z]+)\b"
    name_match = re.search(name_pattern, message_lower)
    if name_match:
        start_idx = name_match.start(1)
        end_idx = name_match.end(1)
        detected["applicant_name"] = message[start_idx:end_idx]
        detected["name"] = detected["applicant_name"]  # Compatibility
        print(f"        - Extracted Applicant Name: {detected['applicant_name']!r}")

    print(f"      ◀ [entity.py:extract_entities] Returning: {detected}")
    return detected
