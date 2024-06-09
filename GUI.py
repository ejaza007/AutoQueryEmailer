import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import ntpath
from functools import partial

import DataManager
import EmailManager
import Encryption
import RecipientManager
import QueryManager
import RoutineManager

def make_routine_list():
    Routine_List.clear()
    Routines = RoutineManager.get_routine()
    for i in range(len(Routines)):
        routine,time = Routines[i]
        time = time[0:2]+":"+time[2:4]+":"+time[4:6]
        Run_Command = partial(run_routine, routine,time)
        Run_Button = tk.Button(routine_window, text='Run', command=Run_Command)
        Routine_Name = tk.Label(routine_window, text=routine, anchor='w')
        Routine_Time = tk.Label(routine_window, text=time, anchor='w')
        Edit_Button = tk.Button(routine_window, text='edit')
        Remove_Command = partial(remove_from_routine_list, routine)
        Remove_Button = tk.Button(routine_window, text='X', command=Remove_Command)
        Routine_List.append((Run_Button, Routine_Name, Routine_Time, Edit_Button, Remove_Button))
    add_routine_button = tk.Button(routine_window, text='add', command=add_routine_button_pressed)
    Routine_List.append(add_routine_button)

def render_routine_list():
    for i in range(len(Routine_List)-1):
        line = Routine_List[i]
        line[0].place(x=15,y=60+i*35,height=30,width=30)
        line[1].place(x=50,y=60+i*35,height=30,width=300)
        line[2].place(x=370,y=60+i*35,height=30,width=65)
        #line[3].place(x=400,y=60+i*35,height=30,width=35)          Edit button for later updates
        line[4].place(x=420,y=60+i*35,height=30,width=30)

    Routine_List[-1].place(x=220, y=70 + len(Routine_List) * 35, width=60, height=30)

def init_routine_window():
    routine_window.protocol('WM_DELETE_WINDOW',close_routine_window)
    routine_window.title("Routine Management")
    database_config_button = tk.Button(routine_window, text='DB config', command=database_button_pressed)
    database_config_button.place(x=420, y=10, width=70, height=40)
    font_tuple = ("TkDefaultFont", 11, "bold")
    routine_label = tk.Label(routine_window, text='Routines', anchor='w', font=font_tuple)
    routine_label.place(x=15,y=25,height=30,width=70)
    routine_window.geometry("500x500")
    make_routine_list()
    render_routine_list()

def close_routine_window():
    routine_window.withdraw()

def init_database_window():
    database_window.protocol('WM_DELETE_WINDOW', close_database_window)
    if(bool(DataManager.get_type()=="0")):
        database_window.title("Config Database SQL")
        database_window.geometry("300x290")
        label = tk.Label(database_window, text="Enter Sender Credentials")
        user_label = tk.Label(database_window, text="User:", anchor="e")
        password_label = tk.Label(database_window, text="Password:", anchor="e")
        host_label = tk.Label(database_window, text="Host:", anchor="e")
        database_label = tk.Label(database_window, text="Database:", anchor="e")
        user_field = tk.Entry(database_window, textvariable=updated_db_user)
        password_field = tk.Entry(database_window, show="*", textvariable=updated_db_password)
        host_field = tk.Entry(database_window, textvariable=updated_db_host)
        database_field = tk.Entry(database_window, textvariable=updated_db_database)
        label.place(x=50, y=50, height=25, width=200)
        user_label.place(x=10, y=80, height=25, width=55)
        user_field.place(x=65, y=80, height=25, width=200)
        password_label.place(x=10, y=120, height=25, width=55)
        password_field.place(x=65, y=120, height=25, width=200)
        host_label.place(x=10, y=160, height=25, width=55)
        host_field.place(x=65, y=160, height=25, width=200)
        database_label.place(x=10, y=200, height=25, width=55)
        database_field.place(x=65, y=200, height=25, width=200)
        Update_button = tk.Button(database_window, text="Update", command=update_db_sql)
        Update_button.place(x=100, y=240, height=30, width=100)
        toggle_auth_button = tk.Button(database_window, text="Windows Authentication",command=toggle_auth_pressed)
        toggle_auth_button.place(x=40,y=10,height=30,width=220)
    else:
        database_window.title("Config Database Win")
        database_window.geometry("300x210")
        label = tk.Label(database_window, text="Enter Database Credentials")
        server_label = tk.Label(database_window, text="Server:", anchor="e")
        database_label = tk.Label(database_window, text="Database:", anchor="e")
        server_field = tk.Entry(database_window, textvariable=updated_db_server_win)
        database_field = tk.Entry(database_window, textvariable=updated_db_database_win)
        server_label.place(x=10,y=80,height=25,width=55)
        database_label.place(x=10,y=120,height=25,width=55)
        server_field.place(x=65, y=80, height=25, width=200)
        database_field.place(x=65, y=120, height=25, width=200)
        label.place(x=50, y=50, height=25, width=200)
        Update_button = tk.Button(database_window, text="Update", command=update_db_win)
        Update_button.place(x=100, y=160, height=30, width=100)
        toggle_auth_button = tk.Button(database_window, text="SQL Authentication", command=toggle_auth_pressed)
        toggle_auth_button.place(x=40, y=10, height=30, width=220)

