from cmath import e
import requests
import yaml
import json
import os
from groq import Groq # type: ignore


with open("config/settings.yaml", "r") as f:
    settings = yaml.safe_load(f)

MODE = settings["llm"]["mode"]
LOCAL_MODEL = settings["llm"]["local_model"]
OLLAMA_URL = settings["llm"].get("ollama_url","http://localhost:11434")
GROQ_API_KEY = settings["llm"].get("groq_api_key")
GROQ_MODEL = settings["llm"].get("groq_model", "llama3-70b-8192")

client = Groq(api_key=GROQ_API_KEY)

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
   
def call_groq(prompt: str, stream: bool = True) -> str:
    response_text = ""

    if stream:
        try:
            stream_response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in stream_response:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        print(delta.content, end="", flush=True)
                        response_text += delta.content
            return response_text
        except Exception as e:
            print(f"\n[Streaming error] {e}")
            return ""

    else:
        try:
            res = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=False,
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f"[Non-streaming error] {e}")
            return ""
   
def query_llm(prompt: str) -> str:
    if MODE == "local_model":
        return call_ollama(prompt)
    elif MODE == "groq":
        return call_groq(prompt)
    else:
         return "Error: Invalid llm mode in config"
       

