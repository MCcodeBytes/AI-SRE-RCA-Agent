What is the AI Post-Mortem Agent?

The AI Post-Mortem Agent is a command-line tool designed for Site Reliability Engineers (SREs) who need to automate the manual, time-consuming process of drafting Root Cause Analysis (RCA) reports while maintaining strict data compliance.

This agent uses localized, open-source Large Language Models (LLMs) to synthesize unstructured incident logs into a clean, structured JSON format, eliminating the need to expose sensitive production data to external cloud-based LLM APIs (like GPT-4).

How It Works
The agent uses a simple, three-step pipeline:
1. The user inputs a raw log file (e.g., incident_log.txt).
2. The rca_agent.py script sends the log and a specialized SRE System Prompt to the local Llama 3 model via the Ollama API.
3. The model returns a validated, structured RootCauseAnalysis object in JSON format.

🤝 Contributing
Contributions are welcome! Whether you have ideas for new analysis features, want to integrate with other models (like Mixtral), or can provide diverse, anonymized log samples (network failures, Kubernetes errors), please open an issue or submit a pull request.
