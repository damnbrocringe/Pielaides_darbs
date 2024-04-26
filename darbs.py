import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox
from finance_manager import finance_window 

conn = sqlite3.connect("users.db")

conn.execute("""CREATE TABLE IF NOT EXISTS lietotaji(
            key INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            parole TEXT)""")
conn.commit()

conn.execute("""CREATE TABLE IF NOT EXISTS finanses(
            user_key INTEGER PRIMARY KEY,
            total_funds REAL,
            reason TEXT,
            FOREIGN KEY(user_key) REFERENCES lietotaji(key)
)""")
conn.commit()


def check_user(username, password):
    curr = conn.cursor()
    curr.execute("SELECT parole FROM lietotaji WHERE username=?", (username,))
    rinda = curr.fetchone()
    if rinda:
        stored_hash = rinda[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            finance_window(username)
        else:
            messagebox.showerror("Paziņojums", "Nepareiza parole.")
    else:
        messagebox.showerror("Paziņojums", "Lietotājs nav atrasts")


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed_password




def add_user_window():

    def add_user():
        user = username_entry.get()
        password = encrypt_password(password_entry.get())
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM lietotaji WHERE username=?",(user,))
        user_count = cursor.fetchone()[0]
        if user_count > 0:
            messagebox.showerror("Kļūda", "Lietotājvārds jau izmantots")
            return
        if len(password_entry.get()) < 6:
            messagebox.showerror("Kļūda","Parolei jābūt vismaz 6 rakstzīmes.")
            return


        cursor.execute("INSERT INTO lietotaji (username, parole) VALUES (?,?)",(user,password))
        conn.commit()
        user_key = cursor.lastrowid
        cursor.execute("INSERT INTO finanses (user_key,total_funds) VALUES (?,?)", (user_key, 0.00))
        conn.commit()

    user_window = Toplevel(root)
    user_window.geometry("300x300")
    user_window.configure(bg="gray")

    Register_label=Label(user_window,text="Reģistrēties",bg="gray")
    Register_label.config(font=("Bold",20))
    Register_label.pack()

    username_label=Label(user_window, text="Vārds:",bg="gray")
    username_label.pack()
    username_entry = Entry(user_window)
    username_entry.pack()

    password_label=Label(user_window, text="Parole:",bg="gray")
    password_label.pack()
    password_label_instruction = Label(user_window, text="*parole jābūt vismaz 6 rakstzīmēm.",bg="gray")
    password_label_instruction.pack()
    password_entry = Entry(user_window)
    password_entry.pack()

    poga_adduser=Button(user_window, text="Pievienot lietotāju")
    poga_adduser.pack(pady=20)
    poga_adduser.config(bd=0,bg="coral",height=2,width=16,command=add_user)
    poga_adduser.pack()
    

    user_window.mainloop()


root=Tk()

root.geometry("300x300")
root.configure(background='gray')

label=Label(text="Pieslēgties",bg="gray")
label.config(font=("Bold",20))
label.pack()

lietotajs_label=Label(text="Ievadi lietotāja vārdu",bg="gray")
lietotajs_label.pack(pady=10)
lietotajs_entry = Entry()
lietotajs_entry.pack()

parole_label=Label(text="Ievadi paroli",bg="gray")
parole_label.pack(pady=10)
parole_entry = Entry(show="*")
parole_entry.pack()



poga1=Button(text="Pieslēgties")
poga1.pack(pady=20)
poga1.config(bd=0,bg="coral",height=2,width=16,command=lambda: check_user(lietotajs_entry.get(),parole_entry.get()))

poga2=Button(text="Izveidot jaunu kontu")
poga2.pack()
poga2.config(bd=0,bg="coral",height=2,width=16,command=add_user_window)

root.mainloop()
