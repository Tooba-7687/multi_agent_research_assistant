import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def writer_agent(summary_data: dict, tone: str = "professional") -> dict:
    """
    Writer Agent — The Creator
    Takes structured summary and writes a 
    polished, full research report
    Args:
        summary_data: Dictionary output from Summarizer Agent
        tone: Writing tone — professional / academic / casual
    Returns:
        Dictionary with final written report
    """
    print("\n✍️  Writer Agent is working...")

    try:
        # Step 1 — Validate incoming data
        if summary_data.get("status") == "error":
            print("❌ Received error from Summarizer Agent")
            return {
                "report":  "",
                "status":  "error",
                "error":   "Summarizer Agent failed"
            }

        summary    = summary_data.get("summary", "")
        query      = summary_data.get("query", "")
        key_points = summary_data.get("key_points", [])
        sources    = summary_data.get("sources", [])

        print(f"   Writing report for: {query}")
        print(f"   Tone: {tone}")

        # Step 2 — Format sources for the report
        sources_text = ""
        for i, source in enumerate(sources, 1):
            sources_text += f"{i}. {source['title']}\n   {source['url']}\n"

        # Step 3 — Use Gemini to write the full report
        print("   Generating full report with Gemini...")
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are a Professional Writer Agent. Your job is to write a 
        complete, polished research report based on the structured 
        summary provided.

        Research Topic: "{query}"
        Writing Tone:   {tone}

        Structured Summary to work from:
        {summary}

        Write a complete research report using this exact structure:

        # {query}

        ## Introduction
        (Write an engaging 2-3 sentence introduction about the topic)

        ## Overview
        (Write a comprehensive paragraph explaining the topic)

        ## Key Findings
        (Write detailed paragraphs covering all the main points
         and themes from the summary)

        ## Important Facts & Statistics
        (Present key data points in a clear, readable format)

        ## Analysis
        (Write your analysis connecting all the findings together
         in 2-3 paragraphs)

        ## Conclusion
        (Write a strong 2-3 sentence conclusion summarizing
         the most important takeaways)

        ## Sources
        {sources_text}

        Important rules:
        - Use {tone} tone throughout
        - Write in complete, flowing sentences
        - Make it engaging and easy to read
        - Do not use bullet points in Introduction, 
          Overview, Analysis or Conclusion sections
        - Minimum 600 words for the full report
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
        final_report = response.text

        print("✅ Writer Agent completed!")

        return {
            "query":   query,
            "report":  final_report,
            "sources": sources,
            "tone":    tone,
            "status":  "success"
        }

    except Exception as e:
        print(f"❌ Writer Agent Error: {e}")
        return {
            "query":  query,
            "report": "",
            "sources": [],
            "status": "error",
            "error":  str(e)
        }