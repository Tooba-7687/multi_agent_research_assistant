import google.generativeai as genai
from tools.web_search import search_web, format_search_results
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def research_agent(query: str) -> dict:
    """
    Research Agent — The Gatherer
    Searches the web and extracts key raw information
    Args:
        query: User's research topic
    Returns:
        Dictionary with raw research data and sources
    """
    print("\n🔍 Research Agent is working...")
    print(f"   Topic: {query}")

    try:
        # Step 1 — Search the web using Tavily
        print("   Searching the web...")
        raw_results = search_web(query, max_results=5)
        formatted_results = format_search_results(raw_results)

        # Step 2 — Use Gemini to extract key points from search results
        print("   Extracting key information with Gemini...")
        
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are a Research Agent. Your job is to analyze the following 
        web search results and extract the most important and relevant 
        information about the topic: "{query}"

        Web Search Results:
        {formatted_results}

        Your task:
        1. Extract the most important facts and data points
        2. Identify key themes and concepts
        3. Note important statistics or figures if any
        4. List the sources used

        Provide a structured research output with clear sections.
        Be thorough but stick only to information from the search results.
        """

        response = None
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                break
            except Exception as api_err:
                if "429" in str(api_err) and attempt < 2:
                    wait = 5 * (attempt + 1)
                    print(f"   ⏳ Rate limited, retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise
        research_output = response.text

        # Step 3 — Collect sources
        sources = [
            {"title": r["title"], "url": r["url"]}
            for r in raw_results
        ]

        print("✅ Research Agent completed!")

        return {
            "query": query,
            "raw_data": research_output,
            "sources": sources,
            "status": "success"
        }

    except Exception as e:
        print(f"❌ Research Agent Error: {e}")
        return {
            "query": query,
            "raw_data": "",
            "sources": [],
            "status": "error",
            "error": str(e)
        }