from agents.monitoring_agent import MonitoringAgent
from agents.analysis_agent import AnalysisAgent
from agents.briefing_agent import BriefingAgent
from agents.router_agent import RouterAgent
from agents.client_impact_agent import ClientImpactAgent
import json
import asyncio
from typing import TypedDict
from langgraph.graph import StateGraph, END
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))

with open("clients/data.json", "r") as f:
    clients = json.load(f)
    
#State
class GraphState(TypedDict):
    user_query:str
    filters:dict
    client_impact_results: dict
    monitoring_results:dict
    analysis_results:dict
    briefing:str
    run_client_analysis:bool
    run_briefing:bool

#Agents
monitoring_agent = MonitoringAgent()    
analysis_agent = AnalysisAgent()
briefing_agent = BriefingAgent()
router_agent = RouterAgent()
client_impact_agent = ClientImpactAgent()

#Nodes
async def monitoring_node(state: GraphState):

    print("\n🚨 Monitoring Node Running...\n")

    results = await monitoring_agent.monitor_sources(state['user_query'])

    return {
        "monitoring_results": results
    }


async def analysis_node(state: GraphState):

    print("\n🧠 Analysis Node Running...\n")

    monitoring_results = state["monitoring_results"]

    analysis_results = (
        analysis_agent.analyze_documents(
            monitoring_results
        )
    )

    return {
        "analysis_results": analysis_results
    }


async def briefing_node(state: GraphState):

    print("\n📰 Briefing Node Running...\n")

    analysis_results = state["analysis_results"]

    filters = state["filters"]

    briefing = briefing_agent.generate_briefing(
        analysis_results,
        filters
    )

    impact_results = state.get(
        "client_impact_results",
        []
    )

    if impact_results:

        print("\n🏢 CLIENT IMPACTS:\n")

        for client_result in impact_results:

            for impact in client_result["impacts"]:

                print(f"Client: {impact['client']}")
                print(f"Source: {impact['source']}")

                analysis = impact["impact_analysis"]

                print(f"Severity: {analysis['severity']}")
                print(
                    f"Impact Score: "
                    f"{analysis['impact_score']}"
                )

                print("Reasons:")
                for reason in analysis["reasons"]:
                    print(f" - {reason}")

                print("Recommended Actions:")
                for action in analysis[
                    "recommended_actions"
                ]:
                    print(f" - {action}")

                print("-" * 50)

    return {
        "briefing": briefing,
        "client_impact_results": impact_results
    }

async def router_node(state: GraphState):

    print("\n🧭 Router Node Running...\n")

    query = state["user_query"].lower()
    client_mode = any(word in query for word in [
        "client",
        "impact",
        "company",
        "companies"
    ])
    briefing_mode = any(word in query for word in [
        "update",
        "regulation",
        "brief",
        "news"
    ])

    filters = router_agent.route_query(query)

    return {
        "filters": filters,
        "run_client_analysis":client_mode,
        "run_briefing":briefing_mode
    }

async def client_impact_node(state: GraphState):

    print("\n🏢 Client Impact Node Running...\n")

    analysis_results = state["analysis_results"]

    all_client_impacts = []

    for client in clients:

        impact_results = (
            client_impact_agent.analyze_client_impact(
                client,
                analysis_results
            )
        )

        all_client_impacts.append(impact_results)

    return {
        "client_impact_results": all_client_impacts
    }

#Graph
graph = StateGraph(GraphState)
graph.add_node("monitoring",monitoring_node)
graph.add_node("analysis",analysis_node)
graph.add_node("briefing",briefing_node)
graph.add_node("router",router_node)
graph.add_node("client_impact",client_impact_node)


#start fro graph
def route_after_analysis(state):

    query = state["user_query"].lower()

    if any(word in query for word in [
        "client",
        "impact",
        "company",
        "companies"
    ]):
        return "client_impact"

    return "briefing"


graph.set_entry_point("router")

graph.add_edge("router","monitoring")
graph.add_edge("monitoring","analysis")
graph.add_conditional_edges("analysis",route_after_analysis,{"client_impact": "client_impact","briefing": "briefing"})
graph.add_edge("client_impact","briefing")
graph.add_edge("briefing",END)

app = graph.compile()

#MAIN
async def main():
    query = input("\nEnter your query: ")
    results = await app.ainvoke({"user_query":query})

    print("\n")
    print("=" * 70)
    print("✅ FINAL REGULATORY INTELLIGENCE OUTPUT")
    print("=" * 70)

    print(results["briefing"])
    print("\n")
    print("=" * 70)
    print("🏢 CLIENT IMPACT ANALYSIS")
    print("=" * 70)

    client_impact_results = results.get("client_impact_results", [])
    if client_impact_results:
        for client_result in client_impact_results:
            for impact in client_result.get("impacts", []):
                print(f"\nClient: {impact['client']}")
                print(f"Source: {impact['source']}")

                analysis = impact["impact_analysis"]

                print(f"Severity: {analysis['severity']}")

                if "impact_score" in analysis:
                    print(f"Impact Score: {analysis['impact_score']}/10")

                print("\nReasons:")
                for reason in analysis.get("reasons", []):
                    print(f" - {reason}")

                print("\nRecommended Actions:")
                for action in analysis.get("recommended_actions", []):
                    print(f" - {action}")

                print("-" * 50)
    else:
        print("No client impact results available.")


if __name__=="__main__":
    asyncio.run(main())    


