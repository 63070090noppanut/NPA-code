from netmiko import ConnectHandler
from pprint import pprint
import re

device_ip = '172.31.105.6'
username = 'admin'
password = 'cisco'

def get_data_from_device(device_params):
        with ConnectHandler(**device_params) as ssh:
            result_shipinbt = ssh.send_command('sh ip int br', use_textfsm=True)
            result_shintdes = ssh.send_command('sh int descr', use_textfsm=True)
            result_shiproutemanage = ssh.send_command('sh ip route vrf management | include ^C', use_textfsm=True)
            result_shiproutecontrol = ssh.send_command('sh ip route vrf control-data | include ^C', use_textfsm=True)
            result_shcdpnei = ssh.send_command('sh cdp nei', use_textfsm=True)
            allinfo = result_shipinbt, result_shintdes, result_shiproutemanage, result_shiproutecontrol,result_shcdpnei
            return allinfo

def get_ip(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[0]

    for line in result:
        if line["intf"][0] == intf[0] and line["intf"][-3:] == intf[-3:]:
             return line["ipaddr"] 
        
def get_subnet(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[2].strip().split('\n')
    result1 = data[3].strip().split('\n')
    for line in result[1:]:
        intf_info = re.search(r'\S+\s+\d+.\d+.\d+.\d+(.\d+)[a-z, ^\,]*(.*)', line)
        if intf[0] in intf_info.group(2) and intf_info.group(2)[-3:] == intf[-3:]:
            return intf_info.group(1)
    for line in result1[1:]:
        intf_info = re.search(r'\S+\s+\d+.\d+.\d+.\d+(.\d+)[a-z, ^\,]*(.*)', line)
        if intf[0] in intf_info.group(2) and intf_info.group(2)[-3:] == intf[-3:]:
            return intf_info.group(1)
        
def get_des(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[1]
    for line in result:
        if intf[0] in line["port"] and intf[-3:] in line["port"]:
            line["descrip"] = line["descrip"].replace("admin down", "admindown")
            return line["descrip"]
        
def get_status(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[1]
    for line in result:
        if line["port"][0] == intf[0] and line["port"][-3:] == intf[-3:]:
            if intf[0] in line["port"] and line["status"] == 'admin down':
                return 'admin down'
            if intf[0] in line["port"] and line["status"] == 'down':
                return 'down'
            if intf[0] in line["port"] and line["status"] == 'up':
                return 'up'
            
if __name__ == '__main__':
    device_params = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': username,
        'password': password
    }
    print(get_des(device_params, 'G0/0'))
    print(get_des(device_params, 'G0/1'))
    print(get_des(device_params, 'G0/2'))
    print(get_des(device_params, 'G0/3'))
    # print(get_subnet(device_params, 'G0/1'))
    # print(get_subnet(device_params, 'G0/2'))
    # print(get_subnet(device_params, 'G0/3'))


    