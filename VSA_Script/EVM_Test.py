from Trigger import VSA_Write_SCPI, VSA_Query_SCPI,Run_RM
import DATA
from tabulate import tabulate
import pyvisa_py.protocols.rpc, pyvisa.errors
import Convert_PDF



def EVM_CAL(INS,OUTPUT):
    
    try:
        CMD = ':FETCh:EVM000001?'
        Res = INS.query(CMD)
        OUT = Res.split(',')
        OUTPUT.append(str(float(OUT[1])))
        # OUTPUT.append(str(float(OUT[3])))
        pass
    except Exception as e:
        s = str(e).split(':')
        OUTPUT.append("{}".format(s[1]))
        # time.sleep(3)
    return OUTPUT


def test_EVM():
    OUTPUT1 = []        #### For SCPI Write
    OUTPUT2 = []        #### For Query Only
    try:
        
        ################# Connect The Instrument ##############
        VSA, RM = Run_RM()


        ################# Write SCPI For ACLR ##############
        VSA_Write_SCPI(VSA,DATA.EVM['Writeable'],OUTPUT1)


        ################# Query For EVM ##############
        for CMD in DATA.ACLR['Query']:
            VSA_Query_SCPI(VSA,CMD,OUTPUT2)
        Res1 = EVM_CAL(VSA,OUTPUT2)
        # print(Res1)


        ################# Verify EVM Output ##############
        flag = 'Fail'
        if float(Res1[-1]) < 4.5:
            flag = 'Pass'
            pass
        else:
            flag = 'Fail'
            pass

        OUTPUT2.append(flag)
        return OUTPUT1,OUTPUT2

    except pyvisa_py.protocols.rpc.RPCError as e:
        print("########### can't connect to server ############")
        print('{}'.format(e))
        OUTPUT2.append('{}'.format(e))
        OUTPUT2.append('Fail')
        return OUTPUT1,OUTPUT2

    except pyvisa.errors.VisaIOError as e:
        print("########### Insufficient location ############")
        print('{}'.format(e))
        OUTPUT2.append('{}'.format(e))
        OUTPUT2.append('Fail')
        return OUTPUT1,OUTPUT2
    
    except Exception as e:
        print('{}'.format(e))
        OUTPUT2.append('{}'.format(e))
        OUTPUT2.append('Fail')
        return OUTPUT1,OUTPUT2





if __name__ == "__main__":
    test_EVM()
