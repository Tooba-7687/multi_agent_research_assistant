from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.writer_agent import writer_agent
import os
from datetime import datetime

def run_pipeline(query: str, tone: str = "professional") -> dict:
    """
    Orchestrator — The Pipeline Manager
    Connects all 3 agents in sequence and manages
    the complete research workflow
    Args:
        query: User's research topic
        tone:  Writing tone for the final report
    Returns:
        Dictionary with final report and metadata
    """

    print("\n" + "="*50)
    print("🚀 Multi-Agent Research Pipeline Started")
    print("="*50)
    print(f"📌 Topic : {query}")
    print(f"🎨 Tone  : {tone}")
    print("="*50)

    start_time = datetime.now()

    # ─────────────────────────────────────────
    # STEP 1 — Research Agent
    # ─────────────────────────────────────────
    print("\n[1/3] Running Research Agent...")
    research_data = research_agent(query)

    if research_data["status"] == "error":
        return {
            "status":  "error",
            "step":    "research",
            "message": "Research Agent failed",
            "error":   research_data.get("error", "Unknown error")
        }

    # ─────────────────────────────────────────
    # STEP 2 — Summarizer Agent
    # ─────────────────────────────────────────
    print("\n[2/3] Running Summarizer Agent...")
    summary_data = summarizer_agent(research_data)

    if summary_data["status"] == "error":
        return {
            "status":  "error",
            "step":    "summarizer",
            "message": "Summarizer Agent failed",
            "error":   summary_data.get("error", "Unknown error")
        }

    # ─────────────────────────────────────────
    # STEP 3 — Writer Agent
    # ─────────────────────────────────────────
    print("\n[3/3] Running Writer Agent...")
    final_output = writer_agent(summary_data, tone=tone)

    if final_output["status"] == "error":
        return {
            "status":  "error",
            "step":    "writer",
            "message": "Writer Agent failed",
            "error":   final_output.get("error", "Unknown error")
        }

    # ─────────────────────────────────────────
    # STEP 4 — Save Report to File
    # ─────────────────────────────────────────
    end_time  = datetime.now()
    duration  = (end_time - start_time).seconds

    report_path = save_report(
        query  = query,
        report = final_output["report"]
    )

    print("\n" + "="*50)
    print("✅ Pipeline Completed Successfully!")
    print(f"⏱️  Time Taken : {duration} seconds")
    print(f"📄 Report Saved: {report_path}")
    print("="*50)

    return {
        "status":      "success",
        "query":       query,
        "report":      final_output["report"],
        "sources":     final_output["sources"],
        "tone":        tone,
        "report_path": report_path,
        "duration":    duration
    }


def save_report(query: str, report: str) -> str:
    """
    Save the final report to outputs/reports folder
    Args:
        query:  Research topic (used for filename)
        report: Final report text
    Returns:
        Path where report was saved
    """
    try:
        # Create folder if it doesn't exist
        os.makedirs("outputs/reports", exist_ok=True)

        # Create clean filename from query
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_name = query[:30].replace(" ", "_").replace("/", "_")
        filename   = f"outputs/reports/{clean_name}_{timestamp}.txt"

        # Write report to file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Research Topic: {query}\n")
            f.write(f"Generated At: {datetime.now()}\n")
            f.write("="*50 + "\n\n")
            f.write(report)

        return filename

    except Exception as e:
        print(f"⚠️ Could not save report: {e}")
        return ""