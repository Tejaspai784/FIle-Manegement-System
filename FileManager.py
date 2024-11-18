import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
# import shutil
import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from random import randint
root = tk.Tk()
ws = root.winfo_screenwidth() 
hs = root.winfo_screenheight() 
x = (ws/2) - (250/2)
y = (hs/2) - (400/2)
root.geometry('%dx%d+%d+%d' % (400, 300, x, y))
root.title('File Manager')
root.maxsize(250,400)
root.minsize(250,400)

manage_window = tk.Toplevel()
manage_window.title("Manage Accounts")
manage_window.geometry("300x300")

def unauth():
    with open("last.txt","r") as f:
        a=f.read()
    b = os.path.getmtime("test.txt")
    b = datetime.datetime.fromtimestamp(b).strftime("%Y-%m-%d %H:%M:%S")
    if a>b:
        messagebox.showinfo("Data breach","test.txt file was tampered with outside login time")

def login_window():
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 
    x = (ws/2) - (400/2)
    y = (hs/2) - (300/2)
    global login_screen
    login_screen = tk.Toplevel(root)
    login_screen.title("Login")
    login_screen.geometry('%dx%d+%d+%d' % (400, 300, x, y))
    login_screen.config()
    var=tk.Label(login_screen,text="Login system",
          font=25,
          bd=25,
          padx=125,
          pady=20,
          relief="raised")
    var.pack()

    usernameLabel = tk.Label(login_screen, text="User Name ",font=18).pack(anchor="w")
    global username_entry
    global password_entry
    username_entry = tk.Entry(login_screen,border=5,background="grey",width=50)
    username_entry.pack(anchor="w")
    passwordLabel = tk.Label(login_screen, text="Password ",font=18).pack(anchor="w")
    password_entry = tk.Entry(login_screen, border=5,background="grey",show="*",width=50)
    password_entry.pack(anchor="w")

    login_button = tk.Button(login_screen, text="Login",font=18, command=login, pady=5,width=10)
    login_button.pack()

def logout():
    with open("last.txt",'w') as f:
        d=datetime.datetime.now()
        f.write(d.strftime("%Y-%m-%d %H:%M:%S")+"\n")
    manage_window.destroy()
    login_window()

def view_accounts():
    with open("accounts.txt", "r") as file:
        accounts = file.readlines()
    messagebox.showinfo("Accounts", "Current accounts:\n\n" + "".join(accounts))

def add_account():
    username = tk.simpledialog.askstring("Add Account", "Enter username:")
    ok=False
    with open("accounts.txt", "r") as file:
        accounts = file.readlines()
    for account in accounts:
        x=account.split(":")
        if username==x[0]:
            ok=False
        else:
            ok=True
    if ok==True:
        check=username.isalnum()
        if len(username)>=4 and check==True:
            if username:
                success=0
                while (success==0):
                    password = tk.simpledialog.askstring("Add Account", "Enter password:")
                    checkpass=password.isalnum()
                    if len(password)>=4 and check==True:
                        if password:
                            with open("accounts.txt", "a") as file:
                                file.write(username + ":" + password + "\n")
                            messagebox.showinfo("Success", "Account added successfully.")
                            success=1
                    else:
                        messagebox.showerror("Error","Password must be alphanumeric and atleast 4 characters long")
        else:
            messagebox.showerror("Error","Invalid characters entered, use alphanumeric characters and length of username should be atleast 4 characters long")
            add_account()
    else:
        messagebox.showerror("Error","Username already taken")
        add_account()

def delete_account():
    username = tk.simpledialog.askstring("Delete Account", "Enter username:")
    if username:
        with open("accounts.txt", "r") as file:
            accounts = file.readlines()
        with open("accounts.txt", "w") as file:
            for account in accounts:
                if not account.startswith(username + ":"):
                    file.write(account)
        messagebox.showinfo("Success", "Account deleted successfully.")

