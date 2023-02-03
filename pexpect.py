import wexpect

prompt = "#"
ip = ['172.31.105.4','172.31.105.5','172.31.105.6' ]
username = "adminn"
password = "cisco"

command = "sh ip int bri"
iploop = 0
for i in ip:
    iploop += 1
    fullip = ((iploop+".")*4).lstrip(".")
    child = wexpect.spawn('telnet ' + i)
    child.expect("Username")
    child.sendline(username)
    child.expect("Password")
    child.sendline(password)
    child.expect(prompt)
    child.sendline("conf t")
    child.sendline("interface loopback 0")
    child.sendline("ip add " + fullip + " 255.255.255.255")
    result = child.before
    print(result.decode('UTF-8'))
    child.sendline("exit")
    child.sendline(command)
