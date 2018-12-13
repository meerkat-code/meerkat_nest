#--"./malaria/ipt_done"
#--BASED ON
#--"malaria./ipt1"
#--"malaria./ipt2"
#--"malaria./ipt3"

def convert_tpi(data_entry):

    data_entry_converted = data_entry

    tpi_1 = data_entry_converted.get('data',{}).get('malaria./ipt1','')
    tpi_2 = data_entry_converted.get('data',{}).get('malaria./ipt2','')
    tpi_3 = data_entry_converted.get('data',{}).get('malaria./ipt3','')

    if tpi_1 == 'yes':
        if tpi_2 == 'yes':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == 'no':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == '':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == 'dk':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass


    elif tpi_1 == 'no':
        if tpi_2 == 'yes':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == 'no':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == '':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == 'dk':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass


    elif tpi_1 == '':
        if tpi_2 == 'yes':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == 'no':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == '':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == 'dk':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass


    elif tpi_1 == 'dk':
        if tpi_2 == 'yes':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == 'no':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == '':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

        elif tpi_2 == 'dk':
            if tpi_3 == 'yes':
                pass
            elif tpi_3 == 'no':
                pass
            elif tpi_3 == '':
                pass
            elif tpi_3 == 'dk':
                pass

    return data_entry_converted