import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarizer_agent(research_data: dict) -> dict:
    """
    Summarizer Agent — The Analyst
    Takes raw research data and converts it into
    clean structured key points and themes
    Args:
        research_data: Dictionary output from Research Agent
    Returns:
        Dictionary with structured summary and themes
    """
    print("\n📝 Summarizer Agent is working...")

    try:
        # Step 1 — Validate incoming data
        if research_data.get("status") == "error":
            print("❌ Received error from Research Agent")
            return {
                "summary": "",
                "key_points": [],
                "themes": [],
                "status": "error",
                "error": "Research Agent failed"
            }

        raw_data = research_data.get("raw_data", "")
        query    = research_data.get("query", "")
        sources  = research_data.get("sources", [])

        print(f"   Analyzing research data for: {query}")

        # Step 2 — Use Gemini to summarize and structure
        print("   Structuring key insights with Gemini...")
        
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        You are a Summarizer Agent. Your job is to analyze raw research 
        data and organize it into a clean, structured summary.

        Research Topic: "{query}"

        Raw Research Data:
        {raw_data}

        Your task — provide output in this exact structure:

        MAIN SUMMARY:
        (Write 3-4 sentences summarizing the overall topic)

        KEY POINTS:
        - (Most important point 1)
        - (Most important point 2)
        - (Most important point 3)
        - (Most important point 4)
        - (Most important point 5)

        MAIN THEMES:
        - Theme 1: (brief explanation)
        - Theme 2: (brief explanation)
        - Theme 3: (brief explanation)

        IMPORTANT FACTS & STATISTICS:
        - (Any key numbers, dates, or figures found)

        Keep it concise, clear, and well organized.
        Only use information from the provided research data.
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
        structured_summary = response.text

        # Step 3 — Parse key points into a list
        key_points = []
        for line in structured_summary.split("\n"):
            if line.strip().startswith("-"):
                key_points.append(line.strip()[1:].strip())

        print("✅ Summarizer Agent completed!")

        return {
            "query":      query,
            "summary":    structured_summary,
            "key_points": key_points,
            "sources":    sources,
            "status":     "success"
        }

    except Exception as e:
        print(f"❌ Summarizer Agent Error: {e}")
        return {
            "query":      query,
            "summary":    "",
            "key_points": [],
            "sources":    [],
            "status":     "error",
            "error":      str(e)
        }