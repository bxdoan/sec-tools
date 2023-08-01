#!/bin/sh
trap "exit" INT
SH_DIR=`cd $(dirname "$BASH_SOURCE") && pwd`
RETRO_DIR=`cd $SH_DIR/.. && pwd`
nuclei_docker_dir="/root/fuzzing-templates"
fuzzing_templates="$RETRO_DIR/fuzzing-templates"

color_fmt="s/\x1B\[([0-9]{1,3}(;[0-9]{1,2};?)?)?[mGK]//g"
doc_str="Usage: ./run.sh [url] [arguments]
    url: example.com
    arguments: all arguments, default is None
    example: ./run.sh example.com
             ./run.sh -u example.com
             ./run.sh -f list_target.txt
             ./run.sh -h
"

# if have -f argument, use it as file name, load list url from file
list_target=()
if [ "$1" = "-f" ]; then
    # Read file into list_target variable
    while IFS= read -r line; do
        list_target+=("$line")
    done < "$2"
elif [ "$1" = "-h" ]; then
    echo "$doc_str"
    exit 1
elif [ "$1" = "-u" ]; then
    list_target+=("$2")
else
    list_target+=("$1")
fi

if [ $# -eq 0 ]; then
    echo "$doc_str"
    exit 1
fi

# prepare log directory
mkdir -p log

function print_done() {
    echo "==============" >> $2
    echo "$1 done"        >> $2
    echo "==============" >> $2
    echo "\n\n\n"         >> $2
}

function mkdir_target() {
  now_log=$(date '+%Y-%m-%d_%H:%M:%S')
  target_log="log/$1_${now_log}"
  mkdir -p $target_log
}

function setup_docker() {
    docker pull projectdiscovery/subfinder:latest
    docker pull projectdiscovery/nuclei:latest
    docker pull projectdiscovery/naabu:latest
    docker pull projectdiscovery/katana:latest
}


function process() {
    url=$1
    printf "Process url: $url\n"
    now_log=$(date '+%Y-%m-%d_%H:%M:%S')
    file_name_log="${target_log}/${url}_${now_log}.log"
    echo "docker run projectdiscovery/nuclei:latest -u $url"
    docker run projectdiscovery/nuclei:latest -u "$url" | sed -r "$color_fmt" >> $file_name_log 2>&1
    print_done "nuclei" $file_name_log
    echo "docker run projectdiscovery/naabu:latest -host $url"
    docker run projectdiscovery/naabu:latest -host "$url" | sed -r "$color_fmt" >> $file_name_log 2>&1
    print_done "naabu" $file_name_log
    echo "docker run projectdiscovery/katana:latest -u $url"
    docker run projectdiscovery/katana:latest -u "$url" | sed -r "$color_fmt" >> $file_name_log 2>&1
    print_done "katana" $file_name_log
}

setup_docker

for target in "${list_target[@]}"
do
  target=$(echo "$target" | sed -r "s/www\.//g")
  printf "Process target: $target\n"
  mkdir_target "$target"
  # Get subdomains of target
  list_sub_target=$(docker run projectdiscovery/subfinder:latest -d "$target" | sed -r "$color_fmt")
  echo $list_sub_target
  output_with_spaces=$(tr '\n' ' ' <<< "$list_sub_target")
  list_sub_url=($output_with_spaces)

  # Iterate through each URL in list_sub_url array
  for url in "${list_sub_url[@]}"
  do
      # Perform desired action on each URL, such as curling it
      url=$(echo "$url" | sed -r "s/www\.//g")
      process "$url"
  done
done
