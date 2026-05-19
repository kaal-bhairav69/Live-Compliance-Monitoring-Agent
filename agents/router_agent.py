class RouterAgent:
    def __init__(self):
        self.name = "Query Router Agent"

    def route_query(self, query: str):

        query = query.lower()

        filters = {
            "jurisdiction": None,
            "topic": None,
            "severity": None
        }

        # Jurisdiction Routing

        if "india" in query:
            filters["jurisdiction"] = "India"

        elif "usa" in query or "us" in query:
            filters["jurisdiction"] = "USA"

        # Topic Routing

        if "bank" in query or "rbi" in query:
            filters["topic"] = "banking"

        elif "tax" in query:
            filters["topic"] = "tax"

        elif "insider trading" in query:
            filters["topic"] = "insider trading"

        # Severity Routing

        if "high severity" in query:
            filters["severity"] = "High"

        return filters

