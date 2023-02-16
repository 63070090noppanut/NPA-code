import jinja2
from netmiko import ConnectHandler

jinja_template = 'template1.j2'
inv_list = [ {'device' : '172.31.105.4',
    'Gi00' : 'Connect to Gi0/0 of S0',
    'Gi01' : 'Connect to Gi0/1 of S1',
    'Gi02' : 'Connect to Gi0/2 of R2',
    'Gi03' : 'Not use admin down'},
    {'device' : '172.31.105.5',
    'Gi00' : 'Connect to Gi0/0 of S0',
    'Gi01' : 'Connect to Gi0/1 of R1',
    'Gi02' : 'Connect to Gi0/2 of R3',
    'Gi03' : 'Not use admin down'},
    {'device' : '172.31.105.6',
    'Gi00' : 'Connect to Gi0/0 of S0',
    'Gi01' : 'Connect to Gi0/1 of R2',
    'Gi02' : 'Connect to WAN',
    'Gi03' : 'Not use admin down'},
]
username = 'admin'
password = 'cisco'

for items in inv_list:
    print('\nCurrent device: ' + items['device'])
    with open(jinja_template) as f:
        tfile = f.read()
    template = jinja2.Template(tfile)
    cfg_list = template.render(items).split('\n')
    print(cfg_list)
    device_params = {
    'device_type': 'cisco_ios',
    'ip': items['device'],
    'username': username,
    'password': password
}
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_config_set(cfg_list)
        print(result)