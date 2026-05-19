from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

class BriefingAgent:
    def __init__(self):
        self.name = "Daily Regulatory Briefing Agent"

    def generate_briefing(self, analysis_results,filters=None):

        print("\n📰 Generating regulatory briefing...\n")

        briefing = []
        
        briefing.append("=" * 60)
        briefing.append("🌍 DAILY REGULATORY INTELLIGENCE BRIEFING")
        briefing.append("=" * 60)
        briefing.append("")

        analyzed_docs = analysis_results.get("results", [])
        if filters:
            filtered_docs=[]
            for item in analyzed_docs:
                keep=True
                if filters.get("jurisdiction"):
                    if item.get("jurisdiction")!=filters["jurisdiction"]:
                        keep=False
                if filters.get("severity"):
                    severity=(item.get("analysis",{}).get("summary",{}).get("serverity",""))        
                    if severity.lower()!=filters["severity"].lower():
                        keep=False
                if keep:
                    filtered_docs.append(item)        
            analyzed_docs = filtered_docs        

        jurisdiction_groups={}

        for item in analyzed_docs:
            jurisdiction=item.get(
                "jurisdiction",
                "Unknown"
            )
            if jurisdiction not in jurisdiction_groups:
                jurisdiction_groups[jurisdiction]=[]

            jurisdiction_groups[jurisdiction].append(item)

        if not analyzed_docs:
            briefing.append("No regulatory updates found today.")
            return "\n".join(briefing)
        
        for jurisdiction,docs in jurisdiction_groups.items():
            briefing.append(
                f"{jurisdiction.upper()} REGULATORY BREIFING"
            )
            briefing.append("")
            for item in docs:
                try:
                    if item["status"]!="analyzed":
                        continue
                    source=item["source"]
                    analysis_data=item["analysis"]
                    summary_block = analysis_data.get("summary",{})
                    short_summary = summary_block.get(
                        "short_summary",
                        "no summary available."
                    )
                    key_changes = summary_block.get(
                        "key_changes",
                        []
                    )
                    affected_industries=summary_block.get(
                        "affected_industries",
                        []
                    )
                    severity=summary_block.get(
                        "severity",
                        "Unknown"
                    )
                    briefing.append(f"📌 SOURCE: {source}")
                    briefing.append(f"⚠️ Severity: {severity}")
                    briefing.append("")
                    briefing.append("📝 Summary:")
                    briefing.append(short_summary)
                    briefing.append("")
                    briefing.append("🔄 Key Changes:")

                    if key_changes:
                        for change in key_changes:
                            briefing.append(f"  • {change}")

                    else:
                        briefing.append("  • No key changes identified")

                    briefing.append("")
                    briefing.append("🏢 Affected Industries:")

                    if affected_industries:
                       for industry in affected_industries:
                        briefing.append(f"  • {industry}")

                    else:
                      briefing.append("  • Not specified")
                    briefing.append("")
                    briefing.append("-" * 60)
                    briefing.append("")

                except Exception as e:
                    briefing.append(
                    f"❌ Error generating briefing: {e}"
                )

        return "\n".join(briefing)


if __name__ == "__main__":

    import asyncio

    from monitoring_agent import MonitoringAgent
    from analysis_agent import AnalysisAgent

    async def main():

        monitoring_agent = MonitoringAgent()

        monitoring_results = (
            await monitoring_agent.monitor_sources()
        )

        analysis_agent = AnalysisAgent()

        analysis_results = (
            analysis_agent.analyze_documents(
                monitoring_results
            )
        )

        briefing_agent = BriefingAgent()

        briefing = briefing_agent.generate_briefing(
            analysis_results
        )

        print("\n")
        print(briefing)

    asyncio.run(main())