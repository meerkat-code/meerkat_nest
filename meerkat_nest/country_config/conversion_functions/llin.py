def convert_llin(data_entry):
    data_entry_converted = data_entry

    #--"malaria./llin"
    #-- BASED
    #ON
    #--"malaria./llin_routine"
    #--"malaria./llin_other"

    llin_routine = data_entry_converted.get('data',{}).get('malaria./llin_routine','')
    llin_other = data_entry_converted.get('data',{}).get('malaria./llin_other','')

    if llin_routine == 'yes':
        if llin_other == 'yes':
            pass
        elif llin_other == 'no':
            pass
        elif llin_other == '':
            pass
        elif llin_other == 'dk':
            pass
    elif llin_routine == 'no':
        if llin_other == 'yes':
            pass
        elif llin_other == 'no':
            pass
        elif llin_other == '':
            pass
        elif llin_other == 'dk':
            pass

    elif llin_routine == '':
        if llin_other == 'yes':
            pass
        elif llin_other == 'no':
            pass
        elif llin_other == '':
            pass
        elif llin_other == 'dk':
            pass

    elif llin_routine == 'dk':
        if llin_other == 'yes':
            pass
        elif llin_other == 'no':
            pass
        elif llin_other == '':
            pass
        elif llin_other == 'dk':
            pass

    return data_entry_converted