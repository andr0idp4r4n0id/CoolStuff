import csv
import re


def write_csv():
    headers = ["RuleId", "Title", "URL", "community-edition", "developer-edition", "enterprise-edition", "sonarcloud-edition", "sonarlint-edition"]
    csv_f = open("rules_by_edition.csv", "w+")
    writer = csv.writer(csv_f)
    writer.writerow(headers)
    with open("parsed.txt") as f:
        for row in f.readlines():
            try:
                data = [None] * (len(headers) + 1)
                split_row = row.split("\\")
                rule = split_row[1].split("/")[1].strip("\n").strip(" ")
                name = split_row[2].strip("\n").strip(" ")
                editions = split_row[0].split(",")
                language = split_row[1].split("/")[0].strip("\n").strip(" ")
                for index, header in enumerate(headers):
                    for edition in editions:
                        if edition not in header:
                            continue
                        data.insert(index, "x")
                data[0] = rule
                data[1] = name
                data[2] = f"https://rules.sonarsource.com/{language}/{rule}"
                writer.writerow(data)
            except Exception as e:
                print(e)
    csv_f.close()

write_csv()
