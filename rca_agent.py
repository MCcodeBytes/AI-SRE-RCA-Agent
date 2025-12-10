import ollama
import json
from pydantic import BaseModel, Field

# --- CONFIGURATION ---
MODEL = "llama3.2"
INPUT_FILE = "sample_data/incident_log.txt"

# --- 1. DEFINE THE STRUCTURE ---
# This ensures every run produces the exact same fields, making it measureable.
class RootCauseAnalysis(BaseModel):
    title: str = Field(description="A short, professional title for the incident.")
    severity: str = Field(description="Estimated severity (Low, Medium, High, Critical).")
    summary: str = Field(description="A 2-sentence executive summary of what happened.")
    root_cause: str = Field(description="The technical reason for the failure (e.g., Deadlock, Timeout).")
    evidence: list[str] = Field(description="A list of specific lines from the log that prove the root cause.")
    remediation: list[str] = Field(description="Recommended steps to fix the issue.")

# Get the JSON schema to pass to the model
schema_json = RootCauseAnalysis.model_json_schema()

# --- 2. THE SYSTEM PROMPT (SRE Persona) ---
system_prompt = f"""
You are a Principal Site Reliability Engineer. Analyze the input log and generate a Root Cause Analysis report.

CRITICAL INSTRUCTION:
Output valid JSON only. 
Do NOT return the schema definition. 
Do NOT use the key "properties". 
You must output a single JSON object where the keys are the field names (title, severity, summary, root_cause, evidence, remediation) and the values are the analysis from the log.

Target JSON Structure:
{json.dumps(schema_json)}
"""

def analyze_log(file_path):
    print(f"READING LOG: {file_path}...")
    try:
        with open(file_path, 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Could not find file {file_path}")
        return

    print(f"ANALYZING LOCALLY with {MODEL}...")
    
    response = ollama.chat(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f"Here is the log data:\n\n{log_content}"},
        ],
        format='json', 
        options={'temperature': 0.1} # Lower temperature = more deterministic/strict
    )

    content = response['message']['content']


    try:
        # Validate that the AI followed our Pydantic structure
        rca = RootCauseAnalysis.model_validate_json(content)
        return rca
    except Exception as e:
        print(f"\n JSON VALIDATION ERROR: {e}")
        print(f"Raw Output received from LLM:\n{content}")
        return None

if __name__ == "__main__":
    result = analyze_log(INPUT_FILE)
    
    if result:
        print("\n SUCCESS! Generated RCA Report:")
        print("-" * 40)
        # Using model_dump_json gives us the clean final JSON string
        print(result.model_dump_json(indent=2))
        print("-" * 40)


