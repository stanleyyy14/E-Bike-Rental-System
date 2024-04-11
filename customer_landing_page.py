import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
 
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import re
from login import *

with sqlite3.connect("Database.db") as db:
    cursor = db.cursor()


# ------------------- WALLET CLOSE BUTTON ------------------------
def close_window(window):
    window.destroy()
# ------------------- ADD BALANCE -------------------------
def add_balance(input_list):
    email = input_list[0]
    amount = int(input_list[1].get())
    # amount = int(amount)
    wallet_balance = input_list[2]
    print("Amount ", amount)
    cursor.execute("select available_balance from userWallet where email = '{}'" .format(email))
    x = cursor.fetchall()
    final_amount = x[0][0] + amount
    cursor.execute("update userWallet set available_balance = '{0}' where email = '{1}'" .format(final_amount, email))
    db.commit()
    cursor.execute("select available_balance from userWallet where email = '{}'" .format(email))
    x = cursor.fetchall()
    wallet_balance.set(x[0][0])
    input_list[1].delete(0, END)
# ------------------- USER WALLET ----------------------
def user_wallet(email):
    with sqlite3.connect("TeamProject.db") as db:
        cursor = db.cursor()
    wallet_screen = Toplevel(win)
    wallet_screen.geometry("420x150")
    wallet_screen.title("Your Wallet")
    wallet_frame = Frame(wallet_screen, width = width, height = height, bg='#E9F1FA')
    wallet_frame.pack(side = "top", fill = "both", expand = True)
    l1 = Label(wallet_frame, text="Current Balance - ", font=("", 16), bg='#E9F1FA')
    l1.grid(row=1, column=1, padx=10, pady=10)
    cursor.execute("select available_balance from userWallet where email = '{}'" .format(email))
    x = cursor.fetchall()
    print(x[0][0])
    wallet_balance = StringVar()
    wallet_balance.set(x[0][0])
    l2 = Label(wallet_frame, textvariable=wallet_balance, font=("", 16), bg='#E9F1FA')
    l2.grid(row=1, column=2, padx=10, pady=10)
    l3 = Label(wallet_frame, text="Add amount - ", font=("", 16), bg='#E9F1FA')
    l3.grid(row=3, column=1, padx=10, pady=10)
    en3 = Entry(wallet_frame, text="")
    en3.grid(row=3, column=2, padx=10, pady=10)
 
    input_list = [email, en3, wallet_balance]
    b3 = Button(wallet_frame, text="Add", command = lambda: add_balance(input_list))
    b3.grid(row=3, column=3, padx=10, pady=10)

 
# ------------------- RENTAL ACTIVITY -----------------
def rental_activity(frame, input_list, rent_button):
    email = input_list[0]
    cursor.execute("select available_balance from userWallet where email ='{}'" .format(email))
    x = cursor.fetchall()
    status = "Open"
    cursor.execute("select * from rentTracker where user_email = '{}' and payment_status = '{}'" .format(email, status))
    y = cursor.fetchall()
    if x[0][0] < 10:
        messagebox.showerror("Insufficient funds", "A minimum balance of £10 should be maintained in your wallet to be able to rent a vehicle. Please add funds to your account")
    elif len(y) > 0:
        messagebox.showerror("Existing active rental", "You already have an active rental. Please close it to rent another vehicle")
    else:
        rental_screen = Toplevel(win)
        rental_screen.geometry("800x200")
        rental_screen.title("Bike Rental")
        # email = input_list[0]
        bike_name = input_list[1].get()
        rental_station = input_list[2]
        cursor.execute("""create table if not exists rentTracker(
            id integer primary key,
            bikename text,
            user_email text,
            rent_station text,
            return_station text, 
            rent_starttime text, 
            rent_endtime text,
            payment_status text)""")
        db.commit()
        rent_starttime = datetime.datetime.now()
        rent_endtime = ""
        return_station = ""
        payment_status = "Open"
        cursor.execute("""insert into rentTracker (bikename, user_email, rent_station, return_station, 
                       rent_starttime, rent_endtime, payment_status) values(?,?,?,?,?,?,?)""", 
        (bike_name, email, rental_station, return_station, rent_starttime, rent_endtime, payment_status))
        db.commit()
        print(bike_name, email, rental_station, return_station, rent_starttime, rent_endtime, payment_status)
        isavailable = 0
        cursor.execute("update bikeInformation set isavailable = '{0}' where bikename = '{1}'" .format(isavailable, bike_name))
        db.commit()
        rental_info = ("You have now rented {0} from the rental station {1} \nYou can find the payable amount when you return the vehicle" .format(bike_name, rental_station))
        lb1 = Label(rental_screen, text=rental_info, font=("", 16))
        lb1.grid(row=1, column=0, padx=10, pady=10)
        landing_frame.grid_columnconfigure(0, weight=1)
        rent_button['state'] = "disabled"
        user_profile(frame, email)
