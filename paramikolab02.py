import time
import paramiko

username = 'admin'
password = 'cisco'

device_ip = ["172.31.105.4", "172.31.105.5", "172.31.105.6"]
acl = ["conf t","access-list 100 deny   tcp host 172.31.105.30 any eq 22",
"access-list 100 deny   tcp host 172.31.105.30 any eq telnet",
"access-list 100 permit ip any any",]
R1 = ["router ospf 1 vrf control-data",
"network  172.31.105.16 0.0.0.15 area 0",
"network  172.31.105.32 0.0.0.15 area 0",
"router-id 1.1.1.1",
"interface GigabitEthernet0/1",
"ip access-group 100 in",
"ip address 172.31.105.17 255.255.255.240",
"no sh",
"interface GigabitEthernet0/2",
"ip address 172.31.105.46 255.255.255.240",
"no sh",
"do wr"]
R2 = ["router ospf 1 vrf control-data",
"network  172.31.105.48 0.0.0.15 area 0",
"network  172.31.105.32 0.0.0.15 area 0",
"router-id 2.2.2.2",
"interface GigabitEthernet0/1",
"ip access-group 100 in",
"ip address 172.31.105.33 255.255.255.240",
"no sh",
"interface GigabitEthernet0/2",
"ip address 172.31.105.49 255.255.255.240",
"no sh",
"do wr"]
R3 = ["router ospf 1 vrf control-data",
"network  172.31.105.48 0.0.0.15 area 0",
"router-id 3.3.3.3",
"redistribute static subnets",
"default-information originate",
"access-list 1 permit 172.31.105.0 0.0.0.255",
"ip nat inside source list 1 interface Gi0/2 overload",
"interface GigabitEthernet0/1",
"ip access-group 100 in",
"ip nat inside",
"ip address 172.31.105.62 255.255.255.240",
"no sh",
"interface GigabitEthernet0/2",
"ip nat outside",
"ip address dhcp",
"no sh",
"do wr"]
con = 0
for ip in device_ip:
    con += 1
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username='admin', password='cisco', key_filename='C:/Users/toenteen/Desktop/id_rsa.ppk')
    if con == 1:
        commands = R1
    if con == 2:
        commands = R2
    if con == 3:
        commands = R3
    with client.invoke_shell() as ssh:
        print("Connecting to {}...".format(ip))
        for i in acl:
            ssh.send(i+"\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)
        for i in commands:
            ssh.send(i+"\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)
        