def update_account():
    username = tk.simpledialog.askstring("Update Account", "Enter username:")
    if username:
        with open("accounts.txt", "r") as file:
            accounts = file.readlines()
        temp=[]
        for account in accounts:
            if account.startswith(username + ":"):
                password = tk.simpledialog.askstring("Update Account", "Enter new password:")
                if password:
                    verify=tk.simpledialog.askstring("Update Account", "Enter yes for 2-Factor Authentication:")
                    if verify.lower()=="yes":
                        a=username+":"+password+":"+verify+"\n"
                    else:
                        a=username+":"+password+":yes\n"
                temp.append(a)
            else:
                temp.append(account)
        with open("accounts.txt", "w") as file:
            file.writelines(temp)
        messagebox.showinfo("Success", "Account updated successfully.")

def otp():
    message = MIMEMultipart()
    message['From'] = "tempsignin07@gmail.com"
    message['To'] = "gouthamvivekanand0@gmail.com"
    message['Subject'] = 'OTP for login'
    motp=randint(10000,99999)
    body = f"{motp}"
    message.attach(MIMEText(body, 'plain'))
    
    
    # Send the email using SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("tempsignin07@gmail.com", 'zwoc wqvt qytq cntn')
    text = message.as_string()

    server.sendmail("tempsignin07@gmail.com","gouthamvivekanand0@gmail.com", text.encode('utf-8'))
    server.quit()
    return motp

def login():

    with open("accounts.txt", "r") as f:
        accounts = f.readlines()
    # print(accounts)

    username = username_entry.get()
    password = password_entry.get()
    valid = False
    for account in accounts:
        if account.strip() == f"{username}:{password}" or account.strip()==f"{username}:{password}:yes":
            valid = True
            break

    if valid:
        if username=="admin" and password=="main":
            messagebox.showinfo("Success", "Login successful!")
            login_screen.destroy()
            unauth()
            view_btn = tk.Button(manage_window, text="View Accounts", command=view_accounts)
            view_btn.pack(pady=10)

            add_btn = tk.Button(manage_window, text="Add Account", command=add_account)
            add_btn.pack(pady=10)

            delete_btn = tk.Button(manage_window, text="Delete Account", command=delete_account)
            delete_btn.pack(pady=10)

            update_btn = tk.Button(manage_window, text="Update Account", command=update_account)
            update_btn.pack(pady=10)

            logout_btn = tk.Button(manage_window, text="logout", command=logout)
            logout_btn.pack(pady=10)

            manage_window.deiconify()

        else:
            global currentuser
            if account.strip()==f"{username}:{password}:yes":
                rotp=otp()
                cotp=tk.simpledialog.askstring("OTP","Enter OTP :")
                if rotp==int(cotp):
                    messagebox.showinfo("Success", "Login successful!")
                    # global currentuser
                    currentuser=username
                    unauth()
                    login_screen.destroy()
                    root.deiconify()
                else:
                    messagebox.showerror("Error","Invalid OTP")
            else:
                messagebox.showinfo("Success", "Login successful!")
                # global currentuser
                currentuser=username
                unauth()
                login_screen.destroy()
                root.deiconify()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def list_files():

    dir_path = filedialog.askdirectory()

    list_files_window = tk.Toplevel(root)
    list_files_window.title("List Files")
    list_files_window.geometry("400x400")

    files_listbox = tk.Listbox(list_files_window)
    files_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    files = os.listdir(dir_path)

    for file in files:
        files_listbox.insert(tk.END, file)

    def open_file(event):

        selected_file = files_listbox.get(files_listbox.curselection())
        counter=0
        with open("accounts.txt", "r") as f:
                accounts = f.readlines()
        for account in accounts:
            acc=account.split(":")
            if acc[0] in selected_file and acc[0]!=currentuser:
                counter+=1
                break
        if counter==0:

            os.startfile(os.path.join(dir_path, selected_file))
        else:
            messagebox.showerror("Error","No access")

    files_listbox.bind("<Double-Button-1>", open_file)

def open_file():
    filename = filedialog.askopenfilename()
    counter=0
    with open("accounts.txt", "r") as f:
            accounts = f.readlines()
    for account in accounts:
        acc=account.split(":")
        if acc[0] in filename and acc[0]!=currentuser:
            counter+=1
            break
    if counter==0:
        flags = os.O_RDWR | os.O_CREAT
        os.open(filename,flags)
        os.system('open ' + filename)
    else:
        messagebox.showerror("Error","No access")

