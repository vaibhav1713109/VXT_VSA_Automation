import time
from ACLR_SCPI import test_ACLR
from EVM_Test import test_EVM
from POWER_Check import test_Power
from RU_Details import CONF
import pyvisa_py.protocols.rpc, pyvisa.errors




################ Test Power and ACLR ###############
def Result_Declare(CH_NOs): 
    Test_Module = 'NR_TM_3.1a' 
    CHANNEL_POWER_DATA = []
    ACLR_DATA = []
    EVM_DATA = []
    FREQUENCY_DATA = []
    TC_Result = []
    try:
        for CH_NO in range(1,int(CH_NOs)+1):
            ################# Channel Power Result ##############
            Power_Scpi,RES1 = test_Power()
            CHANNEL_POWER_DATA.append(RES1)
            RES1.insert(0,str(CH_NO))
            RES1.insert(3,Test_Module)
            RES1.insert(5,CONF['Power_Range'][0])
            RES1.insert(6,CONF['Power_Range'][1])
            time.sleep(10)

            ################# ACLR Result ##############
            ACLR_Scpi,RES2 = test_ACLR()
            ACLR_DATA.append(RES2)
            RES2.insert(0,str(CH_NO))
            RES2.insert(3,Test_Module)
            RES2.insert(8,CONF['ACP_Limit'])
            time.sleep(10)

            ################# EVM Result ##############
            EVM_Scpi,RES3 = test_EVM()
            EVM_DATA.append(RES3)
            RES3.insert(0,str(CH_NO))
            RES3.insert(3,Test_Module)
            RES3.insert(5,CONF['EVM_Limit'])
            time.sleep(10)


            ################## For Checking Data list ##################
            # print(CHANNEL_POWER_DATA)
            # print(ACLR_DATA)
            # print(EVM_DATA)


            Channel_Change = input('Change the Channel and Press (\'N/n\') for next channel : ')
            if Channel_Change == 'N' or Channel_Change == 'n':
                pass
            else:
                break

            

        flag_CH_PW = True
        ################## CHANNEL_POWER_DATA ##################
        for data in CHANNEL_POWER_DATA:
            data[1] = str(float(data[1]))
            data[2] = data[2][1:-2]
            if data[-1] == 'Pass':
                # data[-1] = 'Pass'
                flag_CH_PW = flag_CH_PW & True
            else:
                # data[-1] = 'Fail'
                flag_CH_PW = flag_CH_PW & False
        if flag_CH_PW:
            TC_Result.append(['1','Base station output power','Pass'])
        else:
            TC_Result.append(['1','CHANNEL_POWER_DATA','Fail'])

        flag_ACLR = True
        ################## 'Adjacent Channel Leakage Power Ratio' ##################
        for data in ACLR_DATA:
            data[1] = str(float(data[1]))
            data[2] = data[2][1:-2]
            if data[-1] == 'Pass':
                # data[-1] = 'Pass'
                flag_ACLR = flag_ACLR & True
            else:
                # data[-1] = 'Fail'
                flag_ACLR = flag_ACLR & False
        if flag_ACLR:
            TC_Result.append(['2','Adjacent Channel Leakage Power Ratio','Pass'])
        else:
            TC_Result.append(['2','Adjacent Channel Leakage Power Ratio','Fail'])

        flag_EVM = True
        ################## EVM_DATA ##################
        for data in EVM_DATA:
            data[1] = str(float(data[1]))
            data[2] = data[2][1:-2]
            if data[-1] == 'Pass':
                # data[-1] = 'Pass'
                flag_EVM = flag_EVM & True
            else:
                # data[-1] = 'Fail'
                flag_EVM = flag_EVM & False
        if flag_EVM:
            TC_Result.append(['3','EVM_DATA','Pass'])
        else:
            TC_Result.append(['3','EVM_DATA','Fail'])
        
        
        flag = flag_CH_PW & flag_ACLR & flag_EVM
        TC_Result.append(str(flag))

        
    except pyvisa_py.protocols.rpc.RPCError as e:
        print("########### can't connect to server ############")
        print('{}'.format(e))

    except pyvisa.errors.VisaIOError as e:
        print("########### Insufficient location ############")
        print('{}'.format(e))
    
    except Exception as e:
        print('{}'.format(e))

    


    return [CHANNEL_POWER_DATA,ACLR_DATA,EVM_DATA,TC_Result]


if __name__ == "__main__":
    Result_Declare()
