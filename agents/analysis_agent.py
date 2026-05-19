import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from summarise import get_summary

class AnalysisAgent:

    def __init__(self):
        self.name = "Regulatory Analysis Agent"

    def analyze_documents(self, monitoring_results):

        analyzed_documents = []

        print("\n🧠 Analyzing regulatory documents...\n")

        documents = monitoring_results.get("documents", [])

        for doc in documents:

            try:

                if doc["status"] != "success":
                    continue

                extracted_data = doc["data"]

                source = doc["source"]

                full_text = ""

                for page in extracted_data.get("content", []):

                    full_text += (
                        f"\n--- Page {page.get('page')} ---\n"
                    )

                    full_text += page.get("content", "")

                print(f"Analyzing {source} document...")

                analysis = get_summary(full_text, "pdf")

                analyzed_documents.append({
                    "jurisdiction":doc.get("jurisdiction"),

                    "source": source,

                    "status": "analyzed",

                    "filename": extracted_data.get("filename"),

                    "analysis": analysis

                })

                print(f"✓ Analysis completed for {source}")

            except Exception as e:

                analyzed_documents.append({
                    "jurisdictoin":doc.get("jurisdiction"),

                    "source": doc.get("source"),

                    "status": "error",

                    "error": str(e)

                })

                print(f"❌ Analysis failed: {e}")

        return {
            "total_analyzed": len(analyzed_documents),
            "results": analyzed_documents
        }


if __name__ == "__main__":

    import asyncio
    from monitoring_agent import MonitoringAgent

    async def main():

        monitoring_agent = MonitoringAgent()

        monitoring_results = (
            await monitoring_agent.monitor_sources()
        )

        analysis_agent = AnalysisAgent()

        results = analysis_agent.analyze_documents(
            monitoring_results
        )

        print("\n📊 Analysis Results:\n")

        for item in results["results"]:

            print(f"Source: {item['source']}")
            print(f"Status: {item['status']}")

            if item["status"] == "analyzed":

                analysis = item["analysis"]

                if "summary" in analysis:

                    print(
                        analysis["summary"]
                        .get("short_summary", "")
                    )

            print("-" * 50)

    asyncio.run(main())
