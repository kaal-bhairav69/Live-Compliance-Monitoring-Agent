import json
import re

from phi.agent import Agent
from phi.model.groq import Groq

from pydantic import BaseModel
from typing import List


class ImpactAnalysis(BaseModel):

    impacted: bool

    severity: str

    reasons: List[str]

    impact_score: int

    recommended_actions: List[str]


class ClientImpactAgent:

    def __init__(self):

        self.agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            markdown=False,
            name="Client impact analysis agent",
            instructions=[
                """
                You are a regulatory compliance analyst.

                Return ONLY valid JSON.

                Required schema:

                {
                  "impacted": true,
                  "severity": "High",
                  "reasons": [],
                  "impact_score":8,
                  "recommended_actions": []
                }
                Only mark impacted=true if regulation DIRECTLY affects
                the client's industry, operations, compliance obligations,
                or business workflows.

                Rules:
                - If regulation directly affects client operations → high impact score
                - If indirectly related → medium score
                - If unrelated → low/zero score
                - No markdown
                - No explanations
                - No code blocks
                - ONLY raw JSON
                """
            ]
        )

    def analyze_client_impact(
        self,
        client_profile,
        analysis_results
    ):

        impacts = []

        analyzed_docs = analysis_results.get(
            "results",
            []
        )

        for item in analyzed_docs:

            if item["status"] != "analyzed":
                continue

            regulation = item["analysis"]

            prompt = f"""
            CLIENT PROFILE:

            {json.dumps(client_profile, indent=2)}

            REGULATION:

            {json.dumps(regulation, indent=2)}

            Determine:

            1. Does this regulation impact the client?
            2. Severity
            3. Reasons
            4. Recommended actions
            """

            try:

                response = self.agent.run(prompt)

                response_text = (
                    response.content
                    if hasattr(response, "content")
                    else str(response)
                )

                response_text = re.sub(r"```json|```","",response_text).strip()

                json_match = re.search(
                    r'\{.*\}',
                    response_text,
                    re.DOTALL
                )

                if json_match:

                    json_str = json_match.group(0)

                    impact_data = json.loads(json_str)

                else:

                    impact_data = json.loads(response_text)

                validated = ImpactAnalysis(
                    **impact_data
                )

                if validated.impacted:

                    impacts.append({

                        "client": client_profile["name"],

                        "source": item["source"],

                        "jurisdiction": item["jurisdiction"],

                        "impact_analysis": {

                            "severity": validated.severity,

                            "impact_score":validated.impact_score,

                            "reasons": validated.reasons,

                            "recommended_actions":
                            validated.recommended_actions
                        }
                    })

            except Exception as e:

                print(
                    f"CLIENT IMPACT ERROR: {e}"
                )

        return {

            "client": client_profile["name"],

            "impacts": impacts
        }