# ------------------- TRANSACTION ------------------------
def transaction(screen, frame, total_amount, email):
    cursor.execute("select available_balance from userWallet where email = '{}'" .format(email))
    x = cursor.fetchall()
    updated_amount = x[0][0]-total_amount
    if(updated_amount < 0):
        messagebox.showerror("Insufficient Balance", "Please add some funds to your account")
    else:
        cursor.execute("update userWallet set available_balance = '{0}' where email = '{1}'" .format(updated_amount, email))
        db.commit()
        cursor.execute("update rentTracker set payment_status = 'Closed' where user_email = '{0}'" .format(email))
        db.commit()
        user_profile(frame, email)
# ------------------- SHOW PAYMENT -----------------------
def show_payment(frame, total_amount, email):
    payment_screen = Toplevel(win)
    payment_screen.geometry("500x300")
    payment_screen.title("Payment Screen")
    payable_amount = StringVar()
    t = ("You need to pay the amount of £%.2f" %total_amount)
    payable_amount.set(("You need to pay the amount of £%.2f" %total_amount))
    lb1 = Label(payment_screen, textvariable=payable_amount, font=("", 16))
    lb1.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
    b1 = Button(payment_screen, text="Pay", command = lambda: transaction(payment_screen, frame, total_amount, email))
    b1.grid(row=2, column=1, padx=10, pady=10)
    payment_screen.grid_columnconfigure(1, weight=1)
 
# ------------------- RETURN ACTIVITY --------------------
def return_activity(frame, email, bike_name, station_select):
    return_time = datetime.datetime.now()
    cursor.execute("select rent_starttime from rentTracker where user_email ='{0}' and bikename = '{1}'" .format(email, bike_name))
    x = cursor.fetchall()
    date_format = '%Y-%m-%d %H:%M:%S'
    rent_time = datetime.datetime.strptime(x[0][0][:-7], date_format) 
    cursor.execute("""create table if not exists paymentTracker(
        id integer primary key, 
        email text, 
        bikename text,
        amount_charged text
        )""")
    db.commit()
    total_seconds = (return_time - rent_time).total_seconds()
    total_amount = 0.5 + ((total_seconds/10) * 0.25)
    isavailable = 1
    rental_station = station_select.get()
    cursor.execute("update bikeInformation set isavailable = '{0}', rental_station = '{1}' where bikename = '{2}'" .format(isavailable, rental_station, bike_name))
    db.commit()
    cursor.execute("insert into paymentTracker (email, bikename, amount_charged) values(?, ?, ?)", (email, bike_name, total_amount))
    db.commit()
    show_payment(frame, total_amount, email)
# ------------------- GET STATION INFORMATION -------------------
def get_station(frame, email, bike_name):
    station_select = StringVar()
    station_select.set("Select a return station")
    cursor.execute("select distinct rental_station from bikeInformation")
    rental_station = []
    for x in cursor.fetchall():
        rental_station.append(x[0])
    dd1 = OptionMenu(frame, station_select, *rental_station)
    dd1.place(x=300,y=370,width=200,height=35)
    ddb1 = Button(frame, text="Select", command = lambda: return_activity(frame, email, bike_name, station_select))
    ddb1.place(x=530,y=370,width=100,height=30)