def create_folder():
    folder_path = tk.filedialog.askdirectory(title="Select a folder to create a new folder in")

    folder_name = tk.simpledialog.askstring(title="Create Folder", prompt="Enter the folder name:")
    new_folder_path = os.path.join(folder_path, folder_name)
    os.mkdir(new_folder_path)
    print(f"Created new folder: {new_folder_path}")

def delete_file():#trash
    filename = tk.filedialog.askopenfilename()
    if filename:
        counter=0
    with open("accounts.txt", "r") as f:
            accounts = f.readlines()
    for account in accounts:
        acc=account.split(":")
        if acc[0] in filename and acc[0]!=currentuser:
            counter+=1
    if counter==0:
        os.remove(filename)
    else:
        messagebox.showerror("Error","No access")

def delete_folder():#trash
    parent_folder_path = tk.filedialog.askdirectory(title="Select the parent folder")

    folder_name = tk.simpledialog.askstring(title="Delete Folder", prompt="Enter the folder name:")
    folder_path = os.path.join(parent_folder_path, folder_name)

    if os.path.exists(folder_path):
        counter=0
        files = os.listdir(folder_path)
        for file in files:

            with open("accounts.txt", "r") as f:
                    accounts = f.readlines()
        for account in accounts:
            acc=account.split(":")
            if acc[0] in file and acc[0]!=currentuser:
                counter+=1
                break

        if counter>0:
            messagebox.showerror("Error","No access")
        else:
            os.rmdir(folder_name)

            print(f"{folder_path} has been deleted.")
    else:
        print(f"{folder_path} does not exist.")

def create_group():#check if these folders are already present if present use those folders create default folder // server
    folder_path = tk.filedialog.askdirectory()
    if folder_path:
        files = os.listdir(folder_path)
        for f in files:
            if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG'):
                os.makedirs(os.path.join(folder_path, 'Images'), exist_ok=True)
                os.rename(os.path.join(folder_path, f), os.path.join(folder_path, 'Images', f))
            elif f.endswith('.txt'):
                os.makedirs(os.path.join(folder_path, 'Text'), exist_ok=True)
                os.rename(os.path.join(folder_path, f), os.path.join(folder_path, 'Text', f))
            elif f.endswith('.pdf'):
                os.makedirs(os.path.join(folder_path, 'PDF'), exist_ok=True)
                os.rename(os.path.join(folder_path, f), os.path.join(folder_path, 'PDF', f))
            elif f.endswith('.docx'):
                os.makedirs(os.path.join(folder_path, 'Docs'), exist_ok=True)
                os.rename(os.path.join(folder_path, f), os.path.join(folder_path, 'Docs', f))
            elif f.endswith('.pptx'):
                os.makedirs(os.path.join(folder_path, 'PPT'), exist_ok=True)
                os.rename(os.path.join(folder_path, f), os.path.join(folder_path, 'PPT', f))
            elif f.endswith('.xlsx'):
                os.makedirs(os.path.join(folder_path, 'Excel'), exist_ok=True)
                os.rename(os.path.join(folder_path, f), os.path.join(folder_path, 'Excel', f))
            elif f.endswith('.exe'):
                os.makedirs(os.path.join(folder_path, 'Apps and setups'), exist_ok=True)
                os.rename(os.path.join(folder_path, f), os.path.join(folder_path, 'Apps and setups', f))
            else:
                os.makedirs(os.path.join(folder_path, 'Other'), exist_ok=True)
                os.rename(os.path.join(folder_path, f), os.path.join(folder_path, 'Other', f))
    messagebox.showinfo(title="Successfully Grouped",message="Data in the given folder is grouped")