def toggle_auth_pressed():
    DataManager.toggle_type()
    for widgets in database_window.winfo_children():
        widgets.destroy()
    init_database_window()

def update_db_sql():
    Encryption.save_database_credentials(updated_db_user.get(),updated_db_password.get(),updated_db_host.get(),updated_db_database.get())
    print("Updated Database SQL Credentials")
    database_window.withdraw()

def update_db_win():
    Encryption.save_database_credentials(updated_db_server_win.get(),updated_db_database_win.get())
    print("Updated Database Windows Credentials")
    database_window.withdraw()

def close_database_window():
    database_window.withdraw()

def add_routine():
    print(new_routine.get())
    RoutineManager.add_routine(new_routine.get(),new_routine_time_hour.get()+new_routine_time_min.get()+new_routine_time_sec.get())
    destroy_routine_list()
    make_routine_list()
    render_routine_list()
    add_routine_window.withdraw()

def add_query():
    print(new_query.get())
    QueryManager.add_query(new_query.get())
    destroy_query_list()
    make_query_list()
    render_query_list()
    add_query_window.withdraw()

def close_add_routine_window():
    add_routine_window.withdraw()

def init_add_routine_window():
    add_routine_window.protocol('WM_DELETE_WINDOW', close_add_routine_window)
    add_routine_window.title("Add New Routine")
    add_routine_window.geometry("300x165")
    label = tk.Label(add_routine_window, text="Enter New Routine")
    query_label = tk.Label(add_routine_window, text="Query:", anchor="e")
    time_label = tk.Label(add_routine_window,text="Time:", anchor="e")
    query_field = tk.Entry(add_routine_window, textvariable=new_routine)
    time_field_H = tk.Entry(add_routine_window,textvariable=new_routine_time_hour)
    time_field_M = tk.Entry(add_routine_window,textvariable=new_routine_time_min)
    time_field_S = tk.Entry(add_routine_window,textvariable=new_routine_time_sec)
    Add_button = tk.Button(add_routine_window, text="Add", command=add_routine)
    time_segment_label = tk.Label(add_routine_window,text=":",anchor="e")
    time_segment2_label = tk.Label(add_routine_window,text=":",anchor="e")
    label.pack()
    query_label.place(x=10, y=40, height=25, width=55)
    query_field.place(x=65, y=40, height=25, width=200)
    time_label.place(x=10,y=80,height=25,width=55)
    time_field_H.place(x=65,y=80,height=25,width=20)
    time_field_M.place(x=95,y=80,height=25,width=20)
    time_field_S.place(x=125,y=80,height=25,width=20)
    time_segment_label.place(x=90,y=80,height=25,width=5)
    time_segment2_label.place(x=120,y=80,height=25,width=5)
    Add_button.place(x=165, y=120, height=30, width=80)

def init_add_query_window():
    add_query_window.protocol('WM_DELETE_WINDOW', close_add_query_window)
    add_query_window.title("Add New Query")
    add_query_window.geometry("300x120")
    label = tk.Label(add_query_window, text="Enter New Query")
    query_label = tk.Label(add_query_window, text="Query:", anchor="e")
    query_field = tk.Entry(add_query_window, textvariable=new_query)
    Add_button = tk.Button(add_query_window, text="Add", command=add_query)
    label.pack()
    query_label.place(x=10, y=40, height=25, width=55)
    query_field.place(x=65, y=40, height=25, width=200)
    Add_button.place(x=110, y=80, height=30, width=80)

