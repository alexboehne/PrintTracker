import mysql.connector
import PySimpleGUI as pg
import table_window


def main():

    login_layout = [
        [pg.Text("Username: "), pg.InputText(key='-USER-')],
        [pg.Text("Password: "), pg.InputText(key='-PASS-', password_char=True)],
        [pg.Button("Login")],
    ]

    login_window = pg.Window("Login", login_layout)
    while True:
        event, values = login_window.read()

        if event is None or event == 'Exit':
            break

        if event == 'Login':
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user=values['-USER-'],
                    passwd=values['-PASS-'],
                    database="prints"
                )
                login_window.close()

            except mysql.connector.errors.ProgrammingError:
                pg.popup("Incorrect login details. Please try again.")


    mycursor = mydb.cursor()

    table_window.main(mydb, mycursor)

if __name__=="__main__":
    main()