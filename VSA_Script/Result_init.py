
import sys
from tabulate import tabulate
import Convert_PDF
from VSA_Script import Result_Declare
# from VSA_Script import Result_Declare


def Result(filename):

    CH_NOs = input('Number of Channel in RU For Transmission : ')
    
    PDF = Convert_PDF.PDF_CAP()
    PDF.add_page(format=(350,250))
    PDF.set_font("Times", size=12)
    PDF.set_font_size(float(10))
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5

    data = Result_Declare(CH_NOs)
    Base_station_output_power,ACLR,Modulation_quality,TC_Result = data[0],data[1],data[2],data[3]

    flag = TC_Result[-1]
    TC_Result.pop()

    ###################################### Test report verdict overview ####################################
    if flag == 'True':
        TC_Result.append(['','Overall test verdict ','Pass'])
    else:
        TC_Result.append(['','Overall test verdict ','Fail'])

    Convert_PDF.HEADING(PDF,'\nTest report verdict overview \n')
    table_Header = ['Test Case ID', 'Description', 'verdict']
    print(tabulate(TC_Result, headers=table_Header, tablefmt='fancy_grid'))
    Convert_PDF.render_header(PDF,table_Header,Header_H,PDF.epw / len(table_Header))
    Convert_PDF.render_table_data(PDF,TC_Result,line_height,PDF.epw / len(table_Header),table_Header)


    PDF.add_page(format=(350,250))
    print('\n\n\n')
    ################################### Base station output power- Test results #######################################
    CH_POWER_Header = ['Channel No','Channel Frequency [Hz]','BS Channel Bandwidth BW [MHz]','Test Channel Model','Output Power [dbm]','Limit Low [dBm]','High Low [dBm]','Verdict']
    Convert_PDF.HEADING(PDF,'\nBase station output power- Test results:\n')
    Convert_PDF.Test_HEADING(
    PDF,'''Test purpose : \nThe test purpose is to verify the accuracy of the maximum carrier output power across the frequency range and under normal and extreme conditions''')
    Convert_PDF.Test_HEADING(PDF,'Test environment : \nNormal and Extreme test conditions.')                                                                                                                                                              
    Convert_PDF.Test_HEADING(PDF,'NR FR1 test model: \n{}'.format(Base_station_output_power[0][3]))
    print(tabulate(Base_station_output_power, headers=CH_POWER_Header, tablefmt='fancy_grid'))
    Convert_PDF.render_header(PDF,CH_POWER_Header,line_height,PDF.epw / len(CH_POWER_Header))
    Convert_PDF.render_table_data(PDF,Base_station_output_power,line_height,PDF.epw / len(CH_POWER_Header),CH_POWER_Header)


    PDF.add_page(format=(350,250))
    print('\n\n\n')
    ################################### Adjacent Channel Leakage Power Ratio (ACLR) - Test results: #######################################
    ACLR_Header = ['Channel No','Channel Frequency [Hz]','BS Channel Bandwidth BW [MHz]','Test Channel Model','Low ACLR [dB]','High ACLR [dB]','Low 2xBW ACLR [dB]','High 2xBW ACLR [dB]','ACLR Limit [dB]','Verdict']
    Convert_PDF.HEADING(PDF,'\n Adjacent Channel Leakage Power Ratio (ACLR) - Test results: \n')
    Convert_PDF.Test_HEADING(
    PDF,'''Test purpose : \nTo verify that the adjacent channel leakage ratio requirement shall be met as specified by the minimum requirement.''')
    Convert_PDF.Test_HEADING(PDF,'Test environment : \nNormal test conditions.')                                                                                                                                                              
    Convert_PDF.Test_HEADING(PDF,'NR FR1 test model: \n{}'.format(ACLR[0][3]))
    print(tabulate(ACLR, headers=ACLR_Header, tablefmt='fancy_grid'))
    Convert_PDF.render_header(PDF,ACLR_Header,line_height,PDF.epw / len(ACLR_Header))
    Convert_PDF.render_table_data(PDF,ACLR,line_height,PDF.epw / len(ACLR_Header),ACLR_Header)


    PDF.add_page(format=(350,250))
    print('\n\n\n')
    #################################  Modulation quality - Test results: #########################################
    Convert_PDF.HEADING(PDF,'\n Modulation quality - Test results: \n')
    EVM_Header = ['Channel No','Channel Frequency [Hz]','BS Channel Bandwidth BW [MHz]','Test Channel Model','Measured EVM (RMS) [%]','EVM Limit [%]','Verdict']
    Convert_PDF.Test_HEADING(
    PDF,'''Test purpose : \nThe test purpose is to verify the modulation quality''')
    Convert_PDF.Test_HEADING(PDF,'Test environment : \nNormal test conditions.')                                                                                                                                                              
    Convert_PDF.Test_HEADING(PDF,'NR FR1 test model: \n{}'.format(Modulation_quality[0][3]))
    print(tabulate(Modulation_quality, headers=EVM_Header,stralign='left',maxcolwidths=[10,10,10,10,10,10,10], tablefmt='fancy_grid'))
    Convert_PDF.render_header(PDF,EVM_Header,line_height,PDF.epw / len(EVM_Header))
    Convert_PDF.render_table_data(PDF,Modulation_quality,line_height,PDF.epw / len(EVM_Header),ACLR_Header)

    PDF.output('{}.pdf'.format(filename))



if __name__ == "__main__":
    try:
        Result(sys.argv[1])
    except Exception as e:
        print('{}'.format(e))
        print('Usage: python Result_init.py <PDF filename>')