def remove_from_query_list(query_to_remove):
    QueryManager.remove_query(query_to_remove)
    destroy_query_list()
    make_query_list()
    render_query_list()

def remove_from_routine_list(routine_to_remove):
    RoutineManager.remove_routine(routine_to_remove)
    destroy_routine_list()
    make_routine_list()
    render_routine_list()

def add_to_query_list(query_to_add):
    QueryManager.add_query(query_to_add)
    destroy_query_list()
    make_query_list()
    render_query_list()

def run_query(query):
    query_executor = threading.Thread(target=DataManager.query_to_excel, args=(query,), daemon=True)
    query_executor.start()

def run_routine(query,time):
    print(time)
    time=time[0:2]+time[3:5]+time[6:8]
    print(time)
    routine_executor = threading.Thread(target=RoutineManager.run_routine, args=(query,time), daemon=False)
    routine_executor.start()

def make_query_list():
    Query_List.clear()
    queries = QueryManager.get_query()
    for i in range(len(queries)):
        query = queries[i]
        Run_Command = partial(run_query,query)
        Run_Button = tk.Button(query_window, text='Run', command=Run_Command)
        Query_Name = tk.Label(query_window, text=query, anchor='w')
        Edit_Button = tk.Button(query_window, text='edit')
        Remove_Command = partial(remove_from_query_list,query)
        Remove_Button = tk.Button(query_window, text='X', command= Remove_Command)
        Query_List.append((Run_Button,Query_Name,Edit_Button,Remove_Button))
    add_query_button = tk.Button(query_window, text='add', command=add_query_button_pressed)
    Query_List.append(add_query_button)

def destroy_routine_list():
    for i in range(len(Routine_List)-1):
        line = Routine_List[i]
        for element in line:
            element.destroy()
    Routine_List[-1].destroy()

def destroy_query_list():
    for i in range(len(Query_List)-1):
        line = Query_List[i]
        for element in line:
            element.destroy()
    Query_List[-1].destroy()

def render_query_list():
    for i in range(len(Query_List)-1):
        line = Query_List[i]
        line[0].place(x=15,y=60+i*35,height=30,width=30)
        line[1].place(x=50,y=60+i*35,height=30,width=300)
        #line[2].place(x=420,y=60+i*35,height=30,width=35)              Edit button for later updates
        line[3].place(x=420,y=60+i*35,height=30,width=30)

    Query_List[-1].place(x=220, y=70 + len(Query_List) * 35, width=60, height=30)



def get_checked_recipients():
    recipient_list = RecipientManager.get_emails()
    checked_recipients.clear()
    for i in range(len(checkboxes)):
        if checkboxes[i].instate(['selected']):
            checked_recipients.append(recipient_list[i])
    return checked_recipients


def update_sender():  # update the email and password of sender
    pass_coded = ""
    for n in range(len(updated_password.get())):
        pass_coded = pass_coded + "*"
    print("Updated Email")
    print("Email: ", updated_email.get())
    print(" Password: ", pass_coded)
    Encryption.save_sender_credentials(updated_email.get(), updated_password.get())
    email_window.withdraw()


def send_emails_pressed():  # to send emails to selected recipients
    EmailManager.subject = get_subject()
    print("Subject: ", get_subject())
    EmailManager.message = get_text()
    print("Message: ", get_text())
    print(get_checked_recipients())
    sender = threading.Thread(target=EmailManager.Send_Emails, args=(get_checked_recipients(),), daemon=True)
    sender.start()


def add_recipient():  # to add a new recipient to the list
    print('P', new_recipient.get())
    RecipientManager.add_recipient(new_recipient.get())
    items = RecipientManager.get_emails()
    destroy_check_list()
    check_list(items)
    add_window.withdraw()


def remove_recipients_pressed():  # to remove all selected recipients from the list
    print("Removing")
    checked_recipients = get_checked_recipients()
    for recipient in checked_recipients:
        RecipientManager.remove_recipient(recipient)
    items = RecipientManager.get_emails()
    destroy_check_list()
    check_list(items)
    print(checked_recipients)

def get_text():
    text = text_box.get("1.0", "end-1c")
    return text

def get_subject():
    subject = subject_box.get("1.0", "end-1c")
    return subject