# ------------------- BIKE INFORMATION ----------------
def get_bike_information(frame, selection, email):
    rental_station = selection.get()
    isavailable = 1
    cursor.execute("select bikeName from bikeInformation where rental_station = '{0}' and isavailable = '{1}' " .format(rental_station, isavailable))
    bike_selection = StringVar()
    bike_selection.set("Select a bike")
    bike_list = []
    for x in cursor.fetchall():
        bike_list.append(x[0])
    bike_dd = OptionMenu(frame, bike_selection, *bike_list)
    bike_dd.place(x=300,y=330,width=150,height=35)
    # return_button = Button(frame, text="Return", state="disabled")
    # return_button.grid(row=4, column=5, padx=10, pady=10)
    input_list = [email, bike_selection, rental_station]
    rent_button = Button(frame, text="Rent", command = lambda: rental_activity(frame, input_list, rent_button))
    rent_button.place(x=500,y=330,width=100,height=30)
 
    # report_button = Button(frame, text="Report")
    # report_button.grid(row=4, column=6, padx=10, pady=10)


# ------------------ GET STATION - REPORTING VERSION -------------------

def get_station_report(frame, email, bike_name):

    station_select = StringVar()

    station_select.set("Select a return station")

    cursor.execute("select distinct rental_station from bikeInformation")

    rental_station = []

    for x in cursor.fetchall():

        rental_station.append(x[0])

    dd1 = OptionMenu(frame, station_select, *rental_station)

    dd1.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

    ddb1 = Button(frame, text="Select", command = lambda: report_return_activity(frame, email, bike_name, station_select))

    ddb1.grid(row=3, column=5, padx=10, pady=10)


# ------------------- SHOW PAYMENT - REPORTING VERSION ----------------

def show_payment_report(frame, total_amount, email, bike_name):

    payment_screen = Toplevel(win)

    payment_screen.geometry("500x300")

    payment_screen.title("Payment Screen")

    bike_selection = StringVar()

    bike_selection.set(bike_name)

    input_list = [email, bike_selection]

    mark_defective(frame, input_list)

    payable_amount = StringVar()

    t = ("You need to pay the amount of £%.2f" %total_amount)

    payable_amount.set(("You need to pay the amount of £%.2f" %total_amount))

    lb1 = Label(payment_screen, textvariable=payable_amount, font=("", 16))

    lb1.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

    b1 = Button(payment_screen, text="Pay", command = lambda: transaction(payment_screen, frame, total_amount, email))

    b1.grid(row=2, column=1, padx=10, pady=10)

    payment_screen.grid_columnconfigure(1, weight=1)

    bike_selection = StringVar()

    bike_selection.set(bike_name)

    input_list = [email, bike_selection]

    mark_defective(frame, input_list)


# ------------------- RETURN ACTIVITY - REPORTING VERSION -------------

def report_return_activity(frame, email, bike_name, station_select):

    return_time = datetime.datetime.now()

    cursor.execute("select rent_starttime from rentTracker where user_email ='{0}' and bikename = '{1}'" .format(email, bike_name))

    x = cursor.fetchall()

    date_format = '%Y-%m-%d %H:%M:%S'

    rent_time = datetime.datetime.strptime(x[0][0][:-7], date_format) 

    cursor.execute("""create table if not exists paymentTracker(

        id integer primary key, 

        email text, 

        bikename text,

        amount_charged text

        )""")

    db.commit()

    total_seconds = (return_time - rent_time).total_seconds()

    total_amount = 0.5 + ((total_seconds/10) * 0.25)

    isavailable = 1

    rental_station = station_select.get()

    cursor.execute("update bikeInformation set isavailable = '{0}', rental_station = '{1}' where bikename = '{2}'" .format(isavailable, rental_station, bike_name))

    db.commit()

    cursor.execute("insert into paymentTracker (email, bikename, amount_charged) values(?, ?, ?)", (email, bike_name, total_amount))

    db.commit()

    show_payment_report(frame, total_amount, email, bike_name)
 
