# agentic_groq.py
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool


from tavily import TavilyClient
from supadata import Supadata

load_dotenv() 
import os
SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY")
supadata = Supadata(api_key=SUPADATA_API_KEY)

@tool
def search_web(query: str) -> str:
    """Search the web for a query using Tavily API."""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query)
    
    content = ""
    for item in response.get("results", []):
        content += item.get("content", "")
    
    return content


@tool
def transcribe_video(url: str) -> str:
    """Transcribe YouTube video/shorts or Instagram reels into text using Supadata API."""
    try:
        # Request transcript
        transcript_result = supadata.transcript(
            url=url,
            lang="en",
            text=True,
            mode="auto"   # options: 'native', 'auto', or 'generate'
        )

        # If it's a job, poll until ready
        if hasattr(transcript_result, 'job_id'):
            result = supadata.transcript.get_job_status(transcript_result.job_id)
            if result.status == "completed":
                return result.content
            else:
                return f"Job still processing: {result.status}"
        
        # Otherwise, we got transcript text directly
        return transcript_result

    except Exception as e:
        return f"Error during transcription: {str(e)}"
    
@tool
def get_weather(location: str):

    """Get weather by location"""
    tavily_client = TavilyClient(api_key="YOUR_API_KEY")
    response = tavily_client.search(f"Get whether for {location}")

    print(location)
    try:
        
        # content = response.get("results")[0].get("content")
        content=""
        for i in response.get("results"):
            content=content+i.get("content")
        # print(content)
    except:
        return(response)
    
    return content

def processMessage(agent_executor, config, content):
    # Turn 2: context-aware tool use (weather)
    input_message = {"role": "user", "content": content}
    last_message = None
    for step in agent_executor.stream({"messages": [input_message]}, config, stream_mode="values"):
        last_message = step["messages"][-1]
    
    # Print only the final message content
    return last_message.content

def main():
    load_dotenv()  # loads GROQ_API_KEY from .env

    # ✅ 1. Initialize Groq LLM
    llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

    # ✅ 2. Create memory (for conversation context)
    memory = MemorySaver()

    # ✅ 3. Define tools (TavilySearch here for weather/info)
    tools = [get_weather, transcribe_video, search_web]

#     tool_descriptions = {
#     "transcribe_video": "Call this for any YouTube or Instagram video URL to get the transcript.",
#     "search_web": "Call this to verify facts or claims using web search.",
#     "get_weather": "Call this to get weather of a location by passing location as argument"
# }
    
    # ✅ 4. Build the agent
    agent_executor = create_react_agent(llm, tools, checkpointer=memory)

    # ✅ 5. Run a sample conversation
    config = {"configurable": {"thread_id": "abc123"}}

    print("start convo with LLM")
    while(True):
        print("USER INPUT: ")
        msg = input("")
        if(msg == "exit"):
            break
        
        print("AI RESPONSE: ")
        res = processMessage(agent_executor, config, msg)
        print(res)
        
       


if __name__ == "__main__":
    main()
    # print(get_weather("mumbai").get("results")[0].get("content"))
    # print(transcribe_youtube("https://www.instagram.com/reel/DPV20OkkePE/?igsh=b2k3MmlnbDRlN2k1"))

