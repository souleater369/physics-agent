import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI(title="The Deep Orchestrator")

# Initialize the Gemini Engine
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

class ResearchQuery(BaseModel):
    history: list[dict]
    query: str

# --- File Serving Routes ---
@app.get("/")
def serve_html():
    return FileResponse("index.html")

@app.get("/style.css")
def serve_css():
    return FileResponse("style.css")

@app.get("/script.js")
def serve_js():
    return FileResponse("script.js")

# --- AI Engine Route ---
@app.post("/research")
def conduct_research(payload: ResearchQuery):
    if not client:
        raise HTTPException(status_code=500, detail="API Key missing.")
        
    try:
        # Format conversation memory
        formatted_history = [
            types.Content(role=msg["role"], parts=[types.Part.from_text(text=msg["content"])])
            for msg in payload.history
        ]
        formatted_history.append(
            types.Content(role="user", parts=[types.Part.from_text(text=payload.query)])
        )

        instruction = """
        You are an elite, highly analytical deep-research agent. 
        1. Always use your Google Search tool to verify claims, find recent academic papers, or check current product specifications.
        2. When asked to compare items, products, or concepts, ALWAYS format your response as a detailed Markdown table.
        3. Be concise, objective, and cite your findings naturally.
        """
        
        def stream_generator():
            try:
                response_stream = client.models.generate_content_stream(
                    model='gemini-2.5-flash',
                    contents=formatted_history,
                    config=types.GenerateContentConfig(
                        system_instruction=instruction,
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=0.3
                    )
                )
                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text
            except Exception as stream_err:
                yield f"\n\n**SYSTEM CRASH LOG:** `{str(stream_err)}`"

        # The X-Accel-Buffering header prevents Codespaces from pausing the stream
        return StreamingResponse(
            stream_generator(), 
            media_type="text/plain",
            headers={
                "X-Accel-Buffering": "no",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine Error: {str(e)}")