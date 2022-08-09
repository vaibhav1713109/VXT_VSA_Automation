import RU_Details





################ SCPI Commands to trigger [Basic Station Log ] ####################
############ Commands for write ############
Write_Cmd = [':INIT:CONT ON',':INST:SEL NR5G',':OUTP:STAT OFF',':FEED:RF:PORT:INP RFIN',':CONF:CHP', 
':RAD:STAN:PRES:CARR B{}M'.format(RU_Details.CONF['BANDWIDTH']),':RAD:STAN:PRES:FREQ:RANG FR1',':RAD:STAN:PRES:DMOD TDD',':RAD:STAN:PRES:SCS SCS30K', 
':RAD:STAN:PRES:RBAL {}'.format(RU_Details.CONF['Test_Model'][1]),':RAD:MIMO 0',':RAD:STAN:PRES:DLIN:BS:CAT ALAR',':SENSe:CCARrier:COUNt 1', 
':SENSe:CCARrier:CONFig:ALLocation Contiguous',':SENSe:CCARrier:CONFig:ALLocation:NCONtiguous:ABPoint CC0', 
':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(RU_Details.CONF['BANDWIDTH']),':SENSe:CCARrier0:STATe ON',':SENSe:CCARrier0:FREQuency:OFFSet 0MHz', 
':SENSe:CCARrier0:SPECtrum NORM',':CCAR:REF {}'.format(float(RU_Details.CONF['Freq'])*1000000),':RAD:STAN:PRES:IMM',':RAD:STAN:DIR DLINK', 
':CHP:AVER:STAT 0',':POW:RANG 10',':CHP:SAV ON',':SWE:EGAT:SOUR FRAM',':CORR:BTS:GAIN {}'.format(RU_Details.CONF['Cable_Loss']),':OUTP:STAT ON',':POW:RANG:OPT IMM']

############ Commands for query ############
Query_Cmd = [':CCAR:REF?',':SENSe:CCARrier0:RADio:STANdard:BANDwidth?']








############ ACLR SCPI Commands ###########

ACLR = {'Query' : [':CCAR:REF?',':SENSe:CCARrier0:RADio:STANdard:BANDwidth?'],

'Writeable' : [':INST:SEL NR5G',':INIT:CONT ON',':OUTP:STAT OFF',':FEED:RF:PORT:INP RFIN',':CONF:ACP', 
':RAD:STAN:PRES:CARR B{}M'.format(RU_Details.CONF['BANDWIDTH']),':RAD:STAN:PRES:FREQ:RANG FR1',':RAD:STAN:PRES:DMOD TDD',':RAD:STAN:PRES:SCS SCS30K', 
':RAD:STAN:PRES:RBAL {}'.format(RU_Details.CONF['Test_Model'][1]),':RAD:MIMO 0',':RAD:STAN:PRES:DLIN:BS:CAT ALAR',':SENSe:CCARrier:COUNt 1', 
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
EVM = {'Query' : [':CCAR:REF?',':SENSe:CCARrier0:RADio:STANdard:BANDwidth?'],


'Writeable' : [':INST:SEL NR5G', ':INIT:CONT OFF', ':OUTP:STAT OFF', ':FEED:RF:PORT:INP RFIN', ':CONF:EVM', ':RAD:STAN:PRES:CARR B{}M'.format(RU_Details.CONF['BANDWIDTH']), 
':RAD:STAN:PRES:FREQ:RANG FR1', ':RAD:STAN:PRES:DMOD TDD', ':RAD:STAN:PRES:SCS SCS30K', ':RAD:STAN:PRES:RBAL {}'.format(RU_Details.CONF['Test_Model'][1]), 
':RAD:MIMO 0', ':RAD:STAN:PRES:DLIN:BS:CAT ALAR', ':SENSe:CCARrier:COUNt 1', ':SENSe:CCARrier:CONFig:ALLocation Contiguous', 
':SENSe:CCARrier:CONFig:ALLocation:NCONtiguous:ABPoint CC0', ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(RU_Details.CONF['BANDWIDTH']), 
':SENSe:CCARrier0:STATe ON', ':SENSe:CCARrier0:FREQuency:OFFSet 0MHz', ':SENSe:CCARrier0:SPECtrum NORM', ':CCAR:REF {}'.format(float(RU_Details.CONF['Freq'])*1000000), 
':RAD:STAN:PRES:IMM', ':INIT:CONT OFF', ':RAD:STAN:DIR DLINK', ':EVM:AVER:STAT 0', ':POW:RANG 10', 
':EVM:CCAR0:DC:PUNC ON', ':SWE:EGAT:STATE 0', ':TRIG:EVM:SOUR IMM', 
':RAD:STAN:PRES:RBAL {}'.format(RU_Details.CONF['Test_Model'][1]), ':RAD:STAN:PRES:IMM', ':RAD:MIMO 0', ':EVM:CCAR0:PROF:PDSC:AUTO OFF', 
':EVM:AVER:STAT 0', ':POW:RANG 10', ':SENSe:CCARrier0:RADio:STANdard:BANDwidth B{}M'.format(RU_Details.CONF['BANDWIDTH']), ':SENSe:CCARrier0:STATe ON', 
':SENSe:CCARrier0:FREQuency:OFFSet 0MHz', ':SENSe:CCARrier0:SPECtrum NORM', ':CCAR:REF {}'.format(float(RU_Details.CONF['Freq'])*1000000), ':EVM:CCAR0:DC:PUNC ON', 
':DISP:EVM:VIEW NORM;', ':DISP:EVM:WIND5:DATA FRES;', ':DISP:EVM:WIND1:DATA MTIM;', ':DISP:EVM:WIND1:Y:PDIV 0.275;',
':CORR:BTS:GAIN {}'.format(RU_Details.CONF['Cable_Loss']), ':EVM:AVER:COUN?', ':EVM:AVER:COUN 1', ':INIT:CONT ON', ':POW:RANG:OPT IMM' ]
}



