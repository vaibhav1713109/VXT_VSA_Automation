import pyvisa
import time
import pyvisa_py.protocols.rpc, pyvisa.errors
from SSH_RU import take_SSH
from fpdf import FPDF

def Run_RM():
    try:
        IP_ADDR = '192.168.4.10'
        RM = pyvisa.ResourceManager()
        VSA = RM.open_resource('TCPIP0::{}::inst1::INSTR'.format(IP_ADDR))
        # print(VSA)
        return VSA,RM
    except Exception as e:
        pass

def process_system_error(instrument) :
    bSuccess = True
    EsrErrorMask = 0x3C
    if ((get_esr(instrument) and EsrErrorMask) != 0) :
        print('SYSTEM ERROR : ',instrument.query(":SYST:ERR?"))
        instrument.write("*CLS")
        bSuccess = False

def get_esr(instrument) :
    esr = instrument.query("*ESR?")
    # print(int(esr),'ESR')
    return int(esr)


def VSA_Write_SCPI(INS,Write_List,OUTPUT1):
    for CMD in Write_List:
        try:
            Res = INS.write(CMD)
            status = INS.query('*OPC?')
            li_out = CMD.split(' ')
            try:
                if ':POW:RANG:OPT' in CMD:
                    if len(li_out)>1:
                        stat = INS.query('{}?'.format(li_out[0]))
                        # print(stat)
                        if int(status) != 1:
                            OUTPUT1.append([CMD,status,stat])
                        OUTPUT1.append([CMD,status,stat])
                        # process_system_error(INS)
            except Exception as e:
                OUTPUT1.append([CMD,status,'{}'.format(e)])
                time.sleep(5)
            
        except Exception as e:
            OUTPUT1.append([CMD,'*OPC_FAIL','{}'.format(e)])
            # time.sleep(5)
    return OUTPUT1

def VSA_Query_SCPI(INS,CMD,OUTPUT2):

        try:
            Res = INS.query(CMD)
            Res1 = Res.split(',')
            if CMD == ':CCAR:REF?':
                Res1[0] = str(float(Res1[0]))
            # process_system_error(INS)
            OUTPUT2.append(Res1[0])
        except Exception as e:
            s = str(e).split(':')
            OUTPUT2.append("{}".format(s[1]))
            # time.sleep(3)
        return OUTPUT2


