import os
import json
from openai import OpenAI

# Set your OpenRouter API key (optional if already in environment)
os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI(base_url="https://openrouter.ai/api/v1")

HISTORY_FILE = "debug_history.json"

def save_history(buggy_code, error_message, explanation, fixed_code):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)

    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    entry = {
        "buggy_code": buggy_code,
        "error_message": error_message,
        "explanation": explanation,
        "fixed_code": fixed_code
    }

    history.append(entry)

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def debug_code(buggy_code, error_message):
    try:
        prompt = (
            f"I have this buggy Python code:\n\n{buggy_code}\n\n"
            f"And this is the error I am getting:\n\n{error_message}\n\n"
            "Please analyze the code, find the root cause, explain it step-by-step clearly, "
            "and provide the corrected code with explanation."
        )

        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are an expert AI code debugger."},
                {"role": "user", "content": prompt}
            ]
        )

        explanation_and_fix = response.choices[0].message.content.strip()
        return explanation_and_fix

    except Exception as e:
        print(f"Error during debugging: {e}")
        return "Error generating debug analysis."

def main():
    print("\n=== 🐞 AI Code Debugger CLI ===\n")

    buggy_code = input("Paste your buggy code:\n")
    print()
    error_message = input("Paste the error message you are getting:\n")

    print("\n🔍 Analyzing your code, please wait...\n")

    explanation_and_fix = debug_code(buggy_code, error_message)

    print("\n✅ Here is the analysis and fix:\n")
    print(explanation_and_fix)

    save_history(buggy_code, error_message, explanation_and_fix, explanation_and_fix)

    print("\n📝 Debug session saved to debug_history.json.")

if __name__ == "__main__":
    main()
