import json
from sys import argv
from requests import get

def convert_sarif():
    results = []
    locations = []
    code_flows = []
    code_flows_locations = []
    location_flow_locations = []
    code_flows_locations = []
    threadFlows = []
    rules = []
    rules_dict = {}
    files = argv[1].split(":")
    done_rules = []
    with open(files[0]) as f:
        data = json.load(f)
        for issue in data['issues']:
            try:
                if issue["severity"] in ["CRITICAL", "MAJOR", "BLOCKER"]:
                    severity = "error"
                elif issue["severity"] == "MINOR":
                    severity = "warning"
                else:
                    severity = "note"
                component = issue["component"].split(":")[1]
                locations.append({"physicalLocation": {"artifactLocation": {"uri": f"https://{argv[2]}/tree/{argv[3]}/{component}#L{issue['textRange']['startLine']}"}, "region": {
                    "startLine": issue["textRange"]["startLine"], "startColumn": issue["textRange"]["startOffset"], "endLine":issue["textRange"]["endLine"], "endColumn":issue["textRange"]["endOffset"]}}})
                for flow_loc in issue["flows"]:
                    if len(flow_loc) > 0:
                        for  loc_data in flow_loc["locations"]:
                            component = loc_data["component"].split(":")[1]
                            code_flows.append({"location":{"physicalLocation":{"artifactLocation":{"uri":f"https://{argv[2]}/tree/{argv[3]}/{component}#L{loc_data['textRange']['startLine']}"}, "region":{"startLine":loc_data["textRange"]["startLine"], "startColumn":loc_data["textRange"]["startOffset"], "endLine":loc_data["textRange"]["endLine"], "endColumn":loc_data["textRange"]["endOffset"]}}, "message":{"text":loc_data["msg"]}}})
                        threadFlows.append({"locations":code_flows})
                        code_flows_locations.append({"threadFlows":threadFlows})
                dictionary = {
                    "properties":{"sonarType":"Vulnerability", "tags":issue["tags"], "effort":issue["effort"], "key":issue["key"]},
                    "ruleId":issue["rule"],
                    "level":severity,
                    "message": {
                        "text":issue["message"]
                    },
                    "locations":locations,
                }
                if len(code_flows_locations) > 0:
                    dictionary.update({"codeFlows":code_flows_locations})
                if issue["rule"] not in done_rules:
                    done_rules.append(issue["rule"])
                    r = get(f"http://localhost:9000/api/rules/show?key={issue['rule']}", headers={"Authorization":"Basic c3F1X2YwNmNkZTQ1ZTZiNDUzYmQ0NmY2YjgyMDllMzU5MTdkN2Q3OWFhYmQ6"})
                    j = r.json()
                    rules_dict = {
                        "id":issue["rule"],
                        "name":j["rule"]["name"],
                        "shortDescription":{
                            "text":j["rule"]["htmlDesc"]
                        }
                    }
                    rules.append(rules_dict)
                results.append(dictionary)
                locations = []
                rules_dict = {}
                code_flows = []
                code_flows_locations = []
                threadFlows = []
            except Exception as e:
                print(f"1:{e}")
                continue
    done_rules = []
    with open(files[1]) as f:
        data = json.load(f)
        for hotspot in data["hotspots"]:
            try:
                locations.append({"physicalLocation":{"artifactLocation":{"uri":f"https://{argv[2]}/tree/{argv[3]}/{hotspot['component'].split(':')[1]}#L{hotspot['line']}"}, "region":{"startLine":hotspot["line"], "startColumn":hotspot["textRange"]["startOffset"], "endLine":hotspot["textRange"]["endLine"], "endColumn":hotspot["textRange"]["endOffset"]}}})
                for flow in hotspot["flows"]:
                    if len(flow) > 0:
                        for loc in flow["locations"]:
                            code_flows.append({"location":{"physicalLocation":{"artifactLocation":{"uri":f"https://{argv[2]}/tree/{argv[3]}/{loc['component'].split(':')[1]}#L{loc['textRange']['startLine']}"}, "region":{"startLine":loc["textRange"]["startLine"], "startColumn":loc["textRange"]["startOffset"], "endLine":loc["textRange"]["endLine"], "endColumn":loc["textRange"]["endOffset"]}}, "message":{"text":loc["msg"]}}})
                        threadFlows.append({"locations":code_flows})
                        code_flows_locations.append({"threadFlows":threadFlows})
                dictionary = {
                    "properties":{"sonarType":"Security Hotspot", "vulnerabilityProbability":hotspot["vulnerabilityProbability"], "securityCategory":hotspot["securityCategory"], "key":hotspot["key"]},
                    "ruleId":hotspot["ruleKey"],
                    "kind":"open",
                    "level":"none",
                    "message":{
                        "text":hotspot["message"]
                    },
                    "locations":locations,
                }
                if len(code_flows_locations) > 0:
                    dictionary.update({"codeFlows":code_flows_locations})
                if hotspot["ruleKey"] not in done_rules:
                    done_rules.append(hotspot["ruleKey"])
                    j = get(f"http://localhost:9000/api/rules/show?key={hotspot['ruleKey']}", headers={"Authorization":"Basic c3F1X2YwNmNkZTQ1ZTZiNDUzYmQ0NmY2YjgyMDllMzU5MTdkN2Q3OWFhYmQ6"}).json()
                    rules_dict = {
                        "id":hotspot["ruleKey"],
                        "name":j["rule"]["name"],
                        "shortDescription":{
                            "text":j["rule"]["htmlDesc"]
                        }
                    }
                    rules.append(rules_dict)
                results.append(dictionary)
                locations = []
                code_flows = []
                code_flows_locations = []
                threadFlows = []
                rules_dict = {}
            except Exception as e:
                print(f"2:{e}")
                continue
    runs = [{"tool": {"driver": {"name":"Sonarqube Developer-Edition", "version":"10.0.0.68432", "rules":rules}}, "results": results}]
    print(json.dumps({"version": "2.1.0", "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json", "runs": runs}))


convert_sarif()
