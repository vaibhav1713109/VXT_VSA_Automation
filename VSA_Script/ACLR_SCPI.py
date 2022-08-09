from Trigger import VSA_Write_SCPI, VSA_Query_SCPI,Run_RM
import DATA
import time
from tabulate import tabulate
import pyvisa_py.protocols.rpc, pyvisa.errors
import Convert_PDF

def ACLR_CAL(INS,OUTPUT):
    
    try:
        Res = INS.query(':FETC:ACP?')
        OUT = Res.split(',')
        OUTPUT.append(str(float(OUT[4])))
        OUTPUT.append(str(float(OUT[6])))
        OUTPUT.append(str(float(OUT[8])))
        OUTPUT.append(str(float(OUT[10])))
    except Exception as e:
        s = str(e).split(':')
        OUTPUT.append("{}".format(s[1]))
        # time.sleep(3)
    return OUTPUT


def test_ACLR():
    OUTPUT1 = []        #### For SCPI Write
    OUTPUT2 = []        #### For Query Only
    OUTPUT3 = []        #### For ACLR  Only
    # CH_NO = input('Enter Channel No : ')
    try:
        # CMD = "cd /etc/init.d/THERMAL_TEST_SCRIPT; ./test_5gnr.sh {}".format(CH_NO)
        # take_SSH('192.168.1.10','root','root',CMD)
        
        ################# Connect The Instrument ##############
        VSA, RM = Run_RM()


        ################# Write SCPI For ACLR ##############
        VSA_Write_SCPI(VSA,DATA.ACLR['Writeable'],OUTPUT1)
        time.sleep(5)


        ################# Query For ACLR ##############
        ## [Frequency, Bandwidth, ACLR] ##
        for CMD in DATA.ACLR['Query']:
            VSA_Query_SCPI(VSA,CMD,OUTPUT2)
        Res1 = ACLR_CAL(VSA,OUTPUT2)


        ################# Verify ACLR Output ##############
        if type(Res1) == list:
            if type(Res1[2]) == str:
                flag = 'Fail'
            if float(Res1[2]) < -43.8 and float(Res1[3]) < -43.8 and float(Res1[4]) < -43.8 and float(Res1[5]) < -43.8:
                flag = 'Pass'
            else:
                flag = 'Fail'
        else:
            flag = 'Fail'
        # print([Res1[-3:-1],Res2[-3:-1]])
        OUTPUT2.append(flag)
        return OUTPUT1,OUTPUT2

    except pyvisa_py.protocols.rpc.RPCError as e:
        print("########### can't connect to server ############")
        print('{}'.format(e))

    except pyvisa.errors.VisaIOError as e:
        print("########### Insufficient location ############")
        print('{}'.format(e))



if __name__ == "__main__":
    test_ACLR()
