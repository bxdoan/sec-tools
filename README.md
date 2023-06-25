# sec-tools
combine tools for security using [projectdiscovery](https://github.com/projectdiscovery) resource:

- [nuclei](https://github.com/projectdiscovery/nuclei)
- [subfinder](https://github.com/projectdiscovery/subfinder)
- [naabu](https://github.com/projectdiscovery/naabu)
- [katana](https://github.com/projectdiscovery/katana)

## Usage
```shell
Usage: ./run.sh [url] [arguments]
    url: example.com
    arguments: all arguments, default is None
    example: ./run.sh example.com
             ./run.sh -u example.com
             ./run.sh -f list_target.txt
             ./run.sh -h
```


Example `list_target.txt`
```shell
example.com
example1.com
example2.com
```

the result will be saved in `log` directory

Access the docker via bash if you want to see a raw result of the previous or current scan
```shell
docker ps

docker exec -it <container-id> /bin/sh
```

or
```shell
./docker.sh image_name [arguments]
description: run docker image with /bin/sh
image_name: docker image name
arguments: all arguments, default is None
example: ./docker.sh nuclei
         ./docker.sh naabu
         ./docker.sh katana
         ./docker.sh subfinder
```
