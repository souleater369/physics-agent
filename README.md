# 🌊 The Deep Orchestrator

A sophisticated, streaming cognitive research agent built for the Microsoft Agents League Hackathon (Creative Apps Track).

## 🚀 The Concept
Standard AI agents provide static summaries. The Deep Orchestrator acts as a live research pipeline. Users input complex queries, and the agent autonomously searches the live internet (academic databases, patents, articles), synthesizes the data, and streams the analysis—complete with formatted comparative matrices—directly to a Warm Soft Minimalist UI.

## ⚙️ The Architecture
To ensure zero latency and bypass environment timeout limits, the application is built on a custom streaming architecture:
* **Backend (`main.py`):** FastAPI Python server routing Google Gemini 2.5 Flash. Utilizes `generate_content_stream` and `X-Accel-Buffering` overrides to guarantee real-time token delivery.
* **AI Tooling:** Native integration of the `GoogleSearch()` tool for live web grounding and hallucination reduction.
* **Frontend (`index.html` & `style.css`):** A custom HTML/JS interface styled with Tailwind CSS, focusing on high white-space, monochromatic palettes, and organic shapes to reduce cognitive load.
* **Data Parsing (`script.js`):** Client-side stream decoding combined with `marked.js` to render complex markdown tables and research data in real-time.

## 🛠️ How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install fastapi uvicorn google-genai pydantic`
3. Export your API Key: `export GEMINI_API_KEY="your_api_key"`
4. Boot the server: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Open the local port in your browser.

---
*Built by Arna*