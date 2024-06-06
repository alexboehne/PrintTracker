import mysql.connector
import PySimpleGUI as pg

def main(db, cursor, entry_list):

    # SQL query to update an entry
    update_entry_string = ("UPDATE cur_prints SET l_name = %s, f_name = %s, email = %s, pr_name = %s, pr_description = %s, "
                           "pr_status = %s, date_requested = %s, date_due = %s, color = %s, note = %s "
                           "WHERE ID = %i")

    status_list = ['Approved', 'Sliced', 'Printing', 'Emailed', 'Completed', 'Denied', 'Inquiry']

    entry_layout = [  # Layout of submission form
        [pg.Text("Please click the button to update")],
        [pg.Text("ID", 15, 1), pg.InputText(default_text=entry_list[0], disabled=True)],
        [pg.Text("Last name", 15, 1), pg.InputText(key='-LNAME-', default_text=entry_list[1])],
        [pg.Text("First name", 15, 1), pg.InputText(key='-FNAME-', default_text=entry_list[2])],
        [pg.Text("Email", 15, 1), pg.InputText(key='-EMAIL-', default_text=entry_list[3])],
        [pg.Text("Print name", 15, 1), pg.InputText(key='-PR_NAME-', default_text=entry_list[4])],
        [pg.Text("Description", 15, 1), pg.InputText(key='-PR_DESC-', default_text=entry_list[5])],
        [pg.Text("Status:", 15, 1), pg.Combo(status_list, key='-STATUS-',
                                             default_value=entry_list[6], readonly=True)],

        [pg.Text("Date requested", 15, 1), pg.InputText(key='-REQ_DATE_BOX-', default_text=entry_list[7]),
         pg.Button('Get date', key='-REQ_DATE-')],
        [pg.Text("Date due", 15, 1), pg.InputText(key='-DUE_DATE_BOX-', default_text=entry_list[8]),
         pg.Button('Get date', key='-DUE_DATE-')],

        [pg.Text("Color", 15, 1), pg.InputText(key='-COLOR-', default_text=entry_list[9])],
        [pg.Text("Note", 15, 1), pg.InputText(key='-NOTE-', default_text=entry_list[10])],
        [pg.Button("Submit")]
    ]

    # function to execute SQL query with parameters in update window
    def db_update(l_name, f_name, email, pr_name, pr_desc, status, req_date, due_date, color, note):
        val_string = ['N/A'] * 10

        for x in val_string:
            print(x)

        val_string[0] = repr(l_name)
        val_string[1] = repr(f_name)
        val_string[2] = repr(email)
        val_string[3] = repr(pr_name)
        val_string[4] = repr(pr_desc)
        val_string[5] = "\'" + status + "\'"
        val_string[6] = "\'" + req_date + "\'"
        val_string[7] = "\'" + due_date + "\'"
        val_string[8] = repr(color)
        val_string[9] = repr(note)



        full_command = update_entry_string % (val_string[0], val_string[1], val_string[2], val_string[3], val_string[4],
                                              val_string[5], val_string[6], val_string[7], val_string[8], val_string[9], entry_list[0])
        print(full_command)

        cursor.execute(full_command)
        db.commit()

    # made this function again because pycharm is the enemy of file spread
    def reformat_date(year, mon, day):
        return '%s-%s-%s' % (year, mon, day)

    update_window = pg.Window("Update %s" % entry_list[4], entry_layout)

    while True:
        event, values = update_window.read()

        if event is None or event == 'Exit':
            break

        if event == 'Submit': # update with window values
            try:
                db_update(values['-LNAME-'], values['-FNAME-'], values['-EMAIL-'], values['-PR_NAME-'],
                          values['-PR_DESC-'], values['-STATUS-'], values['-REQ_DATE_BOX-'], values['-DUE_DATE_BOX-'],
                          values['-COLOR-'], values['-NOTE-'])
                update_window.close()
            except mysql.connector.errors.DataError:
                pg.popup_error("Date(s) inputted have incorrect format")
            except mysql.connector.errors.DatabaseError:
                pg.popup_error("Email inputted is not valid")

        # date popups
        if event == '-REQ_DATE-':
            req_date = pg.popup_get_date()
            date_string = reformat_date(req_date[2], req_date[0], req_date[1])
            update_window['-REQ_DATE_BOX-'].update(date_string)

        if event == '-DUE_DATE-':
            due_date = pg.popup_get_date()
            date_string = reformat_date(due_date[2], due_date[0], due_date[1])
            update_window['-DUE_DATE_BOX-'].update(date_string)

if __name__ == '__main__':
    main()