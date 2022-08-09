import os,sys
import time
from defer import return_value
import paramiko
# from rru_init_port_1 import main



def take_SSH(host,user,pswrd,CMD):
    flag = False
    try:
        host = host
        port = 22
        username = user
        password = pswrd

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        for command in CMD:
            try:
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.readlines()
            except Exception as e:
                return '{}'.format(e)
        flag = True

    except Exception as e:
        flag = False
        print('{}'.format(e))
    return flag




def check_ping(hostname):
    iter1 = 0
    while(iter1 <= 2):
        iter1 += 1
        response = os.system("ping -c 1 " + hostname)
        if response == 0:
            pingstatus = 0
            print("Pinging ip {0}".format(hostname))
            return response
        else :
            pingstatus = 1
            print("--------- Not able to ping-----------")
    return pingstatus



ip_addr = "192.168.1.10"
def test_main(channelNumber, frequency, testModel, trxAttenuation, trxID, qpamId) :

    ret = check_ping(ip_addr)
    if ret == 0:
        print("Ping successful")
    else :
        print("Not able to ping")
        return False
    
    
    ################### [Plconfig, Internal_1PPS1, Internal_1PPS2, Internal_External_1PPS] ###################
    commands = ['fpgautil -b /lib/firmware/xilinx/base/MAVU_8T8R_TRX_oran_8t8r_top.bit.bin -o /lib/firmware/xilinix/base/base.dtbo',
    'poke 0xa0140068 0x1','poke 0xa01b0014 0x0','poke 0xa01b0014 0x1']

    # Result = take_SSH(ip_addr,'root','root',commands)
    Result = True
    if Result == True:
        # main(channelNumber, frequency, testModel, trxAttenuation, trxID, qpamId, ipcLink=None)
        pass

    else:
        print('Not able to run script in ')
        return False

    
    


if __name__ == "__main__":
    try:
        test_main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    except Exception as e:
        print(f'{e}')
        print('Usage: python ETW_Automation.py <channelNumber> <frequency> <testModel> <trxAttenuation> <trxID> <qpamId>')

