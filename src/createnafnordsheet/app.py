import yaml
import xlsxwriter
import random
from datetime import datetime

if __name__ == '__main__':

    with open('./etc/ordabok.yaml', 'rt', encoding='utf') as f:
        ordabok = yaml.safe_load(f.read())

    allnafnord = ordabok['karlkyns'] + \
        ordabok['kvenkyns'] + ordabok['hvorugkyns']
    shuffled_ordabok = allnafnord.copy()
    random.shuffle(shuffled_ordabok)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    xslxfile = ordabok['learningsheet_path'] + 'heimavinni_' + now + '.xlsx'

    workbook = xlsxwriter.Workbook(xslxfile)
    # formatting cells
    header_format = workbook.add_format({'bold': True,
                                         'align': 'center',
                                         'valign': 'vcenter',
                                         'fg_color': '#DCE6F1',
                                         'border': 1,
                                         'font_size': 15})
    header_format2 = workbook.add_format({'bold': True,
                                         'align': 'center',
                                         'valign': 'vcenter',
                                         'font_color': '#0070C0',
                                         'fg_color': '#DCE6F1',
                                         'border': 1,
                                         'border_color': '#88A9D2',
                                         'font_size': 15})

    worksheet1 = workbook.add_worksheet('Nominativ Nefnifall')
    worksheet2 = workbook.add_worksheet('Akkusativ Þolfall')
    worksheet1.set_footer('Nominativ Nefnifall')
    worksheet2.set_footer('Akkusativ Þolfall')
    worksheets = [worksheet1, worksheet2]

    normal = workbook.add_format(
        {'bold': False, 'bottom': 1, 'bottom_color': '#DCE6F1'})
    normal.set_font_size(13)
    kyn_col = workbook.add_format(
        {'bold': False,
         'bottom': 1, 'bottom_color': '#DCE6F1',
         'left': 1, 'left_color': '#DCE6F1',
         'right': 1, 'right_color': '#DCE6F1',
         'font_size': 13})

    for ws in worksheets:
        # page setup
        ws.set_margins(0.3, 0.2, 0.3, 0.4)

        # Write some data headers.
        ws.set_row(0, 24)
        ws.write('A1', 'Nafnorð', header_format)
        ws.write('B1', 'kyn', header_format)
        ws.write('C1', 'eintala með greini', header_format)
        ws.write('D1', 'fleirtala', header_format2)
        ws.write('E1', 'fleirtala með greini', header_format2)
        ws.freeze_panes(1, 0)

        ws.set_column('A:A', 15)
        ws.set_column('B:B', 5)
        ws.set_column('C:E', 25)

        # Start from the first cell below the headers.
        row = 1
        col = 0

        # Iterate over the data and write it out row by row.
        for nafnord in shuffled_ordabok:
            ws.write(row, col, nafnord, normal)
            ws.write(row, 1, '', kyn_col)
            ws.write(row, 2, '', normal)
            ws.write(row, 3, '', normal)
            ws.write(row, 4, '', normal)
            ws.set_row(row, 20)
            row += 1
            if row == 40:
                break

    workbook.close()


