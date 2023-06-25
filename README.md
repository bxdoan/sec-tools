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

the result will be saved in `log` directory

# access the docker via bash if you want to see a raw result of the previous or current scan
```shell
docker ps

docker exec -it <container-id> /bin/sh
```
