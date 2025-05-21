import os, pathlib, urllib.request, urllib.error, json

marzban_path = str(pathlib.Path(__file__).parent.resolve())
data={
    "node_name":"node",
    "SERVICE_PORT":"62050",
    "XRAY_API_PORT":"62051",
    "SSL_CLIENT_CERT_FILE":marzban_path+"/ssl_client.pem",


}
try:
    res = urllib.request.urlopen(f'https://ipinfo.io/json').read().decode('utf8')
    res = json.loads(res)
    if res["country"] == "IR":
        #DNS_IP = "185.51.200.2"
        DNS_IP = "194.59.215.36"

    else: DNS_IP = "8.8.8.8"
except urllib.error.HTTPError:
    #DNS_IP = "185.51.200.2"
    DNS_IP = "8.8.8.8"

os.system("ufw disable")

def change_to_iran_dns():
    os.system(f'echo "nameserver {DNS_IP}" > /etc/resolv.conf')

def change_to_normal_dns():
    os.system(f'echo "nameserver 8.8.8.8" > /etc/resolv.conf')


def install_xray_core():
    change_to_normal_dns()
    os.system('bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install --version 1.8.24')
    os.system("systemctl disable --now xray snapd snapd.socket")

def install_pip():
    change_to_normal_dns()
    os.system('apt-get update')
    os.system("apt install python3-pip build-essential libssl-dev libffi-dev libpq-dev python3-dev -y")

def install_python_packages():
    change_to_iran_dns()
    os.system("pip install -r requirements.txt") # ubuntu 20 or lower
    change_to_normal_dns()

def run_marzban_at_server_reboot(node_name):
    
    with open("""/etc/systemd/system/marzban-{node_name}.service""", "w") as file:
        file.write(f"""
[Service]
WorkingDirectory={marzban_path}
ExecStart=python3 main.py
Restart=always
[Install]
WantedBy=multi-user.target
""".strip("\n").strip())
    os.system("systemctl daemon-reload")
    os.system("""systemctl enable --now marzban-{node_name}""")


def read_certificate():
    print("Enter Client cert : ")

    lines = []
    while True:
        line = input()
        lines.append(line)
        if line.strip() == "-----END CERTIFICATE-----":
            break

    certificate_text= "\n".join(lines)
    with open("ssl_client.pem", "w") as f:
        f.write(certificate_text)

def get_data():
    data["node_name"]=str(input("Enter Marzban node Name : ")).strip() or "node"
    data["SERVICE_PORT"]=str(input("Enter node port (Defult: 62050) : ")).strip() or "62050"
    data["XRAY_API_PORT"]=str(input("Enter API port (Defult: 62051) : ")).strip() or "62051"

get_data()
read_certificate()
print(data)
install_pip()
install_xray_core()
install_python_packages()
change_to_normal_dns()
run_marzban_at_server_reboot(data["node_name"])









