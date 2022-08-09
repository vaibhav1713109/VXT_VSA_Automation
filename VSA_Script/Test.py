import sys

class MAIN_INIT():

    def __init__(self, CH_NOs, filename,freq,trxattenaution) -> None:
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
        self.filename = filename


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


    def Result_Declare(self):
        self.Test_Module()
        for CH_NO in range(1, int(self.CH_NOs)+1):
            print(CH_NO-1,self.freq,self.Test_Mod_str,self.trxAttenation,self.trxID,self.qpamID)
            self.trxID = CH_NO//2
            self.qpamID = CH_NO//4
            Channel_Change = input(
                    'Change the Channel and Press \'N/n\' for next channel')
            if Channel_Change == 'N' or Channel_Change == 'n':
                pass
            else:
                break


if __name__ == "__main__":
    try:
        CH_NOs = input('Number of Channel in RU For Transmission: ')
        obj = MAIN_INIT(CH_NOs,sys.argv[1],sys.argv[2], sys.argv[3])
        obj.Result_Declare()
    except Exception as e:
        print(f'{e}')
        print('Usage: python ETW_Automation.py <filename> <frequency> <trxAttenaution>')
