#!/bin/sh
mkdir -p log
color_fmt="s/\x1B\[([0-9]{1,3}(;[0-9]{1,2};?)?)?[mGK]//g"
doc_str="Usage: ./run.sh [url] [arguments]
    url: example.com
    arguments: all arguments, default is None
    example: ./run.sh example.com
             ./run.sh -u example.com
             ./run.sh -f list_target.txt
             ./run.sh -h
"

list_url=()
# if have -f argument, use it as file name, load list url from file
if [ "$1" = "-f" ]; then
    # Read file into list_url variable
    while IFS= read -r line; do
        list_url+=("$line")
    done < "$2"
elif [ "$1" = "-h" ]; then
    echo "$doc_str"
    exit 1
elif [ "$1" = "-u" ]; then
    list_url+=("$1")
else
    list_url+=("$1")
fi

if [ $# -eq 0 ]; then
    echo "$doc_str"
    exit 1
fi

today=$(date '+%Y-%m-%d_%H:%M:%S')

function print_done() {
    echo "==============" >> $file_name_log
    echo "$1 done" >> $file_name_log
    echo "==============" >> $file_name_log
    echo "\n\n\n" >> $file_name_log
}


# Iterate through each URL in list_url array
for url in "${list_url[@]}"
do
    # Perform desired action on each URL, such as curling it
    echo "process $url"
    file_name_log="log/${url}_${today}.log"
    #docker run -it --rm -v osmws:/root/.osmedeus/workspaces j3ssie/osmedeus:latest scan -f fast -t "$url" | sed -r "$color_fmt" >> $file_name_log 2>&1
    #print_done "osmedeus"  docker run projectdiscovery/nuclei:latest -u "$url"               | sed -r "$color_fmt" >> $file_name_log 2>&1
    print_done "nuclei"
    docker run projectdiscovery/subfinder:latest -d "$url" | sed -r "$color_fmt" >> $file_name_log 2>&1
    print_done "subfinder"
    docker run projectdiscovery/naabu:latest -host "$url"  | sed -r "$color_fmt" >> $file_name_log 2>&1
    print_done "naabu"
    docker run projectdiscovery/katana:latest -u "$url"    | sed -r "$color_fmt" >> $file_name_log 2>&1
    print_done "katana"
done

