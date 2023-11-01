# Miko v.07
# Andrew Mueller
import datetime
import paramiko
import time
import csv
import shutil
from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import os
import sys
import threading

win = Tk()
#win.iconbitmap("miko.ico")
win.title('Miko v0.7')

inttime = datetime.datetime.now()
strtime = str(datetime.datetime.now())
month = inttime.strftime("%b")
day = inttime.strftime("%d")
hour = inttime.strftime("%H")
strmin = inttime.strftime("%M")
outputfile = "Miko" + "-" + "Output" + "_" + month + "-" + day + "_" + hour + "-" + strmin + ".csv"


def get_command_results(conn, delay, prompt):
    # interval = 0.1
    maxseconds = delay
    # maxcount = maxseconds / interval
    bufsize = 1024
    input_idx = 0
    timeout_flag = False
    start = datetime.datetime.now()
    start_secs = time.mktime(start.timetuple())
    output = ''
    conn.setblocking(0)
    while True:
        if conn.recv_ready():
            data = conn.recv(bufsize).decode('ascii')
            output += data
        if conn.exit_status_ready():
            break
        # Timeout check
        now = datetime.datetime.now()
        now_secs = time.mktime(now.timetuple())
        et_secs = now_secs - start_secs
        if et_secs > maxseconds:
            timeout_flag = True
            break
        rbuffer = output.rstrip(' ')
        if len(rbuffer) > 0 and (rbuffer[-1] == prompt or rbuffer[-1] == '>'):
            break
        time.sleep(0.200)
    if conn.recv_ready():
        data = conn.recv(bufsize)
        output += data.decode('ascii')
    return output


def trash_command_results(conn, delay, prompt):
    interval = 0.1
    maxseconds = delay
    maxcount = maxseconds / interval
    bufsize = 1024
    input_idx = 0
    timeout_flag = False
    start = datetime.datetime.now()
    start_secs = time.mktime(start.timetuple())
    output = ''
    conn.setblocking(0)
    while True:
        if conn.recv_ready():
            data = conn.recv(bufsize).decode('ascii')
            output += data
        if conn.exit_status_ready():
            break
        # Timeout check
        now = datetime.datetime.now()
        now_secs = time.mktime(now.timetuple())
        et_secs = now_secs - start_secs
        if et_secs > maxseconds:
            timeout_flag = True
            break
        rbuffer = output.rstrip(' ')
        if len(rbuffer) > 0 and (rbuffer[-1] == prompt or rbuffer[-1] == '>'):
            break
        time.sleep(0.200)
    if conn.recv_ready():
        data = conn.recv(bufsize)
        output += data.decode('ascii')
    output = ''
    data = ''
    return output


