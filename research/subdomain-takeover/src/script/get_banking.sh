curl -s https://www.ffiec.gov/npw/Institution/TopHolderList/ | \
  jq -r '.[] | .RssdId' | \
  head -n 3 | \
  xargs -I {} curl -s "https://www.ffiec.gov/npw/Institution/Profile/{}" | \
  xmllint --html --xpath '//li[@id="liUrl"]/a/text()' - 2>/dev/null
