import sys
import time
from ETW_Automation import test_main
from Trigger import VSA_Write_SCPI, VSA_Query_SCPI, Run_RM
import Convert_PDF,RU_Details
import pyvisa_py.protocols.rpc
import pyvisa.errors
from tabulate import tabulate
from RU_Details import CONF



class MAIN_INIT():

    def __init__(self, CH_NOs, filename,freq,trxattenaution) -> None:
        self.filename = filename
        self.CH_NOs = CH_NOs
        self.Test_Mod_str = ''
        self.Test_M_scpi = ''
        self.CH_PW_out1 = []        ######## For write scpi output of CH_PW
        self.CH_PW_out2 = []        ######## For query scpi output of CH_PW
        self.ACLR_OUT1 = []         ######## For Write scpi output of ACLR
        self.ACLR_OUT2 = []         ######## For Query scpi output of ACLR
        self.EVM_OUT1 = []          ######## For Write scpi output of EVM
        self.EVM_OUT2 = []          ######## For Query scpi output of EVM
        self.Write_Cmd = ''
        self.Query_Cmd = ''
        self.ACLR = ''
        self.EVM = ''
        self.freq,self.trxAttenation = freq,trxattenaution
        self.trxID,self.qpamID = 0,0
        # self.frequency = []
        # self.Test_Module_List = []
        # self.Bandwidth = []
        pass


    def Test_Module(self):
        while True:
            print('-'*100)
            el = {'Test_Model':['TM_1.1', 'TM_1.2','TM_2','TM_2a','TM_3.1','TM_3.1a','TM_3.2','TM_3.3']}
            SCPI_Test_model = ['DLTM1DOT1','DLTM1DOT2','DLTM2','DLTM2A','DLTM3DOT1','DLTM3DOT1A','DLTM3DOT2','DLTM3DOT3']
            print(f"{'SR_NO' : <20}{'Test_Module' : <20}{'|' : ^10}{'Value': ^10}")
            print('-'*100)
            j = 1
            for key, vals in el.items():
                for val in vals:
                    print(f"{j : <20}{key : <20}{'=' : ^10}{val: ^10}")
                    j+=1
            print('-'*100)
            
            nm = int(input("Choose Test Model :\n"))
            if nm <= len(el['Test_Model']):
                self.Test_Mod = el['Test_Model'][nm-1]
                self.Test_M_scpi = SCPI_Test_model[nm-1]
                print('-'*100)
                break
            else:
                print('-'*100)
                print('\nPlease Give Correct Input\n')
                print('-'*100)

        ################ SCPI Commands to trigger [Basic Station Log ] ####################
        ############ Commands for write ############
        self.Write_Cmd = [':INIT:CONT ON',':INST:SEL NR5G',':OUTP:STAT OFF',':FEED:RF:PORT:INP RFIN',':CONF:CHP', 
        ':RAD:STAN:PRES:CARR B{}M'.format(RU_Details.CONF['BANDWIDTH']),':RAD:STAN:PRES:FREQ:RANG FR1',':RAD:STAN:PRES:DMOD TDD',':RAD:STAN:PRES:SCS SCS30K', 
        ':RAD:STAN:PRES:RBAL {}'.format(self.Test_M_scpi),':RAD:MIMO 0',':RAD:STAN:PRES:DLIN:BS:CAT ALAR',':SENSe:CCARrier:COUNt 1', 
        ':SENSe:CCARrier:CONFig:ALLocation Contiguous',':SENSe:CCARrier:CONFig:ALLocation:NCONtiguous:ABPoint CC0', 
        ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(RU_Details.CONF['BANDWIDTH']),':SENSe:CCARrier0:STATe ON',':SENSe:CCARrier0:FREQuency:OFFSet 0MHz', 
        ':SENSe:CCARrier0:SPECtrum NORM',':CCAR:REF {}'.format(float(RU_Details.CONF['Freq'])*1000000),':RAD:STAN:PRES:IMM',':RAD:STAN:DIR DLINK', 
        ':CHP:AVER:STAT 0',':POW:RANG 10',':CHP:SAV ON',':SWE:EGAT:SOUR FRAM',':CORR:BTS:GAIN {}'.format(RU_Details.CONF['Cable_Loss']),':OUTP:STAT ON',':POW:RANG:OPT IMM']

        ############ Commands for query ############
        self.Query_Cmd = [':CCAR:REF?',':SENSe:CCARrier0:RADio:STANdard:BANDwidth?']


        ############ ACLR SCPI Commands ###########

        self.ACLR = {'Query' : [':CCAR:REF?',':SENSe:CCARrier0:RADio:STANdard:BANDwidth?'],

        'Writeable' : [':INST:SEL NR5G',':INIT:CONT ON',':OUTP:STAT OFF',':FEED:RF:PORT:INP RFIN',':CONF:ACP', 
        ':RAD:STAN:PRES:CARR B{}M'.format(RU_Details.CONF['BANDWIDTH']),':RAD:STAN:PRES:FREQ:RANG FR1',':RAD:STAN:PRES:DMOD TDD',':RAD:STAN:PRES:SCS SCS30K', 
        ':RAD:STAN:PRES:RBAL {}'.format(self.Test_M_scpi),':RAD:MIMO 0',':RAD:STAN:PRES:DLIN:BS:CAT ALAR',':SENSe:CCARrier:COUNt 1', 
        ':SENSe:CCARrier:CONFig:ALLocation Contiguous',':SENSe:CCARrier:CONFig:ALLocation:NCONtiguous:ABPoint CC0', 
        ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(RU_Details.CONF['BANDWIDTH']),':SENSe:CCARrier0:STATe ON', 
        ':SENSe:CCARrier0:FREQuency:OFFSet 0MHz',':SENSe:CCARrier0:SPECtrum NORM',':CCAR:REF {}'.format(float(RU_Details.CONF['Freq'])*1000000), 
        ':RAD:STAN:PRES:IMM',':INIT:CONT ON',':RAD:STAN:DIR DLINK',':ACP:AVER:STAT 0',':POW:RANG 10', 
        ':ACP:SWE:TIME:AUTO:RUL ACC',':RAD:STAN:DIR DLINK',':RAD:STAN:PRES:DLIN:ACH NR',':ACP:CARR1:PREF:TYPE MPC', 
        ':ACP:CORR:NOIS ON',':RAD:STAN:PRES:IMM',':ACP:SWE:TIME:AUTO:RUL ACC',':RAD:STAN:DIR DLINK', 
        ':RAD:STAN:PRES:DLIN:ACH NR',':ACP:CARR1:PREF:TYPE MPC',':ACP:CORR:NOIS ON',':SWE:EGAT:STATE 1', 
        ':TRIG:FRAM:SYNC RFB',':SWE:EGAT:SOUR FRAM',':SWE:EGAT:LENG 3.7 ms',':SWE:EGAT:DEL 5 ms', 
        ':TRIG:ACP:SOUR IMM',':CORR:BTS:GAIN {}'.format(RU_Details.CONF['Cable_Loss']),':INIT:CONT ON',':INIT:CONT ON', 
        ':INIT:CONT ON',':INIT:IMM',':DISP:FSCR 0',':OUTP:STAT OFF',':POW:RANG:OPT IMM']
        }



        ############ EVM SCPI Commands ###########
        self.EVM = {'Query' : [':CCAR:REF?',':SENSe:CCARrier0:RADio:STANdard:BANDwidth?'],


        'Writeable' : [':INST:SEL NR5G', ':INIT:CONT OFF', ':OUTP:STAT OFF', ':FEED:RF:PORT:INP RFIN', ':CONF:EVM', ':RAD:STAN:PRES:CARR B{}M'.format(RU_Details.CONF['BANDWIDTH']), 
        ':RAD:STAN:PRES:FREQ:RANG FR1', ':RAD:STAN:PRES:DMOD TDD', ':RAD:STAN:PRES:SCS SCS30K', ':RAD:STAN:PRES:RBAL {}'.format(self.Test_M_scpi), 
        ':RAD:MIMO 0', ':RAD:STAN:PRES:DLIN:BS:CAT ALAR', ':SENSe:CCARrier:COUNt 1', ':SENSe:CCARrier:CONFig:ALLocation Contiguous', 
        ':SENSe:CCARrier:CONFig:ALLocation:NCONtiguous:ABPoint CC0', ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(RU_Details.CONF['BANDWIDTH']), 
        ':SENSe:CCARrier0:STATe ON', ':SENSe:CCARrier0:FREQuency:OFFSet 0MHz', ':SENSe:CCARrier0:SPECtrum NORM', ':CCAR:REF {}'.format(float(RU_Details.CONF['Freq'])*1000000), 
        ':RAD:STAN:PRES:IMM', ':INIT:CONT OFF', ':RAD:STAN:DIR DLINK', ':EVM:AVER:STAT 0', ':POW:RANG 10', 
        ':EVM:CCAR0:DC:PUNC ON', ':SWE:EGAT:STATE 0', ':TRIG:EVM:SOUR IMM', 
        ':RAD:STAN:PRES:RBAL {}'.format(self.Test_M_scpi), ':RAD:STAN:PRES:IMM', ':RAD:MIMO 0', ':EVM:CCAR0:PROF:PDSC:AUTO OFF', 
        ':EVM:AVER:STAT 0', ':POW:RANG 10', ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(RU_Details.CONF['BANDWIDTH']), ':SENSe:CCARrier0:STATe ON', 
        ':SENSe:CCARrier0:FREQuency:OFFSet 0MHz', ':SENSe:CCARrier0:SPECtrum NORM', ':CCAR:REF {}'.format(float(RU_Details.CONF['Freq'])*1000000), ':EVM:CCAR0:DC:PUNC ON', 
        ':DISP:EVM:VIEW NORM;', ':DISP:EVM:WIND5:DATA FRES;', ':DISP:EVM:WIND1:DATA MTIM;', ':DISP:EVM:WIND1:Y:PDIV 0.275;',
        ':CORR:BTS:GAIN {}'.format(RU_Details.CONF['Cable_Loss']), ':EVM:AVER:COUN?', ':EVM:AVER:COUN 1', ':INIT:CONT ON', ':POW:RANG:OPT IMM' ]
        }


    ################ Test POWER ###############
    def test_Power(self):
        try:

            ################# Connect The Instrument ##############
            VSA, RM = Run_RM()

            ################# Write SCPI For POWER ##############
            VSA_Write_SCPI(VSA, self.Write_Cmd, self.CH_PW_out1)
            time.sleep(5)

            
            ################# QUERY For POWER ##############
            for CMD in self.Query_Cmd:
                VSA_Query_SCPI(VSA, CMD, self.CH_PW_out2)

            Res = VSA_Query_SCPI(VSA, ':FETC:CHP?', self.CH_PW_out2)
            Flag = 'Fail'
            self.CH_PW_out2[-1] = float(self.CH_PW_out2[-1])
            if type(Res[-1]) != str:
                self.CH_PW_out2[-1] = str(self.CH_PW_out2[-1])
                ################# Verify Power Output ##############
                ########## Change the power from RU Details ############
                if float(Res[-1]) > 23 and float(Res[-1]) < 25:
                    Flag = 'Pass'
                else:
                    Flag = 'Fail'
            self.CH_PW_out2.append(Flag)
            return self.CH_PW_out1, self.CH_PW_out2


        except Exception as e:
            print('{} CH_PW'.format(e))
            li = str(e).split(':')
            self.CH_PW_out2.append('{}'.format(li[1][0:23]))
            self.CH_PW_out2.append('Fail')
            return self.CH_PW_out1, self.CH_PW_out2

    def ACLR_CAL(self, INS, OUTPUT):

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

    def test_ACLR(self):
        try:

            ################# Connect The Instrument ##############
            VSA, RM = Run_RM()

            ################# Write SCPI For ACLR ##############
            VSA_Write_SCPI(VSA, self.ACLR['Writeable'])
            time.sleep(5)

            ################# Query For ACLR ##############
            ## [Frequency, Bandwidth, ACLR] ##
            for CMD in self.ACLR['Query']:
                VSA_Query_SCPI(VSA, CMD, self.ACLR_OUT2)
            Res1 = self.ACLR_CAL(VSA, self.ACLR_OUT2)

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
            self.ACLR_OUT2.append(flag)
            self.ACLR_OUT1, self.ACLR_OUT2

        except Exception as e:
            print('{} ACLR'.format(e))
            li = str(e).split(':')
            self.ACLR_OUT2.append('{}'.format(li[1][0:23]))
            self.ACLR_OUT2.append('Fail')
            return self.ACLR_OUT1, self.ACLR_OUT2

    def EVM_CAL(self, INS, OUTPUT):

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

    def test_EVM(self):
        try:

            ################# Connect The Instrument ##############
            VSA, RM = Run_RM()

            ################# Write SCPI For ACLR ##############
            VSA_Write_SCPI(VSA, self.EVM['Writeable'])

            ################# Query For EVM ##############
            for CMD in self.EVM['Query']:
                VSA_Query_SCPI(VSA, CMD, self.EVM_OUT2)
            Res1 = self.EVM_CAL(VSA, self.EVM_OUT2)

            ################# Verify EVM Output ##############
            flag = 'Fail'
            if float(Res1[-1]) < 4.5:
                flag = 'Pass'
                pass
            else:
                flag = 'Fail'
                pass

            self.EVM_OUT2.append(flag)
            self.EVM_OUT1, self.EVM_OUT2


        except Exception as e:
            print('{} EVM_CAL'.format(e))
            li = str(e).split(':')
            self.EVM_OUT2.append('{}'.format(li[1][1:23]))
            self.EVM_OUT2.append('Fail')
            return self.EVM_OUT1, self.EVM_OUT2

    ################ Test Power and ACLR ###############
    def Result_Declare(self, Test_Module):
        CHANNEL_POWER_DATA = []
        ACLR_DATA = []
        EVM_DATA = []
        FREQUENCY_DATA = []
        TC_Result = []
        try:
            for CH_NO in range(1, int(self.CH_NOs)+1):
                # test_main(CH_NO-1,self.freq,Test_Module,self.trxAttenation,self.trxID,self.qpamID)                
                ################# Channel Power Result ##############
                Power_Scpi, RES1 = self.test_Power()
                CHANNEL_POWER_DATA.append(RES1)
                RES1.insert(0, str(CH_NO))
                RES1.insert(3, Test_Module)
                RES1.insert(5, CONF['Power_Range'][0])
                RES1.insert(6, CONF['Power_Range'][1])

                time.sleep(10)

                ################# ACLR Result ##############
                ACLR_Scpi, RES2 = self.test_ACLR()
                ACLR_DATA.append(RES2)
                RES2.insert(0, str(CH_NO))
                RES2.insert(3, Test_Module)
                RES2.insert(8, CONF['ACP_Limit'])
                time.sleep(10)

                ################# EVM Result ##############
                EVM_Scpi, RES3 = self.test_EVM()
                EVM_DATA.append(RES3)
                RES3.insert(0, str(CH_NO))
                RES3.insert(3, Test_Module)
                RES3.insert(5, CONF['EVM_Limit'])
                time.sleep(10)

                print(CHANNEL_POWER_DATA)
                print(ACLR_DATA)
                print(EVM_DATA)

                Channel_Change = input(
                    'Change the Channel and Press \'N/n\' for next channel: ')
                if Channel_Change == 'N' or Channel_Change == 'n':
                    pass
                else:
                    break
                self.trxID = CH_NO//2
                self.qpamID = CH_NO//4


            flag_CH_PW = True
            ################## CHANNEL_POWER_DATA ##################
            for data in CHANNEL_POWER_DATA:
                if data[-1] == 'Pass':
                    # data[-1] = 'Pass'
                    flag_CH_PW = flag_CH_PW & True
                else:
                    # data[-1] = 'Fail'
                    flag_CH_PW = flag_CH_PW & False
            if flag_CH_PW:
                TC_Result.append(
                    ['1', 'Base station output power', 'Pass'])
            else:
                TC_Result.append(['1', 'CHANNEL_POWER_DATA', 'Fail'])

            flag_ACLR = True
            ################## 'Adjacent Channel Leakage Power Ratio' ##################
            for data in ACLR_DATA:
                if data[-1] == 'Pass':
                    # data[-1] = 'Pass'
                    flag_ACLR = flag_ACLR & True
                else:
                    # data[-1] = 'Fail'
                    flag_ACLR = flag_ACLR & False
            if flag_ACLR:
                TC_Result.append(
                    ['2', 'Adjacent Channel Leakage Power Ratio', 'Pass'])
            else:
                TC_Result.append(
                    ['2', 'Adjacent Channel Leakage Power Ratio', 'Fail'])

            flag_EVM = True
            ################## EVM_DATA ##################
            for data in EVM_DATA:
                if data[-1] == 'Pass':
                    # data[-1] = 'Pass'
                    flag_EVM = flag_EVM & True
                else:
                    # data[-1] = 'Fail'
                    flag_EVM = flag_EVM & False
            if flag_EVM:
                TC_Result.append(['3', 'EVM_DATA', 'Pass'])
            else:
                TC_Result.append(['3', 'EVM_DATA', 'Fail'])

            

            flag = flag_CH_PW & flag_ACLR & flag_EVM
            TC_Result.append(flag)
    
        except pyvisa_py.protocols.rpc.RPCError as e:
            print("########### can't connect to server ############")
            print('{}'.format(e))

        except pyvisa.errors.VisaIOError as e:
            print("########### Insufficient location ############")
            print('{}'.format(e))
        
        except Exception as e:
            print('{}'.format(e))

        return [CHANNEL_POWER_DATA, ACLR_DATA, EVM_DATA, TC_Result]

    def Result(self):
        PDF = Convert_PDF.PDF_CAP()
        PDF.add_page(format=(350, 250))
        PDF.set_font("Times", size=12)
        PDF.set_font_size(float(10))
        Header_H = PDF.font_size * 2.5
        line_height = PDF.font_size * 3.5


        self.Test_Module()
        data = self.Result_Declare(self.Test_Mod_str)
        print(data)
        Base_station_output_power, ACLR, Modulation_quality, TC_Result = data[
            0], data[1], data[2], data[3]

        flag = TC_Result[-1]
        TC_Result.pop()



        ###################################### Test report verdict overview ####################################
        if flag:
            TC_Result.append(['', 'Overall test verdict ', 'Pass'])
        else:
            TC_Result.append(['', 'Overall test verdict ', 'Fail'])

        Convert_PDF.HEADING(PDF, '\nTest report verdict overview \n')
        table_Header = ['Test Case ID', 'Description', 'verdict']
        print(tabulate(TC_Result, headers=table_Header, tablefmt='fancy_grid'))
        Convert_PDF.render_header(
            PDF, table_Header, Header_H, PDF.epw / len(table_Header))
        Convert_PDF.render_table_data(
            PDF, TC_Result, line_height, PDF.epw / len(table_Header), table_Header)

        


        ################################### Base station output power- Test results #######################################
        PDF.add_page(format=(350, 250))
        print('\n\n\n')
        CH_POWER_Header = ['Channel No', 'Channel Frequency [Hz]', 'BS Channel Bandwidth BW [MHz]',
                           'Test Channel Model', 'Output Power [dbm]', 'Limit Low [dBm]', 'High Low [dBm]', 'Verdict']
        Convert_PDF.HEADING(
            PDF, '\nBase station output power- Test results:\n')
        Convert_PDF.Test_HEADING(
            PDF, '''Test purpose : \nThe test purpose is to verify the accuracy of the maximum carrier output power across the frequency range and under normal and extreme conditions''')
        Convert_PDF.Test_HEADING(
            PDF, 'Test environment : \nNormal and Extreme test conditions.')
        Convert_PDF.Test_HEADING(PDF, 'NR FR1 test model: \n{}'.format(
            Base_station_output_power[0][3]))
        print(tabulate(Base_station_output_power,
              headers=CH_POWER_Header, tablefmt='fancy_grid'))
        Convert_PDF.render_header(
            PDF, CH_POWER_Header, line_height, PDF.epw / len(CH_POWER_Header))
        Convert_PDF.render_table_data(
            PDF, Base_station_output_power, line_height, PDF.epw / len(CH_POWER_Header), CH_POWER_Header)

        

        
        ################################### Adjacent Channel Leakage Power Ratio (ACLR) - Test results: #######################################
        PDF.add_page(format=(350, 250))
        print('\n\n\n')
        ACLR_Header = ['Channel No', 'Channel Frequency [Hz]', 'BS Channel Bandwidth BW [MHz]', 'Test Channel Model',
                       'Low ACLR [dB]', 'High ACLR [dB]', 'Low 2xBW ACLR [dB]', 'High 2xBW ACLR [dB]', 'ACLR Limit [dB]', 'Verdict']
        Convert_PDF.HEADING(
            PDF, '\n Adjacent Channel Leakage Power Ratio (ACLR) - Test results: \n')
        Convert_PDF.Test_HEADING(
            PDF, '''Test purpose : \nTo verify that the adjacent channel leakage ratio requirement shall be met as specified by the minimum requirement.''')
        Convert_PDF.Test_HEADING(
            PDF, 'Test environment : \nNormal test conditions.')
        Convert_PDF.Test_HEADING(
            PDF, 'NR FR1 test model: \n{}'.format(ACLR[0][3]))
        print(tabulate(ACLR, headers=ACLR_Header, tablefmt='fancy_grid'))
        Convert_PDF.render_header(
            PDF, ACLR_Header, line_height, PDF.epw / len(ACLR_Header))
        Convert_PDF.render_table_data(
            PDF, ACLR, line_height, PDF.epw / len(ACLR_Header), ACLR_Header)

        
        
        
        #################################  Modulation quality - Test results: #########################################
        PDF.add_page(format=(350, 250))
        print('\n\n\n')
        Convert_PDF.HEADING(PDF, '\n Modulation quality - Test results: \n')
        EVM_Header = ['Channel No', 'Channel Frequency [Hz]', 'BS Channel Bandwidth BW [MHz]',
                      'Test Channel Model', 'Measured EVM (RMS) [%]', 'EVM Limit [%]', 'Verdict']
        Convert_PDF.Test_HEADING(
            PDF, '''Test purpose : \nThe test purpose is to verify the modulation quality''')
        Convert_PDF.Test_HEADING(
            PDF, 'Test environment : \nNormal test conditions.')
        Convert_PDF.Test_HEADING(
            PDF, 'NR FR1 test model: \n{}'.format(Modulation_quality[0][3]))
        print(tabulate(Modulation_quality, headers=EVM_Header, stralign='left',
              maxcolwidths=[10, 10, 10, 10, 10, 10, 10], tablefmt='fancy_grid'))
        Convert_PDF.render_header(
            PDF, EVM_Header, line_height, PDF.epw / len(EVM_Header))
        Convert_PDF.render_table_data(
            PDF, Modulation_quality, line_height, PDF.epw / len(EVM_Header), ACLR_Header)

        PDF.output('{}.pdf'.format(self.filename))



if __name__ == "__main__":
    try:
        CH_NOs = input('Number of Channel in RU For Transmission: ')
        obj = MAIN_INIT(CH_NOs,sys.argv[1],sys.argv[2], sys.argv[3])
        obj.Result()
    except Exception as e:
        print(f'{e}')
        print('Usage: python ETW_Automation.py <filename> <frequency> <trxAttenaution>')

