#! /usr/bin/env bash

markup=$(
  curl -s -k -X $'GET' \
    -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0' \
    $'https://fortune.com/ranking/fortune500/2022/search/'
)

script=$(
  echo "$markup" | \
    xmllint --html --xpath '//script[@id="__NEXT_DATA__"]/text()' - 2> /dev/null
)

json=$(
  echo "$script" |
    sed -e 's/^<!\[CDATA\[//' -e 's/]]>$//'
)

echo "$json" |
  jq -r '.props.pageProps.franchiseList'
