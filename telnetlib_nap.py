import getpass
import telnetlib
import time

ip = '172.31.105.4'
username = "adminn"
password = getpass.getpass()

tn = telnetlib.Telnet(ip, 23, 5)

tn.read_until(b"Username:")
tn.write(username.encode('ascii') + b'\n')
time.sleep(1)
tn.read_until(b"Password:")
tn.write(password.encode('ascii') + b'\n')
time.sleep(1)
tn.write(b"show ip int bri\n")
time.sleep(2)
tn.write(b"conf t\n")
time.sleep(2)
tn.write(b"int giga 0/1\n")
time.sleep(2)
tn.write(b"ip add 172.31.105.17 255.255.255.240\n")
time.sleep(2)
tn.write(b"no sh\n")
time.sleep(2)
tn.write(b"exit\n")
time.sleep(1)

output = tn.read_very_eager()
print(output.decode('ascii'))
tn.close()
