from textfsm02 import *
device_ip = '172.31.105.4'
username = 'admin'
password = 'cisco'

device_params = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'password': password
}

def test_ip():
    assert get_ip(device_params, 'G0/0') == '172.31.105.4'
    assert get_ip(device_params, 'G0/1') == '172.31.105.17'
    assert get_ip(device_params, 'G0/2') == '172.31.105.46'
    assert get_ip(device_params, 'G0/3') == 'unassigned'

    assert get_des(device_params, 'G0/0') == "Connect to Gi0/0 of S0"
    assert get_des(device_params, 'G0/1') == "Connect to Gi0/1 of S1"
    assert get_des(device_params, 'G0/2') == "Connect to Gi0/2 of R2"
    assert get_des(device_params, 'G0/3') == "Not use admindown"

    assert get_subnet(device_params, 'G0/0') == '/28'
    assert get_subnet(device_params, 'G0/1') == '/28'
    assert get_subnet(device_params, 'G0/2') == '/28'
    assert get_subnet(device_params, 'G0/3') == None

    assert get_status(device_params, 'G0/0') == 'up'
    assert get_status(device_params, 'G0/1') == 'up'
    assert get_status(device_params, 'G0/2') == 'up'
    assert get_status(device_params, 'G0/3') == 'admin down'
#upload to git first

