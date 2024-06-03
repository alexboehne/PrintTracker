import mysql.connector
import PySimpleGUI as pg

def main(db, cursor):

    exec_string = ("INSERT INTO cur_prints (l_name, f_name, email, "
                   "pr_name, pr_description, pr_status, date_requested, date_due,"
                   "color, note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    val_string = [''] * 10

    status_list = ['Approved', 'Sliced', 'Printing', 'Emailed', 'Completed', 'Denied', 'Inquiry']

    entry_layout = [  # Layout of submission form
        [pg.Text("Please click the button to update")],
        [pg.Text("Last name", 15, 1), pg.InputText(key='-LNAME-')],
        [pg.Text("First name", 15, 1), pg.InputText(key='-FNAME-')],
        [pg.Text("Email", 15, 1), pg.InputText(key='-EMAIL-')],
        [pg.Text("Print name", 15, 1), pg.InputText(key='-PR_NAME-')],
        [pg.Text("Description", 15, 1), pg.InputText(key='-PR_DESC-')],
        [pg.Text("Status:", 15, 1), pg.Combo(status_list, key='-STATUS-',
                                             default_value='Approved', readonly=True)],

        [pg.Text("Date requested", 15, 1), pg.InputText(key='-REQ_DATE_BOX-'),
         pg.Button('Get date', key='-REQ_DATE-')],
        [pg.Text("Date due", 15, 1), pg.InputText(key='-DUE_DATE_BOX-'),
         pg.Button('Get date', key='-DUE_DATE-')],

        [pg.Text("Color", 15, 1), pg.InputText(key='-COLOR-')],
        [pg.Text("Note", 15, 1), pg.InputText(key='-NOTE-')],
        [pg.Button("Submit")]
    ]

    def db_update(l_name, f_name, email, pr_name, pr_desc, status, req_date, due_date, color, note):
        val_string[0] = l_name
        val_string[1] = f_name
        val_string[2] = email
        val_string[3] = pr_name
        val_string[4] = pr_desc
        val_string[5] = status
        val_string[6] = req_date
        val_string[7] = due_date
        val_string[8] = color
        val_string[9] = note

        cursor.execute(exec_string, val_string)
        db.commit()

    def db_date_get():
        pg.popup_get_date()

    def reformat_date(year, mon, day):
        return '%s-%s-%s' % (year, mon, day)

    entry_window = pg.Window('New Entry', entry_layout)  # Init window

    while True:
        event, values = entry_window.read()

        if event is None or event == 'Exit':
            break

        if event == 'Submit':
            try:
                db_update(values['-LNAME-'], values['-FNAME-'], values['-EMAIL-'], values['-PR_NAME-'],
                          values['-PR_DESC-'],
                          values['-STATUS-'], values['-REQ_DATE_BOX-'], values['-DUE_DATE_BOX-'], values['-COLOR-'],
                          values['-NOTE-'])
                break
            except mysql.connector.errors.DataError:
                pg.popup_error("Date(s) inputted have incorrect format")
            except mysql.connector.errors.DatabaseError:
                pg.popup_error("Email inputted is not valid")

        if event == '-REQ_DATE-':
            req_date = pg.popup_get_date()
            date_string = reformat_date(req_date[2], req_date[0], req_date[1])
            entry_window['-REQ_DATE_BOX-'].update(date_string)

        if event == '-DUE_DATE-':
            due_date = pg.popup_get_date()
            date_string = reformat_date(due_date[2], due_date[0], due_date[1])
            entry_window['-DUE_DATE_BOX-'].update(date_string)

if __name__ == '__main__':
    main()