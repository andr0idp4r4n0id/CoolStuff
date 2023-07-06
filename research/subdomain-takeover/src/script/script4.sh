cat $1 | dnsx -t $2 -raw -a | grep -Poz ".+IN\tCNAME\t\K(.*?)(\n)" | grep -Eva ".+sectionedge.+|.+ep\.section\.io.+" | sed 's/\.$//g'
cat $1
