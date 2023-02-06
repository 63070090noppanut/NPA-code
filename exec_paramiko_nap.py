import time
import paramiko

username = 'admin'
password = 'cisco'

device_ip = ["172.31.105.4", "172.31.105.5", "172.31.105.6"]
for ip in device_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username='admin', password='cisco', key_filename='C:/Users/toenteen/Desktop/id_rsa.ppk')
    commands = ["sh ip int bri"]
    for command in commands:
        print("Executing {}".format(command))
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        print("Error : " + stderr.read().decode())
        time.sleep(1)
    client.close()