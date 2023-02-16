from netmiko import ConnectHandler
import re
def get_data_from_device(device_params):
    with ConnectHandler(**device_params) as ssh:
        result_shipinbt = ssh.send_command('sh ip int br')
        result_shintdes = ssh.send_command('sh int descr')
        result_shiproutemanage = ssh.send_command('sh ip route vrf management | include ^C')
        result_shiproutecontrol = ssh.send_command('sh ip route vrf control-data | include ^C')
        result_shcdpnei = ssh.send_command('sh cdp nei')
        allinfo = result_shipinbt, result_shintdes, result_shiproutemanage, result_shiproutecontrol,result_shcdpnei
        return allinfo

def get_ip(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[0].strip().split('\n')
    for line in result[1:]:
        intf_info = re.search(r'(\D*)(\S+)\s*(\S*)\s*.*', line)
        if intf[0] in intf_info.group(1) and intf_info.group(2) == intf[-3:]:
             return intf_info.group(3)
        
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
    result = data[1].strip().split('\n')
    for line in result[1:]:
        line = line.replace('admin down', "admindown")
        intf_info = re.search(r"(\S*)\s*(\S*)\s*(\S*)\s*(.*)", line)
        if intf[0] in intf_info.group(1)[0] and intf[-3:] in intf_info.group(1):
            return intf_info.group(4)
        
def get_status(device_params, intf):
    data = get_data_from_device(device_params)
    result = data[1].strip().split('\n')
    for line in result[1:]:
        intf_info = re.search(r"(\S*)\s*(\S*)\s*(\S*)\s*(.*)", line)
        if intf_info.group(1)[0] == intf[0] and intf_info.group(1)[-3:] == intf[-3:]:
            if intf[0] in intf_info.group(1) and intf_info.group(2) == 'admin':
                return 'admin down'
            if intf[0] in intf_info.group(1) and intf_info.group(2) == 'down':
                return 'down'
            if intf[0] in intf_info.group(1) and intf_info.group(2) == 'up':
                return 'up'

        
if __name__ == '__main__':
    device_ip = '172.31.105.4'
    username = 'admin'
    password = 'cisco'

    device_params = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': username,
        'password': password
    }

    print(get_subnet(device_params, 'G0/0'))
    print(get_subnet(device_params, 'G0/1'))
    print(get_subnet(device_params, 'G0/2'))
    print(get_subnet(device_params, 'G0/3'))

#     Python has special designations for character sets:
# - \d - any digit
# - \D - any non-numeric value
# - \s - whitespace character
# - \S - all except whitespace characters
# - \w - any letter, digit or underline character
# - \W - all except letter, digit or underline character

# Repeating character sets:
# - regex+ - one or more repetitions of preceding element
# - regex* - zero or more repetitions of preceding element
# - regex? – zero or one repetition of preceding element
# - regex{n} - exactly n repetitions of preceding element
# - regex{n,m} - from n to m repetitions of preceding element
# - regex{n,} - n or more repetitions of preceding element

# Special symbols
# - . - any character except new line character
# - ^ - beginning of line
# - $ - end of line
# - [abc] - any symbol in square brackets
# - [^abc] - any symbol except those in square brackets
# - a|b - element a or b
# - (regex) - expression is treated as one element. In addition, substring that matches an expression is memorized

# print(match.group(0))
# print(match.group(1))
# print(match.group(2))
# print(match.group(3))