import mysql.connector
import PySimpleGUI as pg
import entry_window
import update_window


def main(db, cursor):

    def update(): # refresh table view to reflect update/new entry
        cursor.execute('SELECT * FROM cur_prints LIMIT 1000')

        db_results = cursor.fetchall()

        header = ['ID', 'Last', 'First', 'Email', 'Print name', 'Description', 'Status', 'Requested', 'Due', 'Color',
                  'Note']

        result_storage = [[]]

        for row in db_results:
            result_storage.append(list(row))
        table_window['-TABLE-'].update(result_storage)

    # initialize table
    cursor.execute('SELECT * FROM cur_prints LIMIT 1000')

    results = cursor.fetchall()

    header = ['ID', 'Last', 'First', 'Email', 'Print name', 'Description', 'Status', 'Requested', 'Due', 'Color',
              'Note']

    result_storage = [[]]

    for row in results:
        result_storage.append(list(row))

    table_layout = [
        [pg.Table(result_storage, headings=header, justification='left', key='-TABLE-', enable_events=True)],
        [pg.Push(), pg.Button('View'), pg.Button('Update'), pg.Button('New Entry', key='-ENTRY-'), pg.Push()]
    ]

    table_window = pg.Window('Table Example', table_layout)

    # View window setup

    while True:
        event, values = table_window.read()

        if event == pg.WINDOW_CLOSED:
            break

        if event == '-ENTRY-': # open entry menu
            entry_window.main(db, cursor)
            update()

        if event == 'Update':
            try: # handle update without selecting row
                row_index = values['-TABLE-']
                popup_list = result_storage[row_index[0]]
                update_window.main(db, cursor, popup_list)
                update()
            except IndexError:
                pg.popup_error("Please select a row to update")


        if event == 'View': # full expanded view for entry
            row_index = values['-TABLE-']
            for result in result_storage[row_index[0]]:
                print(result)
            popup_list = result_storage[row_index[0]]

            full_desc_layout = [
                [pg.Text('Print ID:'), pg.Text(popup_list[0])],
                [pg.Text('Last name:'), pg.Text(popup_list[1])],
                [pg.Text('First name:'), pg.Text(popup_list[2])],
                [pg.Text('Email:'), pg.Text(popup_list[3])],
                [pg.Text('Print name:'), pg.Text(popup_list[4])],
                [pg.Text('Print description:'), pg.Text(popup_list[5])],
                [pg.Text('Status:'), pg.Text(popup_list[6])],
                [pg.Text('Request date:'), pg.Text(popup_list[7])],
                [pg.Text('Due date:'), pg.Text(popup_list[8])],
                [pg.Text('Color:'), pg.Text(popup_list[9])],
                [pg.Text('Note:'), pg.Text(popup_list[10])]
            ]

            full_desc_window = pg.Window(popup_list[4], full_desc_layout)

            while True:
                event, values = full_desc_window.read()

                if event is None or event == 'Exit':
                    break


if __name__ == '__main__':
    main()
