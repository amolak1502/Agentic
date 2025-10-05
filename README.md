# Agentic Groq LLM with Video Transcription, Web Search, and Weather Tools

This project demonstrates an **agentic AI setup** using Groq LLM (`ChatGroq`) that can:

- Transcribe YouTube videos, Instagram reels, or shorts using **Supadata API**  
- Search the web to fact-check claims using **Tavily API**  
- Fetch weather information for a location using **Tavily API**  

The agent automatically selects the appropriate tool based on user queries.

---

## Requirements

Install the required Python packages:

```bash
pip install python-dotenv langchain-groq langgraph tavily supadata langchain
```
Create a `.env` file in the project root with the following keys:

GROQ_API_KEY=your_groq_api_key_here  
TAVILY_API_KEY=your_tavily_api_key_here  
SUPADATA_API_KEY=your_supadata_api_key_here  

---

## Usage

Run the main agent script:

python agentic_groq.py

The script will start an interactive console:

start convo with LLM  
USER INPUT:

Type your queries (e.g., video URLs, weather questions, or factual claims).  
Type `exit` to quit.

### Example Queries

- transcribe this video https://www.youtube.com/watch?v=...  
- Is it true that leeches are common in the Western Ghats?  
- What is the weather in Mumbai?

The agent will automatically decide which tool to use based on the input.
