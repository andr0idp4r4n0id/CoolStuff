import csv

def write_csv():
    langs = ["secrets","abap","apex","c","cpp","cloudformation","cobol","csharp","css",
            "docker","flex","go","html","java","javascript","kotlin","kubernetes","objective-c","php","pli",
            "plsql","python","rpg","ruby","scala","swift","terraform","text","typescript","tsql","vbnet","vb6","xml"]
    headers = ["RuleId", "Title", "URL"]
    for lang in langs:
        headers.append(lang)
    csv_f = open("rules_by_language.csv", "w+")
    writer = csv.writer(csv_f)
    writer.writerow(headers)
    with open("parsed.txt") as f:
        for row in f.readlines():
            try:
                data = [None] * (len(headers) + 1)
                split_row = row.split("\\")
                rule = split_row[1].split("/")[1].strip("\n").strip(" ")
                name = split_row[2].strip("\n").strip(" ")
                language = split_row[1].split("/")[0].strip("\n").strip(" ")
                for index, lang in enumerate(headers):
                    if language == lang:
                        data.insert(index, "x")
                        break
                data[0] = rule
                data[1] = name
                data[2] = f"https://rules.sonarsource.com/{language}/{rule}"
                writer.writerow(data)
            except Exception:
                print(split_row)
    csv_f.close()

write_csv()
