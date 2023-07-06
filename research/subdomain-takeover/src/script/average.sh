for domain in $(cat $1)
do
  number_domains=$(cat $2 | grep -Eo "$domain\$" | wc -l); echo "$domain: $number_domains" | anew subs_per_domain;
  total=$(($total+number_domains));
done;
count=$(wc -l $1 | cut -d " " -f 1);
let "output=$total/$count"; echo "Average: $output" | anew subs_per_domain;
