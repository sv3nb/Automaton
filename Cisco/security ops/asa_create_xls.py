import xlsxwriter

def asa_create_xls():

    fwrules = asa_parse_syslog()
    with xlsxwriter.Workbook('asa_fwrules.xlsx') as workbook:
        Rules = workbook.add_worksheet('Rules')
        bold = workbook.add_format({'bold': True})

    # create first row with headers
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        headers = fwrules[0].keys()
        for (letter,header) in zip(letters, headers):
            Rules.write(f'{letter}1', header, bold)

    # write each list of subnets to correct row
        rows = fwrules.len()
        row = 2
        
        for rule in fwrules:
            Rules.write_row('B1',rule.values())