def open_file():
    global inputfile
    global denot
    global vratiot
    blank_labels()
    file = filedialog.askopenfile(mode='r', filetypes=[('Comma Separated', '*.csv')])
    if file:
        filepath = os.path.abspath(file.name)
        inputfile = filepath
        introws = 0
        with open(inputfile, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                introws = introws + 1
            denot = introws
        csvfile.close()
        print("Rows: " + str(denot))
        vratiot = 'Target: 0/' + str(denot)
        present()


def blank_labels():
    global vbanner
    global vstatus
    global inputfile
    vstatus = ''
    # vbanner = ''
    inputfile = ''
    present()


def continue_button():
    global vpromptlabel
    global vuserlabel
    global vpasslabel
    global vtimeoutlabel
    global vstatus
    global vboxlabel
    global vefile
    global vheader
    global vbanner
    global inputfile
    global username
    global password
    global efile
    global promptlabel
    global userlabel
    global passlabel
    global timeoutlabel
    global status
    global eprompt
    global etimeout
    global eusername
    global epassword
    global header
    global banner
    global con_button
    global filebutton
    global help_butt
    global vbox1
    global box1
    global denoc
    global numc
    global denot
    global numt
    global vratiot
    global vratioc
    global target

    win.update()
    confir = messagebox.askokcancel(title="Confirmation", message='Are you sure?')
    if confir is False:
        sys.exit()
    else:
        username = eusername.get()
        password = epassword.get()
        prompt = eprompt.get()
        delay = int(etimeout.get())
        blast = vbox1.get()

        con_button.configure(state=DISABLED)
        eusername.configure(state=DISABLED)
        epassword.configure(state=DISABLED)
        eprompt.configure(state=DISABLED)
        etimeout.configure(state=DISABLED)
        box1.configure(state=DISABLED)
        filebutton.configure(state=DISABLED)
        win.update()

        curline = 0
        # introw = 1
        # intcolmn = 0
        # rows = []
        # line = ""
        # author = []

        print('Username: ' + username)
        print('Password: ')
        print('Delay: ' + str(delay))
        print('Prompt: ' + prompt)
        print("Input file: " + inputfile)
        print('Bypass: ')
        print(blast)

        time.sleep(2)

        print("Starting at " + str(datetime.datetime.now()))
        print('####################################')
        with open(inputfile, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            with open("varcsv.csv", 'w', newline='') as varcsv:
                csvwriter = csv.writer(varcsv)
                for row in csvreader:
                    # for every row
                    author = []
                    curline = curline + 1
                    gettarget = row[0]
                    target = str(gettarget)
                    print('-------------------')
                    print("Connecting to target: " + target)
                    blank_labels()
                    vratiot = 'Target: ' + str(curline) + '/' + str(denot)
                    vbanner = target
                    present()
                    win.update()
                    author.append(target)
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname=target, username=username, password=password, port=22, look_for_keys=False,
                            allow_agent=False)
                        conn = ssh.invoke_shell()
                        timer = 0
                        while not conn.recv_ready():
                            print('Connecting . . .')
                            time.sleep(.2)
                            timer = timer + 1
                            if timer == 100:
                                print('TIMER EXPIRED!')
                                break
                        print("Connected!")
                        conn.send("terminal length 0\r")
                        time.sleep(1)
                        output = trash_command_results(conn, delay, prompt)
                        print('-------------------')
                        for x in range(len(row)):
                            # for every column
                            if 1 <= x <= (len(row) - 1):
                                # if not first column
                                print("-----")
                                command = row[x]
                                denoc = str((len(row) - 1))
                                blank_labels()
                                vratioc = 'Command: ' + str(x) + '/' + denoc
                                vstatus = command
                                present()
                                win.update()
                                conn.send(command + "\r")
                                results = get_command_results(conn, delay, prompt)
                                print(results)
                                author.append(results)
                        conn.close()
                        ssh.close()
                        csvwriter.writerow(author)
                    except:
                        if blast == 0:
                            print('Connection Error1')
                            author.append('Connection Error1 (Stopped)')
                            csvwriter.writerow(author)
                            blank_labels()
                            vbanner = "Failed to connect"
                            vstatus = "Connection Error1"
                            print("Stopped Input CSV at " + str(datetime.datetime.now()))
                            varcsv.close()
                            csvfile.close()
                            shuin = 'varcsv.csv'
                            shuout = outputfile
                            shutil.copyfile(shuin, shuout)
                            print("Output file saved: " + outputfile)
                            blank_labels()
                            vbanner = "Stopped due to failed Target"
                            vstatus = "Output file saved: " + outputfile
                            present()
                            time.sleep(10)
                            sys.exit()
                        else:
                            print('Connection Error2')
                            author.append('Connection Error2 (bypassed)')
                            csvwriter.writerow(author)
                            blank_labels()
                            vbanner = "Failed to connect"
                            vstatus = "Continuing"
                            present()
                            time.sleep(5)
                            continue
            varcsv.close()
        csvfile.close()
        print("Completed Input CSV at " + str(datetime.datetime.now()))
        shuin = 'varcsv.csv'
        shuout = outputfile
        shutil.copyfile(shuin, shuout)
        print("Output file saved: " + outputfile)
        blank_labels()
        vbanner = "Done"
        vstatus = "Output file saved: " + outputfile
        present()
        win.update()
        sys.exit()


def help_button():
    messagebox.showinfo('Miko 0.7 Info', 'Miko is designed to run any number of unique commands on any number of hosts'
                                         '. Miko will take the first column in a .csv file as the target, each '
                                         'consecutive'
                                         ' column will be for the command/s you would like to run on its respective '
                                         'host in that row.\n\nThe SSH prompt is the character youre expecting to receive '
                                         'from your hosts. This will tell Miko to stop receiving data and process the '
                                         'next command.\n\nThe Response timeout specifies the maximum amount of time '
                                         'Miko should wait for the target to respond, this should be increased if you '
                                         'expect the target to return a lot of data.\n\nContinue on Error will specify '
                                         'whether or not Miko should continue to the next target if it cant connect to'
                                         ' a target or process all commands.')


def config_wid():
    global vpromptlabel
    global vuserlabel
    global vpasslabel
    global vtimeoutlabel
    global vstatus
    global vboxlabel
    global vefile
    global vheader
    global vbanner
    global inputfile
    global efile
    global promptlabel
    global userlabel
    global passlabel
    global timeoutlabel
    global status
    global eprompt
    global etimeout
    global eusername
    global epassword
    global header
    global banner
    global con_button
    global filebutton
    global exit_button
    global help_butt
    global vbox1
    global box1
    global boxlabel
    global denoc
    global numc
    global denot
    global numt
    global vratiot
    global vratioc

    inputfile = 'Browse to Select Input CSV'
    vpromptlabel = "SSH Prompt (#)"
    vuserlabel = "Username"
    vpasslabel = "Password"
    vtimeoutlabel = 'Response Timeout (sec)'
    vstatus = ""
    vboxlabel = "Continue on Error"
    vefile = "Selected File"
    vheader = "Select Input CSV File"
    vbanner = ''
    vratiot = 'Target: ?/?'
    vratioc = 'Command: ?/?'


    efile = Label(win, text=inputfile, bd=1, relief=SUNKEN)
    promptlabel = Label(win, text=vpromptlabel)
    userlabel = Label(win, text=vuserlabel)
    passlabel = Label(win, text=vpasslabel)
    timeoutlabel = Label(win, text=vtimeoutlabel)
    status = Label(win, text=vstatus, bd=1, relief=SUNKEN, anchor=E)
    eprompt = Entry(win, width=2)
    etimeout = Entry(win, width=2)
    eusername = Entry(win, width=15)
    epassword = Entry(win, show="*", width=15)
    header = Label(win, text=vheader)
    banner = Label(win, text=vbanner, bd=1, relief=SUNKEN, anchor=E)
    ratiot = Label(win, text=vratiot, bd=1, relief=SUNKEN, anchor=W)
    ratioc = Label(win, text=vratioc, bd=1, relief=SUNKEN, anchor=W)
    eprompt.insert(0, '#')
    etimeout.insert(0, '10')

    help_butt = Button(win, text="?", height=1, width=1, command=help_button)
    exit_button = ttk.Button(win, text="Exit", command=sys.exit)
    con_button = ttk.Button(win, text="Continue", command=threading.Thread(target=continue_button).start)
    filebutton = ttk.Button(win, text="Browse", command=open_file)

    vbox1 = IntVar()

    boxlabel = Label(win, text=vboxlabel)
    box1 = Checkbutton(win, variable=vbox1)

    header.grid(row=0, column=0)
    filebutton.grid(row=0, column=1, pady=10)

    efile.grid(row=1, column=0, columnspan=2)

    userlabel.grid(row=2, column=0)
    passlabel.grid(row=2, column=1)

    eusername.grid(row=3, column=0)
    epassword.grid(row=3, column=1, padx=20)

    promptlabel.grid(row=4, column=0)
    eprompt.grid(row=4, column=1, pady=10)

    timeoutlabel.grid(row=5, column=0)
    etimeout.grid(row=5, column=1, pady=5)

    boxlabel.grid(row=6, column=0)
    box1.grid(row=6, column=1, pady=5)

    con_button.grid(row=7, column=1)
    exit_button.grid(row=7, column=0, pady=10)

    banner.grid(row=8, column=1, columnspan=1, sticky=W + E)
    ratiot.grid(row=8, column=0, columnspan=1, sticky=W)
    status.grid(row=9, column=1, columnspan=1, sticky=W + E)
    ratioc.grid(row=9, column=0, columnspan=1, sticky=W)
    help_butt.grid(row=10, column=1, sticky=E)

    win.update()


def present():
    global vpromptlabel
    global vuserlabel
    global vpasslabel
    global vtimeoutlabel
    global vstatus
    global vboxlabel
    global vefile
    global vheader
    global vbanner
    global inputfile
    global efile
    global promptlabel
    global userlabel
    global passlabel
    global timeoutlabel
    global status
    global eprompt
    global etimeout
    global eusername
    global epassword
    global header
    global banner
    global con_button
    global filebutton
    global exit_button
    global help_butt
    global vbox1
    global box1
    global boxlabel
    global denoc
    global numc
    global denot
    global numt
    global vratioc
    global vratiot
    global target

    efile = Label(win, text=inputfile, bd=1, relief=SUNKEN)
    promptlabel = Label(win, text=vpromptlabel)
    userlabel = Label(win, text=vuserlabel)
    passlabel = Label(win, text=vpasslabel)
    timeoutlabel = Label(win, text=vtimeoutlabel)
    status = Label(win, text=vstatus, bd=1, relief=SUNKEN, anchor=E)
    #eprompt = Entry(win, width=2)
    #etimeout = Entry(win, width=2)
    #eusername = Entry(win, width=15)
    #epassword = Entry(win, show="*", width=15)
    header = Label(win, text=vheader)
    banner = Label(win, text=vbanner, bd=1, relief=SUNKEN, anchor=E)
    ratiot = Label(win, text=vratiot, bd=1, relief=SUNKEN, anchor=W)
    ratioc = Label(win, text=vratioc, bd=1, relief=SUNKEN, anchor=W)
    #help_butt = Button(win, text="?", height=1, width=1, command=help_button)
    #exit_button = ttk.Button(win, text="Exit", command=sys.exit)
    #con_button = ttk.Button(win, text="Continue", command=threading.Thread(target=continue_button).start)
    #filebutton = ttk.Button(win, text="Browse", command=open_file)


    header.grid(row=0, column=0)
    filebutton.grid(row=0, column=1, pady=10)

    efile.grid(row=1, column=0, columnspan=2)

    userlabel.grid(row=2, column=0)
    passlabel.grid(row=2, column=1)

    eusername.grid(row=3, column=0)
    epassword.grid(row=3, column=1, padx=20)

    promptlabel.grid(row=4, column=0)
    eprompt.grid(row=4, column=1, pady=10)

    timeoutlabel.grid(row=5, column=0)
    etimeout.grid(row=5, column=1, pady=5)

    boxlabel.grid(row=6, column=0)
    box1.grid(row=6, column=1, pady=5)

    con_button.grid(row=7, column=1)
    exit_button.grid(row=7, column=0, pady=10)

    banner.grid(row=8, column=1, columnspan=1, sticky=W + E)
    ratiot.grid(row=8, column=0, columnspan=1, sticky=W)
    status.grid(row=9, column=1, columnspan=1, sticky=W + E)
    ratioc.grid(row=9, column=0, columnspan=1, sticky=W)

    help_butt.grid(row=10, column=1, sticky=E)

    win.update()



global vpromptlabel
global vuserlabel
global vpasslabel
global vtimeoutlabel
global vstatus
global vboxlabel
global vefile
global vheader
global vbanner
global inputfile
global username
global password
global eusername
global epassword
global efile
global promptlabel
global userlabel
global passlabel
global timeoutlabel
global status
global eprompt
global etimeout
global eusername
global epassword
global header
global banner
global con_button
global filebutton
global help_butt
global vbox1
global box13

#efile = Label(win, text=inputfile, bd=1, relief=SUNKEN)
#promptlabel = Label(win, text=vpromptlabel)
#userlabel = Label(win, text=vuserlabel)
#passlabel = Label(win, text=vpasslabel)
#timeoutlabel = Label(win, text=vtimeoutlabel)
#status = Label(win, text=vstatus, bd=1, relief=SUNKEN, anchor=E)
#eprompt = Entry(win, width=2)
#etimeout = Entry(win, width=2)
#eusername = Entry(win, width=15)
#username = eusername.get()
#epassword = Entry(win, show="*", width=15)
#password = epassword.get()
#header = Label(win, text=vheader)
#banner = Label(win, text=vbanner, bd=1, relief=SUNKEN, anchor=E)
#help_butt = Button(win, text="?", height=1, width=1, command=help_button)
#exit_button = ttk.Button(win, text="Exit", command=sys.exit)
#con_button = ttk.Button(win, text="Continue", command=threading.Thread(target=continue_button).start)
#filebutton = ttk.Button(win, text="Browse", command=open_file)
#box1.deselect()




config_wid()
win.mainloop()
sys.exit()
