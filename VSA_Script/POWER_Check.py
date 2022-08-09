import time
from Trigger import VSA_Write_SCPI, VSA_Query_SCPI,Run_RM
import DATA
import pyvisa_py.protocols.rpc, pyvisa.errors

    



################ Test POWER ###############

def test_Power():
    OUTPUT1 = []    ### For Write
    OUTPUT2 = []    ### For Query
    try:

        ################# Connect The Instrument ##############
        VSA, RM = Run_RM()


        ################# Write SCPI For POWER ##############
        VSA_Write_SCPI(VSA,DATA.Write_Cmd,OUTPUT1)
        time.sleep(5)


        ################# Write QUERY For POWER ##############
        for CMD in DATA.Query_Cmd:
            VSA_Query_SCPI(VSA,CMD,OUTPUT2)
            
        Res = VSA_Query_SCPI(VSA,':FETC:CHP?',OUTPUT2)
        Flag = 'Fail'
        OUTPUT2[-1] = float(OUTPUT2[-1])
        if type(Res[-1])!=str:
            OUTPUT2[-1] = str(OUTPUT2[-1])
            ################# Verify Power Output ##############
            ########## Change the power from RU Details ############
            if float(Res[-1])> 23 and float(Res[-1])< 25:
                Flag = 'Pass'
            else:
                Flag = 'Fail'
        OUTPUT2.append(Flag)
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



