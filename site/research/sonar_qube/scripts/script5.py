import aiohttp
import asyncio
import json

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.text()
    

async def get_all():
    tasks = []
    async with aiohttp.ClientSession() as session:
        with open("keys.txt") as f:
            for key in f:
                tasks.append(fetch(session, f"https://rules.sonarsource.com/page-data{key}/page-data.json"))
            jsons = await asyncio.gather(*tasks)
            for json_ in jsons:
                loaded_json = json.loads(json_)
                rules = loaded_json["result"]["pageContext"]["rules"]
                language = loaded_json["result"]["pageContext"]["language"]["name"]
                language = language.lower()
                for rule in rules:
                    editions = []
                    summary = rule["summary"].strip("\n")
                    ruleKey = rule["ruleKey"].strip("\n")
                    availability = rule["availability"]
                    if "sonarqube" in availability:
                        if "injection" in rule["tags"] or language in ["c", "c++", "objective c", "swift", "abap", "t-sql", "pl/sql"]:
                            editions.append("developer-edition")
                        elif language in ["apex", "cobol", "pl/i", "rpg", "vb6"]:
                            editions.append("enterprise-edition")
                        else:
                            editions.append("community-edition")
                    if "sonarcloud" in availability:
                            editions.append("sonarcloud-edition")
                    if "sonarlint" in availability:
                        editions.append("sonarlint-edition")
                    editions_s = ','.join(editions)
                    print(f"{editions_s} \ {language}/{ruleKey} \ {summary}")

asyncio.run(get_all())