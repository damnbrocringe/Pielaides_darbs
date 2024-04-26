import sqlite3
from tkinter import *
from tkinter import messagebox

conn = sqlite3.connect("users.db")




def finance_window(username):
    finance_root = Tk()
    cursor = conn.cursor()



    finance_root.geometry("300x300")
    finance_root.configure(background='gray')


    cursor.execute("SELECT key FROM lietotaji WHERE username=?", (username,))
    user_key = cursor.fetchone()[0]

    cursor.execute("SELECT total_funds FROM finanses WHERE user_key=?", (user_key,))
    funds = cursor.fetchone()[0]

    welcome_user = Label(finance_root,text=f"Sveiki, {username}!",bg="gray",font=(25))
    welcome_user.pack(pady=10)

    current_funds = Label(finance_root,text=f"Konta Bilance: {funds} €",bg="gray")
    current_funds.pack(pady=10)


    def change_amount():
        change_window = Toplevel(finance_root)
        change_window.geometry("500x300")
        change_window.configure(bg="gray")

        amount_label = Label(change_window,text="Ievadiet skaitli, lai mainītu konta bilanci (+/-) \n Maksimālais skaitlis ir (+/- 10'000)",bg="gray")
        amount_label.pack(pady=10)
        amount_entry = Entry(change_window,width=10)
        amount_entry.pack()

        reason_label = Label(change_window, text="Pierakstiet komentāru (Nav obligāti)",bg="gray")
        reason_label.pack(pady=10)
        reason_entry = Entry(change_window, width=50)
        reason_entry.pack(pady=10)

        amount_button = Button(change_window,text="Apstiprināt")
        amount_button.pack(pady=10)
        amount_button.config(bd=0,bg="coral",height=2,width=16,command=lambda: add_change(amount_entry.get(),reason_entry.get()))



    change_amount_button = Button(finance_root,text="Nomainīt")
    change_amount_button.pack()
    change_amount_button.config(bd=0,bg="coral",height=2,width=16,command=change_amount)

    changes_tip = Label(finance_root, text="Pēdējās transakcijas:",bg="gray")
    changes_tip.pack(pady=10)
    changes_label = Label(finance_root, text="", bg="gray")
    changes_label.pack(pady=10)

    

    

    def update_changes():
        latest_five_changes = latest_changes[-5:]
        latest_five_changes = latest_five_changes + [''] * (5 - len(latest_five_changes))
        changes_text = "\n".join(latest_five_changes)
        changes_label.config(text=changes_text)
        cursor.execute("UPDATE finanses SET reason = ? WHERE user_key =?", (changes_text, user_key))
        conn.commit()
        

    cursor.execute("SELECT reason FROM finanses WHERE user_key=?", (user_key,))
    result = cursor.fetchone()

    if result[0] != None:
        latest_changes = result[0]
        latest_changes = latest_changes.split('\n')
        update_changes()
    else:
        latest_changes = [" "," "," "," "," "]




    

    def add_change(amount,reason):
        try:
            amount = float(amount.replace(',','.'))
            if amount > 10000 or amount < -10000:
                messagebox.showerror("Kļūda", "Skaitlis pārsniedz maksimālo limitu.")
                return
        except ValueError:
            messagebox.showerror("Kļūda","Lūdzu Ievadiet skaitli.")
            return
    
        cursor = conn.cursor()
        cursor.execute("SELECT total_funds FROM finanses WHERE user_key=?", (user_key,))
        total_funds = cursor.fetchone()
        if total_funds:
            total_funds = total_funds[0]
            new_total_funds = total_funds + round(amount, 2)
            cursor.execute("UPDATE finanses SET total_funds = ? WHERE user_key = ?", (new_total_funds, user_key))
            conn.commit()
            current_funds.config(text=f"Konta Bilance: {new_total_funds} €")

            latest_changes.insert(0,f"{round(amount,2)} € - {reason if reason else "---"}")
            latest_changes.pop()
            

            update_changes()
        else:
            return



    finance_root.mainloop()

