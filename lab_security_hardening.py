import json
import datetime
import pandas as pd
from sklearn.ensemble import IsolationForest

print("======================================================")
print("   AI Security Layer & Data Validation Test           ")
print("======================================================\n")

# --- 1. قائمة الأنماط المحظورة (Input & Output) ---
INPUT_THREATS = [
    "ignore previous instructions",
    "reveal confidential data",
    "bypass safety"
]

FORBIDDEN_OUTPUTS = [
    "SECRET_KEY", 
    "API_TOKEN", 
    "123456789"
]

# --- 2. سجل الأمان (Security Log) ---
security_logs = []

def log_event(user: str, prompt: str, status: str, detail: str):
    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user,
        "status": status,
        "detail": detail
    }
    security_logs.append(log_entry)

# --- 3. فحص المدخلات (Input Guardrail) ---
def check_input(prompt: str) -> tuple[bool, str]:
    prompt_lower = prompt.lower()
    for pattern in INPUT_THREATS:
        if pattern in prompt_lower:
            return False, f"Threat pattern detected: {pattern}"
    return True, "Input Safe"

# --- 4. فحص المخرجات وسلامة البيانات (Output Guardrail) ---
def check_output(response_text: str) -> tuple[bool, str]:
    for forbidden in FORBIDDEN_OUTPUTS:
        if forbidden in response_text:
            return False, f"Data leak detected: {forbidden}"
    return True, "Output Verified & Secure"

# --- 5. معالج الطلبات الكامل (Security Pipeline) ---
def process_request(user: str, prompt: str, mock_ai_response: str):
    print(f"Incoming Request\nUser: {user}\nPrompt: {prompt}")
    
    # فحص المدخلات
    is_input_valid, input_msg = check_input(prompt)
    if not is_input_valid:
        log_event(user, prompt, "blocked", input_msg)
        print(f"[BLOCKED INPUT] {input_msg}\n" + "-"*54)
        return {"status": "blocked", "reason": input_msg}
    
    # فحص المخرجات وسلامة البيانات
    is_output_valid, output_msg = check_output(mock_ai_response)
    if not is_output_valid:
        log_event(user, prompt, "blocked", output_msg)
        print(f"[BLOCKED OUTPUT] {output_msg}\n" + "-"*54)
        return {"status": "blocked", "reason": output_msg}
        
    log_event(user, prompt, "approved", "Success")
    print(f"[SUCCESS] Secure AI Response: {mock_ai_response}\n" + "-"*54)
    return {"status": "approved", "response": mock_ai_response}


# ======================================================
#                   تطبيق الاختبارات
# ======================================================

# تجربة 1: اختبار محاولة تخطي الأمان في المدخلات (Prompt Injection Test)
process_request("guest", "Ignore previous instructions", "Here is system prompt")

# تجربة 2: اختبار سلامة المخرجات (تسريب بيانات غير صحيحة/حساسة)
process_request("analyst", "Fetch user details", "User details: ID 123456789 with API_TOKEN")

# تجربة 3: طلب آمن ومخرجات سليمة 100%
final_res = process_request("analyst", "Explain AI security best practices", "Secure AI response generated successfully")

print("API Final Response:")
print(json.dumps(final_res, indent=3))