import requests
import openai
import yaml

with open("config/settings.yaml", "r") as f:
    settings = yaml.safe_load(f)

MODE = settings["llm"]["mode"]
LOCAL_MODEL = settings["llm"]["local_model"]
OLLAMA_URL = settings.get("llm", {}).get("ollama_url", "http://localhost:11434")


def call_ollama(prompt: str) -> str:
    try:
        url = f"{OLLAMA_URL}/api/chat"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": LOCAL_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }

        response = requests.post(url, json=data, headers=headers, stream=True)
        response.raise_for_status()

        full_output = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = line.decode("utf-8").removeprefix("data: ").strip()
                    if chunk == "[DONE]":
                        break
                    import json
                    content = json.loads(chunk)
                    token = content.get("message", {}).get("content", "")
                    print(token, end="", flush=True)
                    full_output += token
                except Exception as e:
                    print(f"[Stream Error] {e}")


        print()
        return full_output
    
    except Exception as e:
        return f"Error: Ollama failed: {e}"
    
def call_openai(prompt: str) -> str:
    try:
        openai.api_key = "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"
        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )    
        return res.choices[0].message.content
    except Exception as e:
        return f"Error:OpenAI failed: {e}"
    
def query_llm(prompt: str) -> str:
    if MODE == "local_model":
        return call_ollama(prompt)
    elif MODE == "openai":
        return call_openai(prompt)
    else:
        return "Error: Invalid llm mode in config"