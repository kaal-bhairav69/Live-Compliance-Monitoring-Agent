import asyncio
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from extractor import extract_pdf_text


class MonitoringAgent:

    def __init__(self):
        self.sources = {"India": ["rbi","sebi"],"USA": ["sec","irs"]}

    async def monitor_sources(self,user_query):

        documents = []
        query=user_query.lower()
        filtered_sources = {}
        for jurisdiction,source_list in self.sources.items():
            if jurisdiction.lower() in query:
                filtered_sources[jurisdiction]=source_list

                for source in source_list:
                    if source.lower() in query:
                        filtered_sources[jurisdiction]=[source]

        if not filtered_sources:
            filtered_sources = self.sources                

        print("\n🔍 Monitoring regulatory sources...\n")

        for jurisdiction,source_list in filtered_sources.items():
            for source in source_list:
                try:
                    print(f"Checking {source.upper()}...")
                    extracted_data = await extract_pdf_text(source)
                    
                    if extracted_data:
                        documents.append({
                        "jurisdiction":jurisdiction,
                        "source": source.upper(),
                        "status": "success",
                        "data": extracted_data
                        })

                        print(f"✓ New document found from {source.upper()}")

                    else:
                        documents.append({
                            "jurisdiction":jurisdiction,
                            "source":source.upper(),
                            "status":"failed",
                            "data":extracted_data
                        })    
                        print(f"✗ No document found from {source.upper()}")


                except Exception as e:
                    documents.append({
                       "jurisdiction":jurisdiction,
                       "source": source.upper(),
                       "status": "error",
                       "error": str(e)
                    })        
                    print(f"❌ Error monitoring {source.upper()}: {e}")

        return {
            "total_sources": sum(len(sources) for sources in self.sources.values()),
            "documents_found": len(
                [d for d in documents if d["status"] == "success"]
            ),
            "documents": documents
        }            

async def main():

    agent = MonitoringAgent()

    results = await agent.monitor_sources()

    print("\n📄 Monitoring Results:\n")

    for doc in results["documents"]:

        print(f"Jurisdiction: {doc['jurisdiction']}")
        print(f"Source: {doc['source']}")

        if doc["status"] == "success":

            data = doc["data"]

            print(f"Filename: {data.get('filename')}")
            print(f"Pages: {data.get('total_pages')}")

        print("-" * 50)


if __name__ == "__main__":
    asyncio.run(main())