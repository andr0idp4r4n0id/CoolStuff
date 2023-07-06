#! /usr/bin/env bash
for url in $(cat $1);
do
  if [[ $(curl -L -k -s $url | wc -w) =~ ([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|1000) ]]; then echo $url | tee -a valid_http; fi &
done
cat valid_http | dnsx -cname -resp -silent | tee -a valid_http_cnames