image_path = ""
def select_image():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=(("Images", "*.jpg *.bmp *.jpeg *.png *.raw"), ("all files", "*.*")))
    EmailManager.image_path = image_path
    img_path_label.configure(text=ntpath.basename(image_path))
    print("Selected Image:", image_path)

file_path = ""
def select_file():
    file_path = filedialog.askopenfilename(title="Select attachment")
    EmailManager.file_path = file_path
    file_path_label.configure(text=ntpath.basename(file_path))
    print("Selected File:", file_path)

def close_email_window():
    email_window.withdraw()

def close_add_query_window():
    add_query_window.withdraw()

def init_change_email_window():
    email_window.protocol('WM_DELETE_WINDOW', close_email_window)
    email_window.title("Change email")
    email_window.geometry("300x170")
    label = tk.Label(email_window, text="Enter Sender Credentials")
    email_label = tk.Label(email_window, text="Email:", anchor="e")
    password_label = tk.Label(email_window, text="Password:", anchor="e")
    email_field = tk.Entry(email_window, textvariable=updated_email)
    password_field = tk.Entry(email_window, show="*", textvariable=updated_password)
    label.place(x=50, y=10, height=25, width=200)
    email_label.place(x=10, y=40, height=25, width=55)
    email_field.place(x=65, y=40, height=25, width=200)
    password_label.place(x=10, y=80, height=25, width=55)
    password_field.place(x=65, y=80, height=25, width=200)
    Update_button = tk.Button(email_window, text="Update", command=update_sender)
    Update_button.place(x=100, y=120, height=30, width=100)

def change_email_window_pressed():
    email_window.deiconify()

def close_query_window():
    query_window.withdraw()

def add_query_button_pressed():
    add_query_window.deiconify()

def add_routine_button_pressed():
    add_routine_window.deiconify()


def database_button_pressed():
    database_window.deiconify()

def init_query_window():
    query_window.protocol('WM_DELETE_WINDOW', close_query_window)
    query_window.title("Query Window")
    query_window.geometry("500x500")
    database_config_button = tk.Button(query_window, text='DB config', command=database_button_pressed)
    database_config_button.place(x=420,y=10,width=70,height=40)
    font_tuple = ("TkDefaultFont", 11, "bold")
    query_label = tk.Label(query_window, text='Queries', anchor='w', font=font_tuple)
    query_label.place(x=15,y=25,height=30,width=70)
    make_query_list()
    render_query_list()


def close_add_recipient_window():
    add_window.withdraw()

def init_add_recipient_window():
    add_window.protocol('WM_DELETE_WINDOW', close_add_recipient_window)
    add_window.title("Add New Recipient")
    add_window.geometry("300x120")
    label = tk.Label(add_window, text="Enter Recipient Email")
    email_label = tk.Label(add_window, text="Email:", anchor="e")
    email_field = tk.Entry(add_window, textvariable=new_recipient)
    Add_button = tk.Button(add_window, text="Add", command=add_recipient)
    label.pack()
    email_label.place(x=10, y=40, height=25, width=55)
    email_field.place(x=65, y=40, height=25, width=200)
    Add_button.place(x=110, y=80, height=30, width=80)


def add_recipient_window_pressed():
    add_window.deiconify()


def destroy_check_list():
    for checkbox in checkboxes:
        checkbox.destroy()
    for check_label in check_labels:
        check_label.destroy()


def check_list(items):
    checkboxes.clear()
    check_labels.clear()

    for i in range(len(items)):
        item = items[i]
        checkbox = ttk.Checkbutton(root, text="")
        checkbox.invoke()
        checkbox.invoke()
        check_label = tk.Label(root, text=item, anchor="w")
        check_label.place(x=275, y=10 + i * 20, height=20, width=250)
        checkbox.place(x=260, y=10 + i * 20, width=25, height=20)
        checkboxes.append(checkbox)
        check_labels.append(check_label)


def select_all_pressed():
    count = len(checkboxes)
    for checkbox in checkboxes:
        if checkbox.instate(['selected']):
            checkbox.invoke()
            count = count - 1
    if not count == 0:
        for checkbox in checkboxes:
            checkbox.invoke()

def query_window_pressed():
    query_window.deiconify()
    print("Query")

def routine_window_pressed():
    routine_window.deiconify()
    print("Routine")