# ------------------- MARK AS DEFECTIVE -------------------
def mark_defective(frame, input_list):
    email = input_list[0]
    bike_selection = input_list[1]
    cursor.execute("update bikeInformation set isavailable = 0, isservicing = 1 where bikename = '{}'" .format(bike_selection.get()))
    db.commit()
    cursor.execute("""create table if not exists reportTracker(
        id integer primary key, 
        email text, 
        bikename text,
        isdefective integer
        )""")
    db.commit()
    isdefective = 1
    cursor.execute("insert into reportTracker (email, bikename, isdefective) values(?,?,?)", (email, bike_selection.get(), isdefective))
    db.commit()
    messagebox.showinfo("Report this bike", "The selected bike has been marked as defective and will be available again after repair.")
    user_profile(frame, email)
# ------------------- REPORT DEFECTIVE -----------------
def report(frame, email):
    frame.forget()
    report_frame = Frame(win, width = width, height = height)
    report_frame.pack(side = "top", fill = "both", expand = True)

    lgn_frame = Frame(win, bg='#d4d4ff', width=950, height=300)
    lgn_frame.place(x=470, y=200)

    lb1 = Label(lgn_frame, text=("Report Bike Here"), font = ("bold",40), bg='#d4d4ff')
    lb1.place(x=280,y=50)

    b1 = Button(lgn_frame, text="Home", command=lambda: UserPortal(report_frame, y[0]))
    b1.place(x=130,y=55,width=100,height=50)

    lb0 = Label(lgn_frame, text="Please select the bike you would like to report as defective", font=("", 16))
    lb0.place(x=100,y=150, width=700,height=40)
    bike_selection = StringVar()
    bike_selection.set("Select a bike")
    cursor.execute("select distinct bikeName from rentTracker where user_email = '{}'" .format(email))
    bike_list = []
    for x in cursor.fetchall():
        bike_list.append(x[0])
    bike_dd = OptionMenu(lgn_frame, bike_selection, *bike_list)
    bike_dd.place(x=320,y=250, width=175,height=40)
    input_list = [email, bike_selection]
    bn0 = Button(lgn_frame, text="Select", command = lambda: mark_defective(lgn_frame, input_list))
    bn0.place(x=520,y=250, width=100,height=40)

 
# ------------------- USER PROFILE ---------------------
def user_profile(frame, email):
    frame.forget()
    profile_frame = Frame(win, width = width, height = height)

    lgn_frame = Frame(win, bg='#d4d4ff', width=950, height=600)
    lgn_frame.place(x=470, y=200)

    lb1 = Label(lgn_frame, text=("User Activity"), font = ("bold",40), bg='#d4d4ff')
    lb1.place(x=280,y=50)

    profile_frame.pack(side = "top", fill = "both", expand = True)
    cursor.execute("select firstname, lastname, email, password from customerProfile where email = '{}' " .format(email))
    y = cursor.fetchall()
    b1 = Button(lgn_frame, text="Home", command=lambda: UserPortal(profile_frame, y[0]))
    b1.place(x=200,y=140,width=150,height=50)
    b0 = Button(lgn_frame, text="Wallet", command=lambda: user_wallet(email))
    b0.place(x=380,y=140, width=150,height=50)
    b2 = Button(lgn_frame, text="Report", command = lambda: report(profile_frame, email))
    b2.place(x=560,y=140, width=150,height=50)

    rental_info = StringVar()
    lb2 = Label(lgn_frame, textvariable=rental_info, font = ("", 16))
    lb2.place(x=340,y=240, width=250,height=50)
    status = "Open"
    cursor.execute("select bikename from rentTracker where user_email = '{0}' and payment_status = '{1}'" .format(email, status))
    x = cursor.fetchall()
    if(len(x) > 0):
        lb1 = Label(lgn_frame, text = "Your Active Rentals", font = ("", 16))
        lb1.place(x=250,y=200, width=200,height=50)
        s = ("Rented bike - {}" .format(x[0][0]))
        rental_info.set(s)
        return_button = Button(lgn_frame, text="Return", command = lambda: get_station(lgn_frame, email, x[0][0]))
        return_button.place(x=620,y=250, width=80,height=40)
        report_button = Button(lgn_frame, text="Report", command = lambda: get_station_report(lgn_frame, email, x[0][0]))
        report_button.place(x=720,y=250, width=80,height=40)
    else:
        s = "No Active Rental"
        rental_info.set(s)
 
# ------------------- USER PORTAL ----------------------

