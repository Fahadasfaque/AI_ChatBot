# backend/run_verification.py
import sys
from chatbot import get_bot_response
from context import get_session, sessions

def print_separator(title):
    print("\n" + "=" * 80)
    print(f" {title.upper()} ".center(80, "="))
    print("=" * 80)

def run_test_query(query: str, user_id: str = "default_user"):
    print(f"\nUser: {query}")
    reply, detected_type, score = get_bot_response(query, user_id=user_id)
    print(f"Bot:   {reply}")
    print(f"       [Type: {detected_type} | Score: {score}]")
    return reply, detected_type, score

def main():
    print_separator("Testing Single-Turn Scenarios")
    
    # 1. Greeting
    run_test_query("hello")
    
    # 2. Spelling correction / typos
    run_test_query("good morinnig")
    run_test_query("what is the coost of vehicle loan?") # should trigger interest rates / cost search
    
    # 3. FastPath (Direct application status)
    run_test_query("status APP-987654")
    
    # 4. Intent detection (Direct keyword)
    reply, intent, score = run_test_query("apply loan")
    assert intent == "loan_application", f"Expected intent loan_application, got {intent}"
    
    # 5. Intent Synonym Expansion tests
    print_separator("Verifying Intent Synonym Expansion")
    _, intent, _ = run_test_query("tell me about loans")
    assert intent == "loan_products", f"Expected loan_products for synonym, got {intent}"
    
    _, intent, _ = run_test_query("what is the repo rate?")
    assert intent == "interest_rates", f"Expected interest_rates for synonym, got {intent}"
    
    _, intent, _ = run_test_query("what is the minimum cibil score?")
    assert intent == "loan_eligibility", f"Expected loan_eligibility for synonym, got {intent}"
    
    _, intent, _ = run_test_query("proof of salary")
    assert intent == "required_documents", f"Expected required_documents for synonym, got {intent}"
    
    _, intent, _ = run_test_query("customer care helpline")
    assert intent == "customer_support", f"Expected customer_support for synonym, got {intent}"
    
    # 6. Knowledge Base Jaccard Search & Ranking (Exact vs Loose)
    print_separator("Verifying Jaccard Search Ranking (Exact vs Loose)")
    reply, intent, score = run_test_query("about company")
    assert score == 100.0, f"Expected 100% score for exact match, got {score}"
    assert "ABC Lending was established" in reply
    
    reply, intent, score = run_test_query("company name")
    assert score == 100.0, f"Expected 100% score for exact match, got {score}"
    assert "ABC Lending Solutions Private Limited" in reply

    # 7. Gibberish check
    run_test_query("asdfghjklqwerty")

    print_separator("Testing Multi-Turn Loan Application Flow")
    user_id = "test_applicant_1"
    
    # Clean session
    if user_id in sessions:
        del sessions[user_id]
        
    run_test_query("My name is Rajesh Kumar", user_id=user_id)
    run_test_query("I want to apply for a Home Loan", user_id=user_id)
    run_test_query("My monthly income is 75000", user_id=user_id)
    run_test_query("I need a loan amount of 5000000", user_id=user_id)
    run_test_query("I am salaried and working at Microsoft", user_id=user_id)
    
    print_separator("Verifying Session Memory (Context queries bypass KB)")
    reply, intent, score = run_test_query("What is my name?", user_id=user_id)
    assert intent == "context", f"Expected intent 'context' for context retrieval, got {intent}"
    assert score is None, f"Expected score to be None (bypassing KB), got {score}"
    
    reply, intent, score = run_test_query("What is my monthly income?", user_id=user_id)
    assert intent == "context", f"Expected intent 'context', got {intent}"
    assert score is None, f"Expected score to be None, got {score}"
    
    reply, intent, score = run_test_query("What is my employment type?", user_id=user_id)
    assert intent == "context", f"Expected intent 'context', got {intent}"
    assert score is None, f"Expected score to be None, got {score}"
    
    reply, intent, score = run_test_query("What loan did I select?", user_id=user_id)
    assert intent == "context", f"Expected intent 'context', got {intent}"
    assert score is None, f"Expected score to be None, got {score}"
    
    print_separator("Verifying Conversation History Retrieval")
    run_test_query("Tell me the last 5 conversations", user_id=user_id)

    print_separator("Validation Completed Successfully")

if __name__ == "__main__":
    main()