def main_window():
    root.title("DataRoutine Manager")

    root.geometry("500x510")

    curr_email = tk.Label(root, text=Encryption.read_sender_credentials()[0], anchor="w")
    curr_email.place(x=15, y=10, height=40, width=170)
    email_button = tk.Button(root, text="Change email", command=change_email_window_pressed)
    email_button.place(x=15, y=50, height=30, width=170)

    send_button = tk.Button(root, text="Send", command=send_emails_pressed)
    send_button.place(x=440, y=450, height=40, width=50)

    file_img = tk.PhotoImage(file='Icons/file.png')
    file_button = tk.Button(root, command=select_file, image=file_img)
    file_button.place(x=10, y=405, height=40, width=40)
    file_path_label.place(x=55, y=415, height=20, width=400)

    img_img = tk.PhotoImage(file="Icons/img.png")
    image_button = tk.Button(root, command=select_image, image=img_img)
    image_button.place(x=10, y=450, height=40, width=40)
    img_path_label.place(x=55, y=460, height=20, width=400)

    add_recipient_button = tk.Button(root, text="Add Recipient", command=add_recipient_window_pressed)
    add_recipient_button.place(x=400, y=405, height=40, width=90)

    query_button = tk.Button(root, text="Queries", command=query_window_pressed)
    query_button.place(x=375, y=450, height=40, width=60)

    routine_button = tk.Button(root, text="Routines", command=routine_window_pressed)
    routine_button.place(x=305, y=450, height=40, width=65)

    DB_button = tk.Button(root, text="DB config", command=database_button_pressed)
    DB_button.place(x=230, y=450, height=40, width=70)

    remove_recipients_button = tk.Button(root, text="Remove Selected", command=remove_recipients_pressed)
    remove_recipients_button.place(x=295, y=405, height=40, width=100)

    select_all_button = tk.Button(root, text="Select\nAll", command=select_all_pressed)
    select_all_button.place(x=230, y=405, width=60, height=40)

    subject_label = tk.Label(root, text="Subject:", anchor="w")
    subject_label.place(x=15, y=85, height=20, width=50)

    message_label = tk.Label(root, text="Message:", anchor="w")
    message_label.place(x=15, y=140, height=20, width=55)

    font_tuple = ("Calibri", 11, "")
    subject_box.configure(font=font_tuple)
    text_box.configure(font=font_tuple)
    subject_box.place(x=15, y=105, height=30, width=225)
    text_box.place(x=15, y=160, height=200, width=225)

    items = RecipientManager.get_emails()
    check_list(items)

    root.mainloop()


#-------------------------------------Main Code Starts Here---------------------------------------

#Lists to help us organize data
checked_recipients = []
checkboxes = []
check_labels = []
recipient_list = RecipientManager.get_emails()
Query_List = []
Routine_List = []

#creating windows
root = tk.Tk()
add_window = tk.Toplevel(root)
email_window = tk.Toplevel(root)
query_window = tk.Toplevel(root)
add_query_window = tk.Toplevel(root)
database_window = tk.Toplevel(root)
routine_window = tk.Toplevel(root)
add_routine_window = tk.Toplevel(root)

#creating variables for our windows
photo = tk.PhotoImage(file="Icons/icon.png")
root.iconphoto(False, photo)
new_recipient = tk.StringVar()
new_query = tk.StringVar()
new_routine = tk.StringVar()
new_routine_time_hour = tk.StringVar()
new_routine_time_min = tk.StringVar()
new_routine_time_sec = tk.StringVar()
updated_email = tk.StringVar()
updated_password = tk.StringVar()
updated_db_server_win = tk.StringVar()
updated_db_database_win = tk.StringVar()
updated_db_user = tk.StringVar()
updated_db_password = tk.StringVar()
updated_db_host = tk.StringVar()
updated_db_database = tk.StringVar()

#initializing all our windows
init_add_recipient_window()
init_change_email_window()
init_query_window()
init_add_query_window()
init_add_routine_window()
init_database_window()
init_routine_window()

# withdrawing all windows except main window (Home window)
add_window.withdraw()
email_window.withdraw()
query_window.withdraw()
add_query_window.withdraw()
add_routine_window.withdraw()
database_window.withdraw()
routine_window.withdraw()

#creating some widgets to help data flow
text_box = tk.Text(root)
img_path_label = tk.Label(root, text=image_path, anchor="w")
file_path_label = tk.Label(root, text=file_path, anchor="w")
subject_box = tk.Text(root)
subject_box.focus()

#running the main window loop
main_window()