def search_file():#search algo

    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    file_name = tk.simpledialog.askstring("Search File", "Enter the name of the file to search for:")
    counter=0
    with open("accounts.txt", "r") as f:
            accounts = f.readlines()
    for account in accounts:
        acc=account.split(":")
        if acc[0] in file_name and acc[0]!=currentuser:
            counter+=1
    if counter>0:
        messagebox.showerror("Error","No access")
    else:

        if not file_name:
            return

        for root, dirs, files in os.walk(folder_path):
            if file_name in files:
                file_path = os.path.join(root, file_name)

                message = f"File '{file_name}' found at:\n{file_path}\n\nWould you like to open the file?"
                choice = messagebox.askquestion("Search File", message, icon="question", default="yes")
                if choice == "yes":

                    os.startfile(file_path)
                else:

                    window = tk.Tk()
                    window.withdraw()
                    window.clipboard_clear()
                    window.clipboard_append(file_path)
                    window.update()
                    messagebox.showinfo("Search File", "File path copied to clipboard.")
                return

        messagebox.showinfo("Search File", f"File '{file_name}' not found in '{folder_path}'.")

def mainlogout():
    root.withdraw()
    login_window()

def send_email():
    # Create the GUI window
    window = tk.Tk()
    window.title("Send Email")
    window.geometry("400x300")
    
    # Create the email address input fields
    
    global receiver_email_entry
    receiver_email_label = tk.Label(window, text="Receiver's Email Address")
    receiver_email_label.pack()
    receiver_email_entry = tk.Entry(window, width=30)
    receiver_email_entry.pack()
    receiver=receiver_email_entry
    print(receiver)
    
    # Create the file selection button
    file_button = tk.Button(window, text="Select File(s)", command=select_files)
    file_button.pack()
    
    # Create the send email button
    send_button = tk.Button(window, text="Send Email", command=send)
    send_button.pack()
    
    # Start the GUI event loop
    window.mainloop()

def select_files():
    # Use the filedialog library to allow the user to select files
    files = filedialog.askopenfilenames()
    global file_list
    file_list = list(files)

def send():
    message = MIMEMultipart()
    message['From'] = "tempsignin07@gmail.com"
    message['To'] = receiver_email_entry.get()
    message['Subject'] = 'File'
    body = 'File sent through file manager'
    message.attach(MIMEText(body, 'plain'))
    
    # Attach the selected files to the email
    for f in file_list:
        with open(f, "rb") as attachment:
            part = MIMEApplication(
                attachment.read(),
                Name=f.split('/')[-1]
            )
            part['Content-Disposition'] = f'attachment; filename="{f.split("/")[-1]}"'
            message.attach(part)

    # Send the email using SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("tempsignin07@gmail.com", 'zwoc wqvt qytq cntn')
    text = message.as_string()

    server.sendmail("tempsignin07@gmail.com",receiver_email_entry.get(), text.encode('utf-8'))
    server.quit()
    messagebox.showinfo("Success","File sent successfully")
    

var1=tk.Label(root,text=f"FILE MANAGER",
          bd=5,
          padx=20,
          pady=20)
list_files_button = tk.Button(root, text='List Files', command=list_files)
open_file_button = tk.Button(root, text='Open File', command=open_file)
create_folder_button = tk.Button(root, text='Create Folder',command=create_folder)
delete_file_button = tk.Button(root, text='Delete File', command=delete_file)
delete_folder_button = tk.Button(root, text='Delete Folder', command=delete_folder)
create_group_button = tk.Button(root, text='Grouper', command=create_group)
searchfile_button = tk.Button(root, text='Search file', command=search_file)
sendfile_button = tk.Button(root, text='Send file', command=send_email)
logouter_button = tk.Button(root, text='Logout', command=mainlogout)

var1.pack()
list_files_button.pack(padx=5,pady=5,fill="both")
open_file_button.pack(padx=5,pady=5,fill="both")
create_folder_button.pack(padx=5,pady=5,fill="both")
delete_file_button.pack(padx=5,pady=5,fill="both")
delete_folder_button.pack(padx=5,pady=5,fill="both")
create_group_button.pack(padx=5,pady=5,fill="both")
searchfile_button.pack(padx=5,pady=5,fill="both")
sendfile_button.pack(padx=5,pady=5,fill="both")
logouter_button.pack(padx=5,pady=5,fill="both")

root.withdraw()

manage_window.withdraw()

login_window()
#reload if required
root.mainloop()