#!/bin/sh
mkdir -p log
color_fmt="s/\x1B\[([0-9]{1,3}(;[0-9]{1,2};?)?)?[mGK]//g"
doc_str="Usage: ./run.sh [url] [arguments]
    url: example.com
    arguments: all arguments, default is None
    example: ./run.sh example.com
"
url=$1
# if not have url, exit
if [ $# -eq 0 ]; then
    echo "$doc_str"
    exit 1
fi
function print_done() {
    echo "\n\n\n" >> $file_name_log
    echo "==============" >> $file_name_log
    echo "$1 done" >> $file_name_log
    echo "==============" >> $file_name_log
}
today=$(date '+%Y-%m-%d_%H:%M:%S')
file_name_log="log/${url}_${today}.log"


nuclei -u $url                                          | sed -r "$color_fmt" >> $file_name_log 2>&1
print_done "nuclei"
docker run projectdiscovery/subfinder:latest -d $url    | sed -r "$color_fmt" >> $file_name_log 2>&1
print_done "subfinder"
docker run -it projectdiscovery/naabu:latest -host $url | sed -r "$color_fmt" >> $file_name_log 2>&1
print_done "naabu"
