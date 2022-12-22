import PySimpleGUI as sg
import sqlite3

import random
import string
#==============================================================
#Datu bāze izveidošana 

conn = sqlite3.connect(r'veseliba.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   id_user PRIMARY KEY,
   vards TEXT,
   uzvards TEXT,
   dzim_datums TEXT,
   augums TEXT,
   svars TEXT,
   bmi TEXT);
""")
conn.commit()

#===================================================================
#Svara indeksa noteikšanas funkcija

def calc_bmi(h,w):
    try:
        h, w = float(h), float(w)
        bmi = round(w / h **2, 1)
        if bmi < 18.5:
            standard = "Extra vājš"
        elif 18.5 <= bmi <= 23.9:
            standard = "Normāl"
        elif 24.0 <= bmi <= 27.9:
            standard = "lieks svars"
        else:
            standard = "trekns"
    except (ValueError, ZeroDivisionError):
        return None
    else:
        return (f'BMI: {bmi}, {standard}')
#==========================================================================
#        Galvenais logs
#
#============================================================================      

def main_logs():
  sg.theme("DarkBlue2")
  layot = [[sg.Text("Vārds",size=(20,1)), sg.InputText( key='-V-', size=(15,1))],
        [sg.Text("Uzvārd",size=(20,1)), sg.InputText( key='-U-', size=(15,1))],
        [sg.CalendarButton("dzim.datums",size=(17,1),target='-DZ-',format=('%d-%m-%Y')), sg.InputText('dd,mm,gggg',key='-DZ-', size=(15,1))],
        [sg.Text("Augums",size=(20,1)), sg.InputText( key='-A-', size=(15,1))],
        [sg.Text("Svars",size=(20,1)), sg.InputText (key='-S-',size=(15,1))],
        [sg.Button("aprēķināt BMI", key='submit')],
        [sg.Text('', key='bmi', size=(20,1))],
        [sg.Text('', key='radit',size=(40,2))],
        [sg.Button("Saglabāt datus", key='glab'),sg.Button("Skātit dati", key='skat'),sg.Button("Beigt", key='q')]]

  window = sg.Window ("Calculator BMI", layot)

  while True:
    event, values = window.read()
    
    if event == 'submit':
      bmi = calc_bmi(values['-A-'], values['-S-'])
      window['bmi'].update (bmi)

    if event == 'glab':
      window['radit'].update('dati saglabāti')
      
      letters = string.digits + string.ascii_letters
      #letters = string.ascii_letters
      rand_string = ''.join(random.choice(letters) for i in range(16))
      
      ieraksts=(rand_string,values['-V-'],values['-U-'],values['-A-'],values['-S-'],values['-DZ-'],bmi)
      window['radit'].update(ieraksts)
      #print(type(ieraksts))
      #print(ieraksts)
      cur.execute("INSERT INTO Users VALUES(?,?,?,?,?,?,?)",ieraksts)
      conn.commit()
    if event == 'skat':
      records = cur.execute("SELECT * FROM Users")
      #print(cur.fetchall())
      for row in records:
        print('User ID: ',row[0])
        print('Vārds: ',row[1])
        print('Uzvārds: ',row[2])
        print('dzim.datums: ',row[3])
        print('Augums: ',row[4])
        print('Svars: ',row[5])
        print('Aprēķināts BMI: ',row[6], end="\n\n")

    if event == sg.WINDOW_CLOSED or event == 'q':
      print(values[1],values[2],bmi)
      break

  window.close()
  
      
#=========================================================================== 
# Piekļuves logs
  
username = 'Admin'
password = 'admin'
#PROGRESS BAR
def progress_bar():
    sg.theme('LightBlue2')
    layout = [[sg.Text('«Lūdzu, gaidiet!»...')],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
            [sg.Cancel()]]

    window = sg.Window('Working...', layout)
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()
#=============================================================================

def login(): # Ieejas logs
    global username,password
    sg.theme("LightBlue2")
    layout = [[sg.Text("Log In", size =(15, 1), font=16), sg.Text("login Admin, pass: admin")],
            [sg.Text("Username", size =(15, 1), font=16),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Password", size =(15, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Button('Ok'),sg.Button('Cancel')]]

    window = sg.Window("Log In", layout)

    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Ok":
                if values['-usrnm-'] == username and values['-pwd-'] == password:
                  window.close()
                  progress_bar()
                  main_logs()
                  
                  #sg.popup("Welcome!")
                  
                  #break
                elif values['-usrnm-'] != username or values['-pwd-'] != password:
                  sg.theme("DarkRed")  
                  sg.popup("Invalid login. Try again")

    window.close()


#login()
if __name__ == '__main__':
    sg.theme('DarkAmber')
    login()