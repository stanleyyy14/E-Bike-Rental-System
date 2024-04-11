import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from operator_landing_page import *
from manager_landing_page import manager
from customer_landing_page import *
import os
import re
# import cv2
from matplotlib.colors import LinearSegmentedColormap
from PIL import ImageTk
from PIL import Image


# ========================================================================
# ============ Login Window by default (for now) ========================================
# ========================================================================
win = tk.Tk()

width = win.winfo_screenwidth()
height = win.winfo_screenheight()

win.geometry("%dx%d" %(width, height))
# ('1166x718')
win.resizable(0,0)
win.state('zoomed')
win.title('Login Page')



# //////////////////// ids for primary and foreign keys //////////////////////////////////
customer_id=IntVar()
operator_id=IntVar()
manager_id=IntVar()

# ///////////////////////// customer data variables ///////////////////////////////////

customer_nameVar=StringVar()
customer_surnameVar=StringVar()
customer_emailVar=StringVar()
customer_passVar=StringVar()
customer_genderVar = IntVar()
customer_contact_number=StringVar()


# ////////////////////////// operator variables ////////////////////////////
operator_nameVar=StringVar()
operator_surnameVar=StringVar()
operator_gendervar=StringVar()
operator_addressVar=StringVar()
operator_emailVar=StringVar()
operator_passportnoVar=StringVar()
operator_contactVar=StringVar()
operator_bankaccountVar=StringVar()
operator_workinghoursVar=StringVar()
operator_shiftVar=StringVar()
operator_allowancesVar=StringVar()
operator_managerVar=StringVar()
operator_passwordVar=StringVar()

# ////////////////////////// Manager variables ////////////////////////////

manager_nameVar=StringVar()
manager_surnameVar=StringVar()
manager_gendervar=StringVar()
#manager_addressVar=StringVar()
manager_emailVar=StringVar()
manager_passportnoVar=StringVar()
manager_contactVar=StringVar()
manager_bankaccountVar=StringVar()
manager_workinghoursVar=StringVar()
manager_shiftVar=StringVar()
manager_allowancesVar=StringVar()
#manager_managerVar=StringVar()
manager_passwordVar=StringVar()

passStrength = StringVar()
mail_status = StringVar()
not_valid = False

# --------------- VALIDATION FUNCTIONS ---------------
def fnameValidate(input):
    if input != "":
        return True 
    else:
        win.bell()
        # fnameValidation.set("Name can't be null")
        return False 
def lnameValidate(input):
    if input != "":
        return True 
    else:
        win.bell()
        return False 
def cityValidate(input):
    if input == "Glasgow":
        return True
    else:
        win.bell()
        return False
 
def countryValidate(input):
    if input == "United Kingdom":
        return True
    else:
        win.bell()
        return False
 
def checkPassword(input):
    strength = ["Password cannot be blank", "Very weak", "Weak", "Medium", "Srong", "Very Strong"]
    score = 1
    # if len(password) == 0:
    #     passStrength.set(strength[0])
    #     return
    if len(input) < 8:
        if len(input) == 0:
            passStrength.set(strength[0])
            return False
        else:
            passStrength.set(strength[1])
 
        return False
    else: 
        if len(input) >= 8:
            score += 1
        if re.search("[0-9]", input):
            score += 1   
        if re.search("[a-z]", input) and re.search("[A-Z]", input):
            score += 1   
        if re.search("[@_!]", input):
            score += 1
        passStrength.set(strength[score])
        return True
def show_password(passEntry, toggle):
    if(toggle.get() == "True"):
        passEntry.configure(show = "*")
        toggle.set("False")
    else:
        passEntry.configure(show = "")
        toggle.set("True")
def checkEmail(input):
    r = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,7}'
    if(re.fullmatch(r, input)):
        print("valid")
        mail_status.set("Valid email")
        return True 
    else:
        print("invalid")
        mail_status.set("Invalid email")
        return False
 
def phoneValidate(input):
    if input.isdigit() and len(input) < 11:
        return True
    elif input == "":
        print(input)
        return True
    else:
        print(input)
        win.bell()
        return False



# ///////////////////////////////// Database creation /////////////////////////////////////

conn = sqlite3.connect('Database.db')
with conn:
    cursor=conn.cursor()


# /////////////////////////// CUSTOMER CODE ///////////////////////////////////////////////////
def UserPortal(frame, input_list):

    bg_frame = Image.open('images/Bike.png')
    photo = ImageTk.PhotoImage(bg_frame)
    bg_panel = Label(win, image=photo)
    bg_panel.image = photo
    bg_panel.pack(fill='both', expand='yes')

    lgn_frame = Frame(win, bg='#d4d4ff', width=950, height=600)
    lgn_frame.place(x=470, y=200)
    
    frame.forget()
    firstname = input_list[0]
    email = input_list[2]
    user_frame = Frame(win, width = width, height = height)
    user_frame.pack(side = "top", fill = "both", expand = True)
    lb1 = Label(lgn_frame, text=("Welcome, {}" .format(firstname)), font = ("bold",40), bg='#d4d4ff')
    lb1.place(x=300,y=50)

    b0 = Button(lgn_frame, text="Activity", command=lambda: user_profile(lgn_frame, email))
    b0.place(x=150,y=140, width=150,height=50)
    b1 = Button(lgn_frame, text="Wallet", command=lambda: user_wallet(email))
    b1.place(x=320,y=140, width=150,height=50)
    b3 = Button(lgn_frame, text="Report", command=lambda: report(lgn_frame, email))
    b3.place(x=510,y=140, width=150,height=50)
    b4 = Button(lgn_frame, text="Change Password", command=lambda: change_password(email))
    b4.place(x=690,y=140, width=120,height=50)
    b5 = Button(lgn_frame, text="Log out", command=lambda: LoginActivity())
    b5.place(x=835,y=140, width=120,height=50)

    selection = StringVar()
    selection.set("Select a rental station")
    cursor.execute("select distinct BIKE_LOCATION from Bikes")
    rental_station = []
    for x in cursor.fetchall():
        rental_station.append(x[0])
    dd1 = OptionMenu(lgn_frame, selection, *rental_station)
    dd1.place(x=260,y=240, width=200,height=50)
    ddb1 = Button(lgn_frame, text="Select", command = lambda: get_bike_information(lgn_frame, selection, email))
    ddb1.place(x=520,y=250, width=150,height=30)


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
    conn.commit()
    cursor.execute("select available_balance from userWallet where email = '{}'" .format(email))
    x = cursor.fetchall()
    wallet_balance.set(x[0][0])
    input_list[1].delete(0, END)
# ------------------- USER WALLET ----------------------
def user_wallet(email):
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
        conn.commit()
        rent_starttime = datetime.datetime.now()
        rent_endtime = ""
        return_station = ""
        payment_status = "Open"
        cursor.execute("""insert into rentTracker (bikename, user_email, rent_station, return_station, 
                       rent_starttime, rent_endtime, payment_status) values(?,?,?,?,?,?,?)""", 
        (bike_name, email, rental_station, return_station, rent_starttime, rent_endtime, payment_status))
        conn.commit()

        cursor.execute("select bike_id, bike_name from BIKES where bike_name = '{}'" .format(bike_name))
        bikeInfo = cursor.fetchall()
        bike_id = bikeInfo[0][0]
        bikename = bikeInfo[0][1]
        paystatus = 0

        amount = 0
        cursor.execute("insert into payment (amount, payment_status) values(?,?)", (amount, paystatus))
        conn.commit()

        cursor.execute("select MAX(payment_id) from payment")
        pay = cursor.fetchall()
        pay_id = pay[0][0]
        is_offer = 0
        return_time = ""
        
        cursor.execute("""insert into user_util (email, bike_id, bikename, alloted_time, return_time, payment_id, is_offer, payment_status) values(?,?,?,?,?,?,?,?)""", (email, bike_id, bikename, rent_starttime, return_time, pay_id, is_offer, paystatus))
        conn.commit()

        print(bike_name, email, rental_station, return_station, rent_starttime, rent_endtime, payment_status)
        isavailable = 0
        cursor.execute("update BIKES set is_available = '{0}' where bike_name = '{1}'" .format(isavailable, bike_name))
        conn.commit()
        rental_info = ("You have now rented {0} from the rental station {1} \nYou can find the payable amount when you return the vehicle" .format(bike_name, rental_station))
        lb1 = Label(rental_screen, text=rental_info, font=("", 16))
        lb1.grid(row=1, column=0, padx=10, pady=10)
        landing_frame.grid_columnconfigure(0, weight=1)
        rent_button['state'] = "disabled"
        user_profile(frame, email)
# ------------------- TRANSACTION ------------------------
def transaction(screen, frame, total_amount, email, payment_id):
    cursor.execute("select available_balance from userWallet where email = '{}'" .format(email))
    x = cursor.fetchall()
    updated_amount = x[0][0]-total_amount
    if(updated_amount < 0):
        messagebox.showerror("Insufficient Balance", "Please add some funds to your account")
    else:
        cursor.execute("update userWallet set available_balance = '{0}' where email = '{1}'" .format(updated_amount, email))
        conn.commit()
        cursor.execute("update rentTracker set payment_status = 'Closed' where user_email = '{0}'" .format(email))
        conn.commit()
        cursor.execute("update payment set payment_status = 1 where payment_id = '{}'" .format(payment_id))
        conn.commit()
        user_profile(frame, email)
# ------------------- SHOW PAYMENT -----------------------
def show_payment(frame, total_amount, email, payment_id):
    payment_screen = Toplevel(win)
    payment_screen.geometry("500x300")
    payment_screen.title("Payment Screen")
    payable_amount = StringVar()
    t = ("You need to pay the amount of £%.2f" %total_amount)
    payable_amount.set(("You need to pay the amount of £%.2f" %total_amount))
    lb1 = Label(payment_screen, textvariable=payable_amount, font=("", 16))
    lb1.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
    b1 = Button(payment_screen, text="Pay", command = lambda: transaction(payment_screen, frame, total_amount, email, payment_id))
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
    conn.commit()
    total_seconds = (return_time - rent_time).total_seconds()
    total_amount = 0.5 + ((total_seconds/10) * 0.01)
    isavailable = 1
    rental_station = station_select.get()
    cursor.execute("update BIKES set is_available = '{0}', BIKE_LOCATION = '{1}' where BIKE_NAME = '{2}'" .format(isavailable, rental_station, bike_name))
    conn.commit()
    cursor.execute("insert into paymentTracker (email, bikename, amount_charged) values(?, ?, ?)", (email, bike_name, total_amount))
    conn.commit()

    cursor.execute("select payment_id from user_util where bikename = '{0}' and email = '{1}'" .format(bike_name, email))
    payment = cursor.fetchall()
    payment_id = payment[0][0]

    cursor.execute("update user_util set return_time = '{0}' where bikename = '{1}' and email = '{2}'" .format(return_time, bike_name, email))
    conn.commit()

    cursor.execute("update payment set amount = '{0}' where payment_id = '{1}'" .format(total_amount, payment_id))
    conn.commit()

    show_payment(frame, total_amount, email, payment_id)
# ------------------- GET STATION INFORMATION -------------------
def get_station(frame, email, bike_name):
    station_select = StringVar()
    station_select.set("Select a return station")
    cursor.execute("select distinct BIKE_LOCATION from BIKES")
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
    cursor.execute("select BIKE_NAME from BIKES where BIKE_LOCATION = '{0}' and is_available = '{1}' " .format(rental_station, isavailable))
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

    cursor.execute("select distinct BIKE_LOCATION from BIKES")

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

    conn.commit()

    total_seconds = (return_time - rent_time).total_seconds()

    total_amount = 0.5 + ((total_seconds/10) * 0.25)

    isavailable = 1

    rental_station = station_select.get()

    cursor.execute("update BIKES set is_available = '{0}', BIKE_LOCATION = '{1}' where BIKE_NAME = '{2}'" .format(isavailable, rental_station, bike_name))

    conn.commit()

    cursor.execute("insert into paymentTracker (email, bikename, amount_charged) values(?, ?, ?)", (email, bike_name, total_amount))

    conn.commit()

    show_payment_report(frame, total_amount, email, bike_name)
 
# ------------------- MARK AS DEFECTIVE -------------------
def mark_defective(frame, input_list):
    email = input_list[0]
    bike_selection = input_list[1]
    cursor.execute("update BIKES set is_available = 0, is_servicing = 1 where BIKE_NAME = '{}'" .format(bike_selection.get()))
    conn.commit()
    cursor.execute("""create table if not exists reportTracker(
        id integer primary key, 
        email text, 
        bikename text,
        isdefective integer
        )""")
    conn.commit()
    isdefective = 1
    cursor.execute("insert into reportTracker (email, bikename, isdefective) values(?,?,?)", (email, bike_selection.get(), isdefective))
    conn.commit()
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

    cursor.execute("select name, surname, email, password from customers where email = '{}' " .format(email))
    y = cursor.fetchall()

    b1 = Button(lgn_frame, text="Home", command=lambda: UserPortal(report_frame, y[0]))
    b1.place(x=130,y=55,width=100,height=50)
    b5 = Button(lgn_frame, text="Log out", command=lambda: LoginActivity())
    b5.place(x=800,y=55, width=100,height=50)

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
    cursor.execute("select name, surname, email, password from customers where email = '{}' " .format(email))
    y = cursor.fetchall()
    b1 = Button(lgn_frame, text="Home", command=lambda: UserPortal(profile_frame, y[0]))
    b1.place(x=200,y=140,width=150,height=50)
    b0 = Button(lgn_frame, text="Wallet", command=lambda: user_wallet(email))
    b0.place(x=380,y=140, width=150,height=50)
    b2 = Button(lgn_frame, text="Report", command = lambda: report(profile_frame, email))
    b2.place(x=560,y=140, width=150,height=50)
    b5 = Button(lgn_frame, text="Log out", command=lambda: LoginActivity())
    b5.place(x=750,y=140, width=120,height=50)


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

# /////////////////////////////////////// Managers code ///////////////////////////////////////


def manager_landing(frame) :
    '''
    Inital the window to show.
    '''
    manager(frame)
    # Create the manager page.
    # win = tk.Toplevel(win)
    # win.geometry('2000x1500')
    # win.title('Manager Page')

    # managerScreen=Toplevel(win)
    # managerScreen.geometry('2000x1500')
    # managerScreen.title("Registration Here")
    # frame.forget()

    # frame_man = Frame(managerScreen, bg='#d4d4ff', width=2000, height=1000)
    # frame_man.place(x=200, y=200)

    # # bg_frame = Image.open('images/background3.png')
    # # photo = ImageTk.PhotoImage(bg_frame)
    # # bg_panel = Label(win, image=photo)
    # # bg_panel.image = photo
    # # bg_panel.pack(fill='both', expand='yes')


    # # The manager enter the time and find vehicle' status during the period.
    # label1 = Label(managerScreen, text='Enter the period you want to find : ')
    # label1.place(x=50, y=70)

    # time_choices = [  
    #     time(8, 0),   # 08:00 AM
    #     time(10, 0),  
    #     time(12, 0),  # 12:00 PM
    #     time(14, 0),
    #     time(16, 0),
    #     time(18, 0),  # 06:00 PM
    #     time(20, 0),
    #     time(22, 0),
    #     time(0, 0)   
    # ]
    
    # timebox1 = ttk.Combobox(managerScreen, values=time_choices, state='readonly', font=('Helvetica', 12))
    # timebox1.place(x=280, y=70, width=80, height=25)

    # label2 = Label(managerScreen,text=' - ')
    # label2.place(x=380, y=70)       

    # timebox2 = ttk.Combobox(managerScreen, values=time_choices, state='readonly', font=('Helvetica', 12))
    # timebox2.place(x=400, y=70, width=80, height=25)

    # button1 = Button(managerScreen,text='Find', command = lambda: show_vehicle(timebox1, timebox2,managerScreen))
    # button1.place(x=500, y=70, width=50, height=25)

    # button2 = Button(managerScreen,text='Clear', command=clear(managerScreen))
    # button2.place(x=550, y=70, width=50, height=25)

    # button3 = Button(managerScreen,text='Show location', command= lambda: heatmap(managerScreen))
    # button3.place(x=600, y=70, width=100, height=25)

    # button4 = Button(managerScreen,text='Show figures', command=lambda: show_figure(managerScreen))
    # button4.place(x=700, y=70, width=100, height=25)


    # conn = sqlite3.connect('Database.db')

    # with conn:

    #     cursor = conn.cursor()

    # visualize_status()
    # visualize_usage_date()
    # visualize_type_usage()
    # visualize_revenue()

    # figure1 = PhotoImage(file='images/Vehicle_status_chart.png')
    # # figure1 = figure1.subsample(2, 2)
    # img1 = Label(managerScreen, image=figure1)
    # img1.place(x=100, y=100)

    # figure2 = PhotoImage(file='images/Vehicle_date_chart.png')
    # # figure2 = figure2.subsample(2, 2)
    # img2 = Label(managerScreen, image=figure2)
    # img2.place(x=700, y=100)

    # figure3 = PhotoImage(file='images/Vehicle_type_chart.png')
    # # figure3 = figure3.subsample(2, 2)
    # img3 = Label(managerScreen, image=figure3)
    # img3.place(x=100, y=500)

    # figure4 = PhotoImage(file='images/Revenue_chart.png')
    # # figure4 = figure4.subsample(2, 2)
    # img4 = Label(managerScreen, image=figure4)
    # img4.place(x=700, y=500)

    # label3 = Label(text='Enter the operator you want to find : ')
    # label3.place(x=50, y=100)

    # idbox = Entry(text='')
    # idbox.place(x=280, y=100, width=100)

    # button4 = Button(text='Add')
    # button4.place(x=400, y=100, width=50, height=25)

    # button5 = Button(text='Revoke')
    # button5.place(x=450, y =100, width=60, height=25)

# def visualize_status() :

#     cursor.execute('''SELECT is_available, is_servicing, is_charged FROM BIKES''')

#     result = cursor.fetchall()

#     available_count = 0
#     servicing_count = 0
#     charged_count = 0
#     number = []

#     for i in result :

#         if i[0] :

#             available_count += 1

#         elif i[1] :

#             servicing_count += 1

#         else :

#             charged_count += 1
    
#     categories = ['available', 'servicing', 'charged']
#     number.append(available_count)
#     number.append(servicing_count)
#     number.append(charged_count)

#     plt.figure(figsize=(5, 4))
#     plt.bar(categories, number)

#     # Add title and label
#     plt.xlabel('Bike Status')
#     plt.ylabel('Number')
#     plt.title('Vehicle status')

#     # Show number and label
#     for i, count in enumerate(number):
#         plt.text(i, count, str(count), ha='center', va='bottom')

#     # Save image
#     plt.savefig('images/Vehicle_status_chart.png')
#     # plt.show()

# def visualize_usage_date() :

#     cursor.execute('''SELECT substr(alloted_time, 6, 5) FROM user_util''')

#     result = cursor.fetchall()

#     date = [i[0] for i in result]

#     date_dic = {}

#     for i in date :

#         if i in date_dic :

#             date_dic[i] += 1
        
#         else :

#             date_dic[i] = 1

#     date_dic = dict(sorted(date_dic.items()))
#     categories = list(date_dic.keys())
#     number = list(date_dic.values())

#     plt.figure(figsize=(5, 4))
#     plt.plot(categories, number, linestyle='-', color='g', markersize=8, linewidth=1)

#     plt.ylim(0, 5)
#     # Add title and label
#     plt.xlabel('Date')
#     plt.ylabel('Number')
#     plt.title('Vehicle usage in date')

#     # Show number and label
#     for i, count in enumerate(number):
#         plt.text(i, count+0.2, str(count), ha='center', va='bottom')

#     # Save image
#     plt.savefig('images/Vehicle_date_chart.png')
#     # plt.show()

# def visualize_type_usage() :

#     cursor.execute('''SELECT bike_id FROM user_util ''')

#     result = cursor.fetchall()

#     bike_type = []

#     for i in result :

#         cursor.execute('''SELECT BIKE_TYPE FROM BIKES WHERE BIKE_ID = ?''', (i))
#         bike_type.append(str(cursor.fetchall()[0][0]))

#     type_dic = {}

#     for i in bike_type :

#         if i in type_dic :

#             type_dic[i] += 1

#         else :

#             type_dic[i] = 1

#     categories = list(type_dic.keys())
#     number = list(type_dic.values())

#     plt.figure(figsize=(5, 4))
#     plt.bar(categories, number, color=['blue', 'red', 'green'])

#     # Add title and label
#     plt.xlabel('Type')
#     plt.ylabel('Number')
#     plt.title('Vehicle usage in type')

#     # Show number and label
#     for i, count in enumerate(number):
#         plt.text(i, count, str(count), ha='center', va='bottom')

#     # Save image
#     plt.savefig('images/Vehicle_type_chart.png')
#     # plt.show()

# def visualize_revenue() :

#     cursor.execute('''SELECT payment_id, amount, payment_status FROM payment WHERE payment_status = 1''')

#     result = cursor.fetchall()

#     date_payment = []

#     for i in result :

#         cursor.execute('''SELECT substr(return_time, 6, 5) FROM user_util WHERE payment_id = ? and payment_status = 1''', (i[0], ))
#         date_payment.append(str(cursor.fetchall()[0][0]))

#     amount = [i[1] for i in result]
    
#     revenue_dic = {}

#     for d, a in zip(date_payment, amount) :

#         if d in revenue_dic :

#             revenue_dic[d] += a
        
#         else :

#             revenue_dic[d] = a

#     revenue_dic = dict(sorted(revenue_dic.items()))
#     categories = list(revenue_dic.keys())
#     number = list(revenue_dic.values())

#     plt.figure(figsize=(5, 4))
#     plt.plot(categories, number, linestyle='-', color='r', markersize=8, linewidth=1)

#     # Add title and label
#     plt.xlabel('Amount')
#     plt.ylabel('Money')
#     plt.title('Revenue in date')

#     # Show number and label
#     for i, count in enumerate(number):
#         plt.text(i, count+5, str(count), ha='center', va='bottom')

#     # Save image
#     plt.savefig('images/Revenue_chart.png')
#     # plt.show()


# def show_vehicle(timebox1, timebox2,managerScreen) :
#     '''
#     The function is for showing vehicles' status during the defined time period.
#     '''
#     clear(managerScreen)
#     cursor.execute("SELECT id, bike_id, payment_status, substr(alloted_time, 12, 8), substr(return_time, 12, 8) FROM user_util")
#     results = cursor.fetchall()
#     listbox = Listbox(managerScreen)
#     listbox.place(x=200, y=200, width=700, height=400)
#     start = timebox1.get()
#     end = timebox2.get()
#     if start == '' or end == '' :
#         messagebox.showwarning("Warning", "Please choose the start time and the end time!")

#     elif start > end :

#         messagebox.showwarning("Warning", "You can not choose the end time early than the start time!")

#     results = [i for i in results if i[3] >= start and i[4] <= end]

#     bike_status = []

#     for i in results :

#         cursor.execute("SELECT is_available, is_servicing, is_charged FROM BIKES WHERE BIKE_ID = ?", (int(i[1]), ))
#         bike_status.append(cursor.fetchall()[0])
    
#     status = []

#     for i in bike_status :

#         if i == (0, 1, 0) :

#             status.append('is_servicing')
        
#         elif i == (1, 0, 0) :

#             status.append('is_available')

#         else :

#             status.append('is_charged')


#     label3 = Label(managerScreen, text='Bike id')
#     label4 = Label(managerScreen, text='User id')
#     label5 = Label(managerScreen, text='Bike status')
#     label6 = Label(managerScreen, text='Payment status')

#     label3.place(x=200, y=170)  
#     label4.place(x=350, y=170)   
#     label5.place(x=500, y=170) 
#     label6.place(x=650, y=170)

#     # data_list = []

#     for i, vehicle_data in enumerate(results) :

#         listbox.insert(END, str(vehicle_data[1]) + ' '*33 + str(vehicle_data[0]) + ' '*33 + str(status[i]) + ' '*33  + str(vehicle_data[2]) + '\n')
#     #     label7 = Label(window, text=vehicle_data[1])
#     #     label8 = Label(window, text=vehicle_data[0])
#     #     label9 = Label(window, text=status[i])
#     #     label0 = Label(window, text=vehicle_data[2])    

#     #     data_list.append(label7)
#     #     data_list.append(label8)
#     #     data_list.append(label9)
#     #     data_list.append(label0)

#     #     label7.place(x=50, y=120 + (i + 1) * 20)  
#     #     label8.place(x=150, y=120 + (i + 1) * 20)   
#     #     label9.place(x=250, y=120 + (i + 1) * 20) 
#     #     label0.place(x=350, y=120 + (i + 1) * 20)

# def clear(managerScreen) :
#     if hasattr(managerScreen, 'label3') :
#         label3.destroy()
#     if hasattr(managerScreen,'label4') :
#         label4.destroy()
#     if hasattr(managerScreen,'label5') :
#         label5.destroy()    
#     if hasattr(managerScreen,'label6') :
#         label6.destroy()
#     if hasattr(managerScreen,'photobox') :
#         photobox.destroy()
#     if hasattr(managerScreen,'img1') :
#         img1.destroy()
#     if hasattr(managerScreen,'img2') :
#         img2.destroy()
#     if hasattr( managerScreen,'img3') :
#         img3.destroy()
#     if hasattr(managerScreen, 'img4') :
#         img4.destroy()
#     if hasattr(managerScreen, 'listbox') :
#         listbox.destroy()

# # def authority_change(, add=True) :

# #     '''
# #     The function is for changing of authority.

# #     '''
# #     # Connect to the database.
# #     # conn = sqlite3.connect('Database.db')

# #     # with conn:

# #     #     cursor = conn.cursor()
# #     #     cursor.execute()  
# #     if add :

# def show_heatmap(img_path) :
#     # Read the image
#     image = cv2.imread(img_path)  
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     img_width, img_height = gray_image.shape
#     np.random.seed(417)
#     # Connect to the database.
#     cursor.execute("SELECT BIKE_LOCATION FROM BIKES")
#     results = cursor.fetchall()
#     results = [str(i[0]) for i in results]
#     #print('gdfgdfgfffffffffffffffffffffffffffffffffffffffff')
#     count_partick = 0
#     count_ave = 0
#     count_st = 0
#     count_maclay = 0
#     count_bath = 0
#     for i in results :
#         if i == 'Partick Rental Station':
#             count_partick += 1
#         elif i == 'University Ave. Rental Station':
#             count_ave += 1
#         elif i == 'Argyle St. Rental Station':
#             count_st += 1
#         elif i == 'Maclay Rental Station' :
#             count_maclay += 1
#         elif i == 'Bath St. Rental Station' :
#             count_bath += 1
#     # count_partick = 10
#     # count_ave = 5
#     # count_st = 15
#     # count_maclay = 7
#     # count_bath = 3

#     x_partick = np.random.randint(152, 447, count_partick)
#     y_partick = np.random.randint(324, 566, count_partick)

#     x_ave = np.random.randint(859, 1185, count_ave)
#     y_ave = np.random.randint(62, 251, count_ave)

#     x_st = np.random.randint(920, 1223, count_st)
#     y_st = np.random.randint(490, 688, count_st)

#     x_maclay = np.random.randint(687, 1040, count_maclay)
#     y_maclay = np.random.randint(832, 1107, count_maclay)

#     x_bath = np.random.randint(2030, 2380, count_bath)
#     y_bath = np.random.randint(688, 998, count_bath)

#     # Create a blank heat map
#     heatmap = np.zeros_like(gray_image)

#     # Add data points to heat map
#     for x, y in zip(x_partick, y_partick): 
#         heatmap[y - 8 : y + 8, x - 8 : x + 8] += 50

#     for x, y in zip(x_ave, y_ave): 
#         heatmap[y - 8 : y + 8, x - 8 : x + 8] += 50

#     for x, y in zip(x_st, y_st): 
#         heatmap[y - 8 : y + 8, x - 8 : x + 8] += 50

#     for x, y in zip(x_maclay, y_maclay): 
#         heatmap[y - 8 : y + 8, x - 8 : x + 8] += 50

#     for x, y in zip(x_bath, y_bath): 
#         heatmap[y - 8 : y + 8, x - 8 : x + 8] += 50

#     # Define color mapping
#     colors = [(1, 1, 1), (1, 0, 0)]  
#     cmap = LinearSegmentedColormap.from_list("custom_colormap", colors, N=256)

#     plt.figure(figsize=(10, 8))
#     plt.clf()

#     # Draw heat map
#     plt.imshow(heatmap, cmap=cmap)  # Set alpha value to make heatmap translucent
#     plt.imshow(image, alpha=0.6)  
#     plt.axis("off") 

#     # Save result
#     plt.savefig("images/heatmap_on_image.png", bbox_inches="tight", pad_inches=0, dpi=300)
#     # plt.show()

# def heatmap(managerScreen) :
#     '''
#     The function is for bicycles' visualization.
#     '''
#     clear(managerScreen)
#     show_heatmap("images/glasgow_map.png")
#     photo = PhotoImage(file='images/heatmap_on_image.png')
#     photo = photo.subsample(2, 2)
#     photobox = Label(managerScreen, image=photo)
#     photobox.place(x=130, y=130, width=1200, height=600)

# def show_figure(managerScreen) :
    clear(managerScreen)
    visualize_status()
    visualize_usage_date()
    visualize_type_usage()
    visualize_revenue()

    figure1 = PhotoImage(file='images/Vehicle_status_chart.png')
    # figure1 = figure1.subsample(2, 2)
    img1 = Label(managerScreen, image=figure1)
    img1.place(x=100, y=100)

    figure2 = PhotoImage(file='images/Vehicle_date_chart.png')
    # figure2 = figure2.subsample(2, 2)
    img2 = Label(managerScreen, image=figure2)
    img2.place(x=700, y=100)

    figure3 = PhotoImage(file='images/Vehicle_type_chart.png')
    # figure3 = figure3.subsample(2, 2)
    img3 = Label(managerScreen, image=figure3)
    img3.place(x=100, y=500)

    figure4 = PhotoImage(file='images/Revenue_chart.png')
    # figure4 = figure4.subsample(2, 2)
    img4 = Label(managerScreen, image=figure4)
    img4.place(x=700, y=500)



# ////////////////////////////////////////// Databases created ////////////////////////////////

cursor.execute('''
    CREATE TABLE IF NOT EXISTS payment (
        payment_id INTEGER PRIMARY KEY,
        amount REAL,
        payment_status INTEGER
    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS customers
             (customer_id INTEGER PRIMARY KEY,
              name TEXT,
              surname TEXT,
              gender INTEGER,
              address TEXT,
              email TEXT,
              contact_number TEXT,
              password TEXT
              )''')

cursor.execute("create table if not exists userWallet (email text, available_balance integer)")
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS operators
             (operator_id INTEGER PRIMARY KEY,
              name TEXT,
              surname TEXT,
              gender TEXT,
              address TEXT,
              email TEXT,
              passport_no TEXT,
              contact TEXT,
              bank_account TEXT,
              working_hours TEXT,
              shift TEXT,
              allowances TEXT,
              manager TEXT,
              password TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS managers
             (manager_id INTEGER PRIMARY KEY,
              name TEXT,
              surname TEXT,
              gender TEXT,
              email TEXT,
              passport_no TEXT,
              contact TEXT,
              bank_account TEXT,
              working_hours TEXT,
              shift TEXT,
              allowances TEXT,
              password TEXT)''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS BIKES (
        BIKE_ID INTEGER PRIMARY KEY,
        BIKE_TYPE TEXT,
        BIKE_NAME TEXT,
        BIKE_MODEL TEXT,
        BIKE_LOCATION TEXT,
        is_available INTEGER,
        is_servicing INTEGER,
        is_charged INTEGER
    )
''')
cursor.execute("""create table if not exists rentTracker(
            id integer primary key,
            bikename text,
            user_email text,
            rent_station text,
            return_station text, 
            rent_starttime text, 
            rent_endtime text,
            payment_status text)""")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_util (
        id INTEGER PRIMARY KEY,
        email text,
        bike_id INTEGER,
        bikename text,
        alloted_time DATETIME,
        return_time DATETIME,
        payment_id INTEGER,
        is_offer INTEGER,
        payment_status INTEGER,
        FOREIGN KEY (id) REFERENCES customers(id),
        FOREIGN KEY (bike_id) REFERENCES bikes(bike_id),
        FOREIGN KEY (payment_id) REFERENCES payment(payment_id)
    )''')
print ("Created all databases")
'''
# Insert data for managers
managers_data = [
    ("John", "Doe", "male",  "manager1@example.com", "MGR123", "1234567890", "123-456-789", "9-5", "Day", "$1000", "manager1password"),
    ("Jane", "Smith", "female", "manager2@example.com", "MGR456", "9876543210", "987-654-321", "8-4", "Day", "$1200", "manager2password"),
    ("Bob", "Johnson", "male", "manager3@example.com", "MGR789", "5555555555", "555-555-555", "10-6", "Night", "$800", "manager3password")
]
cursor.executemany("INSERT INTO managers (name, surname, gender, address, email, passport_no, contact, bank_account, working_hours, shift, allowances, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", managers_data)
print("Inserted managers Data")
# Insert data for operators
operators_data = [
    ("Operator 1", "Lola", "male", "123 Operator St.", "operator1@example.com", "OPR123", "1234567890", "123-456-789", "9-5", "Day", "$100", "Manager 1", "operator1password"),
    ("Operator 2", "Lola1", "female", "456 Operator Ave.", "operator2@example.com", "OPR456", "9876543210", "987-654-321", "8-4", "Day", "$120", "Manager 2", "operator2password"),
    ("Operator 3", "Lola3", "male", "789 Operator Rd.", "operator3@example.com", "OPR789", "5555555555", "555-555-555", "10-6", "Night", "$80", "Manager 3", "operator3password")
]
cursor.executemany("INSERT INTO operators (name, surname, gender, address, email, passport_no, contact, bank_account, working_hours, shift, allowances, manager, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", operators_data)
print("Inserted operators Data")
# Insert data for customers
customers_data = [
    ("Alice", "Bond", "female", "123 Customer St.", "customer1@example.com", 1234567890, "customer1password"),
    ("Bob", "Bond1", "male", "456 Customer Ave.", "customer2@example.com", 9876543210, "customer2password"),
    ("Carol", "Bond2", "female", "789 Customer Rd.", "customer3@example.com", 5555555555, "customer3password"),
    ("David", "Bond3", "male", "101 Customer Ln.", "customer4@example.com", 1111111111, "customer4password"),
    ("Eve", "Bond4", "female", "202 Customer Blvd.", "customer5@example.com", 2222222222, "customer5password")
]
cursor.executemany("INSERT INTO customers (name, email, gender, address, email, contact_number, password) VALUES (?, ?, ?, ?, ?, ?, ?)", customers_data)
print("Inserted customers Data")
'''

# ////////////////////// to destroy a window ///////////////////////////////

def destroywindow(fr):
    fr.destroy()

# ========================================================================
# ============ method to add user register data in database ========================================
# ========================================================================


# ///////////////////////// generate customer ids ///////////////////////////////////////
'''
def generate_customer_id():
    cursor.execute("SELECT MAX(id) FROM CUSTOMER_TABLE")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id else 1

def generate_operator_id():
    cursor.execute("SELECT MAX(id) FROM OPERATOR_TABLE")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id else 1

def generate_manager_id():
    cursor.execute("SELECT MAX(id) FROM MANAGER_TABLE")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id else 1'''
# //////////////////////////////////////////////////////////////////////////////////////

cursor.execute("""CREATE TABLE IF NOT EXISTS CUSTOMER_TABLE
                (CUSTOMER_ID INTEGER PRIMARY KEY AUTOINCREMENT,CUSTOMER_NAME TEXT, CUSTOMER_SURNAME TEXT,CUSTOMER_GENDER TEXT, CUSTOMER_EMAIL TEXT,CUSTOMER_PASSWORD TEXT);""")
print("Table created")



def addNewCustomer(window):
    name=customer_nameVar.get()
    surname=customer_surnameVar.get()
    email=customer_emailVar.get()
    password=customer_passVar.get()
    gender=customer_genderVar.get()
    contact_number=customer_contact_number.get()

    emailValidationFlag = True
    r = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,7}'
    if(re.fullmatch(r, email)):
        emailValidationFlag = False

    if(name == "" or surname == "" or email == "" or password == "" or gender == "" or contact_number == ""):
        messagebox.showerror("Registration Error", "Please make sure to fill all the fields")
    elif emailValidationFlag == True:
        messagebox.showerror("Email Error", "Invalid Email")
    else:
        print("Called add customer method")
        
        count=cursor.execute("INSERT INTO customers (name, surname, email, password, gender, contact_number) VALUES (?, ?, ?, ?, ?, ?)",
                (name, surname, email, password, gender, contact_number))
        conn.commit()

        print('hey')

        initial_balance = 0
        cursor.execute("insert into userWallet (email, available_balance) values(?,?)", (email, initial_balance))
        conn.commit()
        print('vsdfgs')

        print("Data inserted")
        if(cursor.rowcount>0):
            print ("Signup Done")
            #LoginActivity()
            messagebox.showinfo("Success!!!","You have registered successfully. Now Login")
            #registerScreen.destroy()
        else:
            print ("Signup Error")
    
        window.destroy()

    

# ========================================================================
# ============ method to perform login ========================================
# ========================================================================

def loginNow(lgn_frame):
    email=customer_emailVar.get()
    password=customer_passVar.get()
    conn = sqlite3.connect('Database.db')
    with conn:
        cursor=conn.cursor()
    cursor.execute("select name, surname, email, password from customers where email = '{}' " .format(email))
    x = cursor.fetchall()
    print(email, password)
    if x[0][3] == password:
        UserPortal(lgn_frame, x[0])
    else:
        messagebox.showerror("Login Failed!", "Invalid username or password.")
    conn.commit()

# ========================================================================
# ============ register page ========================================
# ========================================================================

def registerWindow():
    
    # registerScreen=Toplevel(win)
    # registerScreen.title("Registration Here")

    
    # bg_frame = Image.open('images/background3.png')
    # photo = ImageTk.PhotoImage(bg_frame)
    # bg_panel = Label(registerScreen, image=photo)
    # bg_panel.image = photo
    # bg_panel.pack(fill='both', expand='yes')
    
    # #OperatorLoginActivity.lgn_frame_op.destroy()
    
    # label = Label(registerScreen, text="Registration Here",width=20,fg="blue",font=("bold", 20))
    # label.place(x=90,y=53)

    # reg_frame = Frame(registerScreen, bg='#d4d4ff', width=950, height=600)
    # reg_frame.place(x=200, y=90)

    # reg_form_frame = Frame(reg_frame, bg='#964b85', width=360, height=250)
    # reg_form_frame.place(x=520, y=300)

    # '''reg_frame = tk.Frame(window)
    # reg_frame.pack(padx=20, pady=20)'''

    # # Labels and Entry widgets using grid
    
    # tk.Label(reg_form_frame, text="Id", width=20, font=("bold", 10)).grid(row=0, column=0)
    # nameEntery = tk.Entry(reg_form_frame, textvariable=customer_id)
    # nameEntery.grid(row=0, column=1)

    # tk.Label(reg_form_frame, text="Name", width=20, font=("bold", 10)).grid(row=1, column=0)
    # nameEntery = tk.Entry(reg_form_frame, textvariable=customer_nameVar)
    # nameEntery.grid(row=1, column=1)

    # tk.Label(reg_form_frame, text="Surname", width=20, font=("bold", 10)).grid(row=2, column=0)
    # surnameEntery = tk.Entry(reg_form_frame, textvariable=customer_surnameVar)
    # surnameEntery.grid(row=2, column=1)

    # tk.Label(reg_form_frame, text="Gender", width=20, font=("bold", 10)).grid(row=3, column=0)
    # tk.Radiobutton(reg_form_frame, text="Male", padx=5, variable=customer_genderVar, value=1).grid(row=3, column=1)
    # tk.Radiobutton(reg_form_frame, text="Female", padx=20, variable=customer_genderVar, value=2).grid(row=3, column=2)

    # tk.Label(reg_form_frame, text="Email", width=20, font=("bold", 10)).grid(row=4, column=0)
    # emailEntry = tk.Entry(reg_form_frame, textvariable=customer_emailVar)
    # emailEntry.grid(row=4, column=1)

    # tk.Label(reg_form_frame, text="Password", width=20, font=("bold", 10)).grid(row=5, column=0)
    # passwordEntry = tk.Entry(reg_form_frame, textvariable=customer_passVar)
    # passwordEntry.grid(row=5, column=1)


    # tk.Button(reg_form_frame, text='Submit', width=20, bg='blue', fg='white', pady=5, command=addNewCustomer).grid(row=13, column=1)

    registerScreen=Toplevel(win)
    registerScreen.title("Registration Here")
    
    passStrength.set("")
    mail_status.set("")

    bg_frame = Image.open('images/background1.png')
    photo = ImageTk.PhotoImage(bg_frame)
    bg_panel = Label(registerScreen, image=photo)
    bg_panel.image = photo
    bg_panel.pack(fill='both', expand='yes')
 
    reg_frame = Frame(registerScreen, bg='#d4d4ff', width=1050, height=600)
    reg_frame.place(x=200, y=70)
 
    side_image = Image.open('images/register_side_screen.png')
    #side_image = Image.open('images/vector.png')
    photo = ImageTk.PhotoImage(side_image)
    side_image_label = Label(reg_frame, image=photo, bg='#d4d4ff')
    side_image_label.image = photo
    side_image_label.place(x=5, y=60)
   
    label = Label(reg_frame, text="Create your account",width=20,fg="blue",font=("bold", 20))
    label.place(x=290,y=53)
 
    nameLabel = Label(reg_frame, text="First Name",width=20,font=("bold", 10))
    nameLabel.place(x=525,y=210)
   
    fName = win.register(fnameValidate)
 
    nameEntery = Entry(reg_frame,textvar=customer_nameVar, validate="key", validatecommand=(fName, "%P"))
    #nameEntery.pack()
    nameEntery.place(x=710,y=210,width=150)
 
    #nameEntery = Entry(reg_frame,textvar=customer_nameVar)
    #nameEntery.place(x=460,y=130)
 
    surnameLabel = Label(reg_frame, text="Last Name",width=20,font=("bold", 10))
    surnameLabel.place(x=525,y=240)
    
    lName = win.register(lnameValidate)
    surnameEntery = Entry(reg_frame,textvar=customer_surnameVar)
    surnameEntery.configure(validate="key", validatecommand=(lName, "%P"))
    surnameEntery.place(x=710,y=240,width=150)
 
    genderLabel = Label(reg_frame, text="Gender",width=20,font=("bold", 10))
    genderLabel.place(x=525,y=270)
 
    Radiobutton(reg_frame, text="Male",padx = 5, variable=customer_genderVar, value=1).place(x=710,y=270)
    Radiobutton(reg_frame, text="Female",padx = 5, variable=customer_genderVar, value=2).place(x=780,y=270)
    Radiobutton(reg_frame, text="Other",padx = 1, variable=customer_genderVar, value=3).place(x=860,y=270)
   
    emailLabel = Label(reg_frame, text="Email",width=20,font=("bold", 10))
    emailLabel.place(x=525,y=300)
 
    emailEntry = Entry(reg_frame,textvar=customer_emailVar)
    emailV = win.register(checkEmail)
    emailEntry.configure(validate="focusout", validatecommand=(emailV, "%P"))
    emailEntry.place(x=710,y=300,width=150)

    EmailLabelValidate = Label(reg_frame, textvariable = mail_status, width=20, font=("bold", 10), bg='#d4d4ff')
    EmailLabelValidate.place(x=855,y=300)
 
    NumberLabel = Label(reg_frame, text="Mobile Number",width=20,font=("bold", 10))
    NumberLabel.place(x=525,y=330)
 
    phoneV = win.register(phoneValidate)
 
    NumberEntry = Entry(reg_frame,textvar=customer_contact_number,validate="key", validatecommand=(phoneV, "%P"))
    #NumberEntry.pack()
 
    #NumberEntry = Entry(reg_frame,textvar=customer_contact_number)
    NumberEntry.place(x=710,y=330,width=150)
 
    passLabel = Label(reg_frame, text="Password",width=20,font=("bold", 10))
    passLabel.place(x=525,y=360)
 
    passEntry = Entry(reg_frame,textvar=customer_passVar)
    passV = win.register(checkPassword)
    passEntry.configure(validate="focusout", validatecommand=(passV, "%P"))
    passEntry.place(x=710,y=360,width=150)

    passwordLabel = Label(reg_frame, textvariable = passStrength, width=20, font=("bold", 10), bg='#d4d4ff')
    passwordLabel.place(x=710,y=385)
 
    Button(reg_frame, text='Submit',width=20,bg='blue',fg='white',pady=5,command= lambda: addNewCustomer(registerScreen)).place(x=620,y=420)

# ========================================================================
# ============ Login Window by default (for now) ========================================
# ========================================================================

 

def LoginActivity():
    # ========================================================================
    # ============================background image============================
    # ========================================================================

    bg_frame = Image.open('images/Bike.png')
    photo = ImageTk.PhotoImage(bg_frame)
    bg_panel = Label(win, image=photo)
    bg_panel.image = photo
    bg_panel.pack(fill='both', expand='yes')

    # ====== Login Frame =========================
   
    lgn_frame = Frame(win, bg='#d4d4ff', width=950, height=600)
    lgn_frame.place(x=470, y=200)

    # ========================================================================
    # ========================================================
    # ========================================================================

    txt = "Welcome to GLAS'E-GO"
    heading = Label(lgn_frame, text=txt, font=('yu gothic ui', 20, "bold"), bg="#d4d4ff",
                            fg='black',
                            bd=10,
                            relief=FLAT)
    heading.place(x=300, y=30, width=300, height=30)

    # ========================================================================
    # ============ Left Side Image ================================================
    # ========================================================================

    side_image = Image.open('images/bikesmain.png')
    photo = ImageTk.PhotoImage(side_image)
    side_image_label = Label(lgn_frame, image=photo, bg='#d4d4ff')
    side_image_label.image = photo
    side_image_label.place(x=5, y=100)

    # ========================================================================
    # ============ Sign In Image =============================================
    # ========================================================================

    sign_in_image = Image.open('images/hyy.png')
    photo = ImageTk.PhotoImage(sign_in_image)
    sign_in_image_label = Label(lgn_frame, image=photo, bg='#d4d4ff')
    sign_in_image_label.image = photo
    sign_in_image_label.place(x=620, y=130)


    # ========================================================================
    # ============ Sign In label =============================================
    # ========================================================================

    form_frame = Frame(lgn_frame, bg='#964b85', width=315, height=250)
    form_frame.place(x=550, y=300)

    sign_in_label = Label(lgn_frame, text="Sign In", bg="#d4d4ff", fg="black",
                                font=("yu gothic ui", 17, "bold"))
    sign_in_label.place(x=650, y=240)
    emailLabel = Label(form_frame, text="Email",width=10,font=("bold", 10))
    emailLabel.place(x=20,y=20)
    emailEntry = Entry(form_frame,width = 25,textvar=customer_emailVar)
    emailEntry.place(x=120,y=20)
    passwordLabel = Label(form_frame, text="Password",width=10,font=("bold", 10))
    passwordLabel.place(x=20,y=65)

    passwordEntry = Entry(form_frame,width = 25, textvar=customer_passVar)
    passwordEntry.place(x=120,y=65) 

    # //////////////// Password icon ////////////////////////////////////

    def show():
        hide_button = Button(form_frame, image=hide_image, command=hide, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
        hide_button.place(x=280, y=65)
        passwordEntry.config(show='')

    def hide():
        show_button = Button(form_frame, image=show_image, command=show, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
        show_button.place(x=280, y=65)
        passwordEntry.config(show='*')

    show_image = ImageTk.PhotoImage \
        (file='images/show.png')

    hide_image = ImageTk.PhotoImage \
        (file='images/hide.png')

    show_button = Button(form_frame, image=show_image, command=hide, relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand2")
    show_button.place(x=280, y=65)

    # //////////////////// Clear email and password entry ////////////////

    emailEntry.delete(0,END)
    passwordEntry.delete(0,END)


    # ///////////////////// Password icon eye ///////////////////////////////

    Button(form_frame, text='Login Now',width=23,bg='blue',fg='white',pady=5, command= lambda:  loginNow(lgn_frame)).place(x=60,y=120)

    Button(form_frame,text="Have no Accout! Create one",bg="red",fg="white",font=("bold",10), command=registerWindow).place(x=60,y=170)

    # win.mainloop()



# =====================================================================================
# ================================== Operator add =============================
# =====================================================================================

def addOperator(window):
    name=operator_nameVar.get()
    surname=operator_surnameVar.get()
    gender=operator_gendervar.get()
    address=operator_addressVar.get()
    email=operator_emailVar.get()
    passport_no=operator_passportnoVar.get()
    contact=operator_contactVar.get()
    bank_account=operator_bankaccountVar.get()
    working_hours=operator_workinghoursVar.get()
    shift=operator_shiftVar.get()
    allowances=operator_allowancesVar.get()
    manager=operator_managerVar.get()
    password=operator_passwordVar.get()

    emailValidationFlag = False
    r = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,7}'
    if(re.fullmatch(r, email)):
        emailValidationFlag = True

    if(name == "" or surname == "" or email == "" or password == "" or contact == ""):
        messagebox.showerror("Registration Error", "Please make sure to fill all the fields")
    elif emailValidationFlag == False:
        messagebox.showerror("Email Error", "Invalid Email")
    else:

        count=cursor.execute("INSERT INTO operators (name, surname, gender, address, email, passport_no, contact, bank_account, working_hours, shift, allowances, manager, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name, surname, gender, address, email, passport_no, contact, bank_account, working_hours, shift, allowances, manager, password))
        print("Data inserted")
        if(cursor.rowcount>0):
            print ("Signup Done")
            #LoginActivity()
            messagebox.showinfo("Success!!!","You have registered successfully. Now Login")
            #registerScreen.destroy()
        else:
            print ("Signup Error")
        
        conn.commit()

        window.destroy()


# =====================================================================================
# ================================== Operator Login =============================
# =====================================================================================
def opclearloginfields(email,password):
    email.delete(0,'END')
    password.delete(0,'END')
    

def loginNowOp():
    email=operator_emailVar.get()
    password=operator_passwordVar.get()
    conn = sqlite3.connect('Database.db')
    with conn:
        cursor=conn.cursor()
    cursor.execute(f"SELECT password FROM operators WHERE email = '{email}'")
    print(email)
    check_password = cursor.fetchone()
    print(password)
    print(check_password)
    print(check_password[0])
    if check_password[0] == password:
        open_operator_window(win)
    else:
        messagebox.showerror("Login Failed!", "Invalid username or password.")
    conn.commit()

def loginNowMan(lgn_frame_op):
    lgn_frame_op.forget()
    email=manager_emailVar.get()
    password=manager_passwordVar.get()
    conn = sqlite3.connect('Database.db')
    with conn:
        cursor=conn.cursor()
    cursor.execute(f"SELECT password FROM managers WHERE email = '{email}'")
    print(email)
    check_password = cursor.fetchone()
    print(password)
    print(check_password)
    print(check_password[0])
    if check_password[0] == password:
        manager_landing(lgn_frame_op)
        # messagebox.showinfo("Login success!", "Show the manager page now.")
    else:
        messagebox.showerror("Login Failed!", "Invalid username or password.")
    conn.commit()

# =====================================================================================
# ================================== Operator register =============================
# =====================================================================================



def OperatorRegisterActivity():

    OpregisterScreen=Toplevel(win)
    OpregisterScreen.title("Operator Registration Here")
 
   
    bg_frame = Image.open('images/background1.png')
    photo = ImageTk.PhotoImage(bg_frame)
    bg_panel = Label(OpregisterScreen, image=photo)
    bg_panel.image = photo
    bg_panel.pack(fill='both', expand='yes')

    passStrength.set("")
    mail_status.set("")
   
    #OperatorLoginActivity.lgn_frame_op.destroy()
   
    label = Label(OpregisterScreen, text="Registration Here",width=20,fg="blue",font=("bold", 20))
    label.place(x=490,y=53)
 
    operator_reg_frame = Frame(OpregisterScreen, bg='#d4d4ff', width=1100, height=600)
    operator_reg_frame.place(x=200, y=90)
 
    side_image = Image.open('images/operator.png')
    #side_image = Image.open('images/vector.png')
    photo = ImageTk.PhotoImage(side_image)
    side_image_label = Label(OpregisterScreen, image=photo, bg='#d4d4ff')
    side_image_label.image = photo
    side_image_label.place(x=200, y=150)
 
    operator_reg_form_frame = Frame(operator_reg_frame, bg='#964b85', width=500, height=400)
    operator_reg_form_frame.place(x=480, y=110)
 
    '''reg_frame = tk.Frame(window)
    reg_frame.pack(padx=20, pady=20)'''
 
    # Labels and Entry widgets using grid
 
    nameLabel = Label(operator_reg_frame, text="First Name",width=20,font=("bold", 10))
    nameLabel.place(x=525,y=180)
   
    fname = win.register(fnameValidate)
 
    nameEntery = Entry(operator_reg_frame,textvar=operator_nameVar, validate="key", validatecommand=(fname, "%P"))
    #nameEntery.pack()
    nameEntery.place(x=710,y=180,width=150)
 
    #nameEntery = Entry(reg_frame,textvar=customer_nameVar)
    #nameEntery.place(x=460,y=130)
 
    surnameLabel = Label(operator_reg_frame, text="Last Name",width=20,font=("bold", 10))
    surnameLabel.place(x=525,y=210)
 
    surnameEntery = Entry(operator_reg_frame,textvar=operator_surnameVar)
    surnameEntery.configure(validate="key", validatecommand=(fname, "%P"))
    surnameEntery.place(x=710,y=210,width=150)
 
    genderLabel = Label(operator_reg_frame, text="Gender",width=20,font=("bold", 10))
    genderLabel.place(x=525,y=240)
 
    Radiobutton(operator_reg_frame, text="Male",padx = 5, variable=operator_gendervar, value=1).place(x=710,y=240)
    Radiobutton(operator_reg_frame, text="Female",padx = 5, variable=operator_gendervar, value=2).place(x=780,y=240)
    Radiobutton(operator_reg_frame, text="Other",padx = 1, variable=operator_gendervar, value=3).place(x=860,y=240)
   
    emailLabel = Label(operator_reg_frame, text="Email",width=20,font=("bold", 10))
    emailLabel.place(x=525,y=270)
 
    emailV = win.register(checkEmail)
    emailEntry = Entry(operator_reg_frame,textvar=operator_emailVar)
    emailEntry.configure(validate="focusout", validatecommand=(emailV, "%P"))
    emailEntry.place(x=710,y=270,width=150)

    emailVLabel = Label(operator_reg_frame, textvariable=mail_status,width=14,font=("bold", 10), bg='#964b85')
    emailVLabel.place(x=850,y=270)
 
    passport_label = Label(operator_reg_frame, text="Passport No", width=20, font=("bold", 10))
    passport_label.place(x=525,y=300)
 
    passportEntry = tk.Entry(operator_reg_frame, textvariable=operator_passportnoVar)
    passportEntry.place(x=710,y=300,width=150)
 
    NumberLabel = Label(operator_reg_frame, text="Contact No",width=20,font=("bold", 10))
    NumberLabel.place(x=525,y=330)
 
    phoneV = win.register(phoneValidate)
 
    contactEntry = Entry(operator_reg_frame,textvar=operator_contactVar,validate="key", validatecommand=(phoneV, "%P"))
    #NumberEntry.pack()
 
    #NumberEntry = Entry(reg_frame,textvar=customer_contact_number)
    contactEntry.place(x=710,y=330,width=150)
 
    bank_label = Label(operator_reg_frame, text="Bank Account", width=20, font=("bold", 10))
    bank_label.place(x=525,y=360)
 
    bankEntry = tk.Entry(operator_reg_frame, textvariable=operator_bankaccountVar)
    bankEntry.place(x=710,y=360,width=150)
 
    workhours_label = Label(operator_reg_frame, text="Working Hours", width=20, font=("bold", 10))
    workhours_label.place(x=525,y=390)
 
    workingHrsEntry = tk.Entry(operator_reg_frame, textvariable=operator_workinghoursVar)
    workingHrsEntry.place(x=710,y=390,width=150)
 
    passLabel = Label(operator_reg_frame, text="Password",width=20,font=("bold", 10))
    passLabel.place(x=525,y=420)
    
    passV = win.register(checkPassword)
    passEntry = Entry(operator_reg_frame,textvar=operator_passwordVar, validate="focusout", validatecommand=(passV, "%P"))
    passEntry.place(x=710,y=420,width=150)

    passVLabel = Label(operator_reg_frame, textvariable=passStrength,width=14,font=("bold", 10), bg='#964b85')
    passVLabel.place(x=850,y=420)
 
    Button(operator_reg_frame, text='Submit',width=20,bg='blue',fg='white',pady=5,command = lambda: addOperator(OpregisterScreen)).place(x=620,y=460)

    # OpregisterScreen=Toplevel(win)
    # OpregisterScreen.title("Registration Operator Here")

    
    # bg_frame = Image.open('images/background1.png')
    # photo = ImageTk.PhotoImage(bg_frame)
    # bg_panel = Label(OpregisterScreen, image=photo)
    # bg_panel.image = photo
    # bg_panel.pack(fill='both', expand='yes') 
    
    # #OperatorLoginActivity.lgn_frame_op.destroy()
    
    # label = Label(OpregisterScreen, text="Registration Here",width=20,fg="blue",font=("bold", 20))
    # label.place(x=150,y=53)

    # reg_frame_op = Frame(OpregisterScreen, bg='#d4d4ff', width=800, height=500)
    # reg_frame_op.place(x=470, y=200)

    # reg_frame = Frame(OpregisterScreen, bg='#d4d4ff', width=950, height=600)
    # reg_frame.place(x=200, y=90)

    # '''reg_frame = tk.Frame(window)
    # reg_frame.pack(padx=20, pady=20)'''

    # # Labels and Entry widgets using grid
    
    # tk.Label(reg_frame, text="Id", width=20, font=("bold", 10)).grid(row=0, column=0)
    # nameEntery = tk.Entry(reg_frame, textvariable=operator_nameVar)
    # nameEntery.grid(row=0, column=1)

    # tk.Label(reg_frame, text="Name", width=20, font=("bold", 10)).grid(row=1, column=0)
    # nameEntery = tk.Entry(reg_frame, textvariable=operator_nameVar)
    # nameEntery.grid(row=1, column=1)

    # tk.Label(reg_frame, text="Surname", width=20, font=("bold", 10)).grid(row=2, column=0)
    # surnameEntery = tk.Entry(reg_frame, textvariable=operator_surnameVar)
    # surnameEntery.grid(row=2, column=1)

    # tk.Label(reg_frame, text="Gender", width=20, font=("bold", 10)).grid(row=3, column=0)
    # tk.Radiobutton(reg_frame, text="Male", padx=5, variable=operator_gendervar, value=1).grid(row=3, column=1)
    # tk.Radiobutton(reg_frame, text="Female", padx=20, variable=operator_gendervar, value=2).grid(row=3, column=2)

    # tk.Label(reg_frame, text="Email", width=20, font=("bold", 10)).grid(row=4, column=0)
    # emailEntry = tk.Entry(reg_frame, textvariable=operator_emailVar)
    # emailEntry.grid(row=4, column=1)

    # tk.Label(reg_frame, text="Passport No", width=20, font=("bold", 10)).grid(row=5, column=0)
    # passportEntry = tk.Entry(reg_frame, textvariable=operator_passportnoVar)
    # passportEntry.grid(row=5, column=1)

    # tk.Label(reg_frame, text="Contact No", width=20, font=("bold", 10)).grid(row=6, column=0)
    # contactEntry = tk.Entry(reg_frame, textvariable=operator_contactVar)
    # contactEntry.grid(row=6, column=1)

    # tk.Label(reg_frame, text="Bank Account", width=20, font=("bold", 10)).grid(row=7, column=0)
    # bankEntry = tk.Entry(reg_frame, textvariable=operator_bankaccountVar)
    # bankEntry.grid(row=7, column=1)

    # tk.Label(reg_frame, text="Working Hours", width=20, font=("bold", 10)).grid(row=8, column=0)
    # workingHrsEntry = tk.Entry(reg_frame, textvariable=operator_workinghoursVar)
    # workingHrsEntry.grid(row=8, column=1)

    # tk.Label(reg_frame, text="Shift Hours", width=20, font=("bold", 10)).grid(row=9, column=0)
    # shiftEntry = tk.Entry(reg_frame, textvariable=operator_shiftVar)
    # shiftEntry.grid(row=9, column=1)

    # tk.Label(reg_frame, text="Allowances", width=20, font=("bold", 10)).grid(row=10, column=0)
    # allowanceEntry = tk.Entry(reg_frame, textvariable=operator_allowancesVar)
    # allowanceEntry.grid(row=10, column=1)

    # tk.Label(reg_frame, text="Manager", width=20, font=("bold", 10)).grid(row=11, column=0)
    # managerEntry = tk.Entry(reg_frame, textvariable=operator_managerVar)
    # managerEntry.grid(row=11, column=1)

    # tk.Label(reg_frame, text="Password", width=20, font=("bold", 10)).grid(row=12, column=0)
    # passEntry = tk.Entry(reg_frame, textvariable=operator_passwordVar, show='*')
    # passEntry.grid(row=12, column=1)

    # tk.Button(reg_frame, text='Submit', width=20, bg='blue', fg='white', pady=5, command=addOperator).grid(row=13, column=1)
    #destroywindow(registerScreen)


def addManager(window):
    name=manager_nameVar.get()
    surname=manager_surnameVar.get()
    gender=manager_gendervar.get()
    email=manager_emailVar.get()
    passport_no=manager_passportnoVar.get()
    contact=manager_contactVar.get()
    bank_account=manager_bankaccountVar.get()
    working_hours=manager_workinghoursVar.get()
    #shift=manager_shiftVar.get()
    allowances=manager_allowancesVar.get()
    password=manager_passwordVar.get()

    emailValidationFlag = False
    r = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,7}'
    if(re.fullmatch(r, email)):
        emailValidationFlag = True

    if(name == "" or surname == "" or email == "" or password == "" or contact == ""):
        messagebox.showerror("Registration Error", "Please make sure to fill all the fields")
    elif emailValidationFlag == False:
        messagebox.showerror("Email Error", "Invalid Email")
    else:

        count=cursor.execute("INSERT INTO managers (name, surname, gender, email, passport_no, contact, bank_account, working_hours, allowances, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name, surname, gender, email, passport_no, contact, bank_account, working_hours, allowances, password))
        print("Data inserted")
        if(cursor.rowcount>0):
            print ("Signup Done")
            #LoginActivity()
            messagebox.showinfo("Success!!!","You have registered successfully. Now Login")
            #registerScreen.destroy()
        else:
            print ("Signup Error")
        
        conn.commit()
        window.destroy()


def validate_text(text):
    # Check if the input text contains only alphabetic characters
    return text.isalpha()
 
def validate_numbers(P):
    # Check if the input contains only numeric characters
    return P.isdigit()
    
def ManagerRegisterActivity():
    # mnregisterScreen=Toplevel(win)
    # mnregisterScreen.title("Registration Manager Here")

    
    # bg_frame = Image.open('images/background1.png')
    # photo = ImageTk.PhotoImage(bg_frame)
    # bg_panel = Label(mnregisterScreen, image=photo)
    # bg_panel.image = photo
    # bg_panel.pack(fill='both', expand='yes') 
    
    # #OperatorLoginActivity.lgn_frame_op.destroy()
    
    # label = Label(mnregisterScreen, text="Registration Here",width=20,fg="blue",font=("bold", 20))
    # label.place(x=150,y=53)

    # reg_frame_mn = Frame(mnregisterScreen, bg='#d4d4ff', width=800, height=500)
    # reg_frame_mn.place(x=470, y=200)

    # reg_form_frame = Frame(reg_frame_mn, bg='#d4d4ff', width=950, height=600)
    # reg_form_frame.place(x=200, y=120)

    # '''reg_frame = tk.Frame(window)
    # reg_frame.pack(padx=20, pady=20)'''

    # # Labels and Entry widgets using grid
    
    # tk.Label(reg_form_frame, text="Id", width=20, font=("bold", 10)).grid(row=0, column=0)
    # nameEntery = tk.Entry(reg_form_frame, textvariable=manager_id)
    # nameEntery.grid(row=0, column=1)

    # tk.Label(reg_form_frame, text="Name", width=20, font=("bold", 10)).grid(row=1, column=0)
    # nameEntery = tk.Entry(reg_form_frame, textvariable=manager_nameVar)
    # nameEntery.grid(row=1, column=1)

    # tk.Label(reg_form_frame, text="Surname", width=20, font=("bold", 10)).grid(row=2, column=0)
    # surnameEntery = tk.Entry(reg_form_frame, textvariable=manager_surnameVar)
    # surnameEntery.grid(row=2, column=1)

    # tk.Label(reg_form_frame, text="Gender", width=20, font=("bold", 10)).grid(row=3, column=0)
    # tk.Radiobutton(reg_form_frame, text="Male", padx=5, variable=manager_gendervar, value=1).grid(row=3, column=1)
    # tk.Radiobutton(reg_form_frame, text="Female", padx=20, variable=manager_gendervar, value=2).grid(row=3, column=2)

    # tk.Label(reg_form_frame, text="Email", width=20, font=("bold", 10)).grid(row=4, column=0)
    # emailEntry = tk.Entry(reg_form_frame, textvariable=manager_emailVar)
    # emailEntry.grid(row=4, column=1)

    # tk.Label(reg_form_frame, text="Passport No", width=20, font=("bold", 10)).grid(row=5, column=0)
    # passportEntry = tk.Entry(reg_form_frame, textvariable=manager_passportnoVar)
    # passportEntry.grid(row=5, column=1)

    # tk.Label(reg_form_frame, text="Contact No", width=20, font=("bold", 10)).grid(row=6, column=0)
    # contactEntry = tk.Entry(reg_form_frame, textvariable=manager_contactVar)
    # contactEntry.grid(row=6, column=1)

    # tk.Label(reg_form_frame, text="Bank Account", width=20, font=("bold", 10)).grid(row=7, column=0)
    # bankEntry = tk.Entry(reg_form_frame, textvariable=manager_bankaccountVar)
    # bankEntry.grid(row=7, column=1)

    # tk.Label(reg_form_frame, text="Working Hours", width=20, font=("bold", 10)).grid(row=8, column=0)
    # workingHrsEntry = tk.Entry(reg_form_frame, textvariable=manager_workinghoursVar)
    # workingHrsEntry.grid(row=8, column=1)

    # tk.Label(reg_form_frame, text="Shift Hours", width=20, font=("bold", 10)).grid(row=9, column=0)
    # shiftEntry = tk.Entry(reg_form_frame, textvariable=manager_shiftVar)
    # shiftEntry.grid(row=9, column=1)

    # tk.Label(reg_form_frame, text="Allowances", width=20, font=("bold", 10)).grid(row=10, column=0)
    # allowanceEntry = tk.Entry(reg_form_frame, textvariable=manager_allowancesVar)
    # allowanceEntry.grid(row=10, column=1)

    # tk.Label(reg_form_frame, text="Password", width=20, font=("bold", 10)).grid(row=12, column=0)
    # passEntry = tk.Entry(reg_form_frame, textvariable=manager_passwordVar, show='*')
    # passEntry.grid(row=12, column=1)

    # tk.Button(reg_form_frame, text='Submit', width=20, bg='blue', fg='white', pady=5, command=addManager).grid(row=13, column=1)

    mnregisterScreen=Toplevel(win)
    mnregisterScreen.title("Manager Registration Here")
 
    bg_frame = Image.open('images/background1.png')
    photo = ImageTk.PhotoImage(bg_frame)
    bg_panel = Label(mnregisterScreen, image=photo)
    bg_panel.image = photo
    bg_panel.pack(fill='both', expand='yes')

    passStrength.set("")
    mail_status.set("")
   
    #OperatorLoginActivity.lgn_frame_op.destroy()
 
    label = Label(mnregisterScreen, text="Registration Here",width=20,fg="blue",font=("bold", 20))
    label.place(x=490,y=53)
 
    reg_frame_mn = Frame(mnregisterScreen, bg='#d4d4ff', width=1200, height=600)
    reg_frame_mn.place(x=100, y=90)
 
    side_image = Image.open('images/manager.png')
    #side_image = Image.open('images/vector.png')
    photo = ImageTk.PhotoImage(side_image)
    side_image_label = Label(mnregisterScreen, image=photo, bg='#d4d4ff')
    side_image_label.image = photo
    side_image_label.place(x=110, y=160)
 
    manager_reg_form_frame = Frame(reg_frame_mn, bg='#964b85', width=490, height=410)
    manager_reg_form_frame.place(x=560, y=90)
 
    # Labels and Entry widgets using grid
 
    nameLabel = Label(reg_frame_mn, text="First Name",width=20,font=("bold", 10))
    nameLabel.place(x=575,y=180)
   
    fname = win.register(fnameValidate)
 
    nameEntery = Entry(reg_frame_mn,textvar=manager_nameVar, validate="key", validatecommand=(fname, "%P"))
    #nameEntery.pack()
    nameEntery.place(x=750,y=180,width=150)
 
    #nameEntery = Entry(reg_frame,textvar=customer_nameVar)
    #nameEntery.place(x=460,y=130)
 
    surnameLabel = Label(reg_frame_mn, text="Last Name",width=20,font=("bold", 10))
    surnameLabel.place(x=575,y=210)
    
    lname = win.register(lnameValidate)
    surnameEntery = Entry(reg_frame_mn,textvar=manager_surnameVar)
    surnameEntery.configure(validate="key", validatecommand=(lname, "%P"))
    surnameEntery.place(x=750,y=210,width=150)
 
    genderLabel = Label(reg_frame_mn, text="Gender",width=20,font=("bold", 10))
    genderLabel.place(x=575,y=240)
 
    Radiobutton(reg_frame_mn, text="Male",padx = 5, variable=manager_gendervar, value=1).place(x=750,y=240)
    Radiobutton(reg_frame_mn, text="Female",padx = 1, variable=manager_gendervar, value=2).place(x=820,y=240)
    Radiobutton(reg_frame_mn, text="Other",padx = 1, variable=manager_gendervar, value=3).place(x=890,y=240)
   
    emailLabel = Label(reg_frame_mn, text="Email",width=20,font=("bold", 10))
    emailLabel.place(x=575,y=270)
 
    emailEntry = Entry(reg_frame_mn,textvar=manager_emailVar)
    emailV = win.register(checkEmail)
    emailEntry.configure(validate="focusout", validatecommand=(emailV, "%P"))
    emailEntry.place(x=750,y=270,width=150)

    emailValidateLabel = Label(reg_frame_mn, textvariable = mail_status, width=14, font=("bold", 10), bg='#964b85')
    emailValidateLabel.place(x=890,y=270)
 
    passport_label = Label(reg_frame_mn, text="Passport No", width=20, font=("bold", 10))
    passport_label.place(x=575,y=300)
 
    passportEntry = tk.Entry(reg_frame_mn, textvariable=manager_passportnoVar)
    passportEntry.place(x=750,y=300,width=150)
 
    NumberLabel = Label(reg_frame_mn, text="Contact No",width=20,font=("bold", 10))
    NumberLabel.place(x=575,y=330)
 
    validate_numbers_func = win.register(validate_numbers)
 
    contactEntry = Entry(reg_frame_mn,textvar=manager_contactVar,validate="key", validatecommand=(validate_numbers_func, "%P"))
    #NumberEntry.pack()
 
    #NumberEntry = Entry(reg_frame,textvar=customer_contact_number)
    contactEntry.place(x=750,y=330,width=150)
 
    bank_label = Label(reg_frame_mn, text="Bank Account", width=20, font=("bold", 10))
    bank_label.place(x=575,y=360)
 
    bankEntry = tk.Entry(reg_frame_mn, textvariable=manager_bankaccountVar)
    bankEntry.place(x=750,y=360,width=150)
 
    workhours_label = Label(reg_frame_mn, text="Working Hours", width=20, font=("bold", 10))
    workhours_label.place(x=575,y=390)
 
    workingHrsEntry = tk.Entry(reg_frame_mn, textvariable=manager_workinghoursVar)
    workingHrsEntry.place(x=750,y=390,width=150)
 
    allowances_label = Label(reg_frame_mn, text="Allowances", width=20, font=("bold", 10))
    allowances_label.place(x=575,y=420)
 
    allowanceEntry = tk.Entry(reg_frame_mn, textvariable=manager_allowancesVar)
    allowanceEntry.place(x=750,y=390,width=150)
 
    passLabel = Label(reg_frame_mn, text="Password",width=20,font=("bold", 10))
    passLabel.place(x=575,y=420)
    
    passV = win.register(checkPassword)
    passEntry = Entry(reg_frame_mn,textvar=manager_passwordVar)
    passEntry.configure(validate="focusout", validatecommand=(passV, "%P"))
    passEntry.place(x=750,y=420,width=150)
 
    passValidateLabel = Label(reg_frame_mn, textvariable = passStrength, width=14, font=("bold", 10), bg='#964b85')
    passValidateLabel.place(x=890,y=420)
   
   
    # tk.Label(manager_reg_form_frame, text="Id", width=20, font=("bold", 10)).grid(row=0, column=0)
    # nameEntery = tk.Entry(manager_reg_form_frame, textvariable=operator_nameVar)
    # nameEntery.grid(row=0, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Name", width=20, font=("bold", 10)).grid(row=1, column=0)
    # nameEntery = tk.Entry(manager_reg_form_frame, textvariable=operator_nameVar)
    # nameEntery.grid(row=1, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Surname", width=20, font=("bold", 10)).grid(row=2, column=0)
    # surnameEntery = tk.Entry(manager_reg_form_frame, textvariable=operator_surnameVar)
    # surnameEntery.grid(row=2, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Gender", width=20, font=("bold", 10)).grid(row=3, column=0)
    # tk.Radiobutton(manager_reg_form_frame, text="Male", padx=5, variable=operator_gendervar, value=1).grid(row=3, column=1)
    # tk.Radiobutton(manager_reg_form_frame, text="Female", padx=20, variable=operator_gendervar, value=2).grid(row=3, column=2)
 
    # tk.Label(manager_reg_form_frame, text="Email", width=20, font=("bold", 10)).grid(row=4, column=0)
    # emailEntry = tk.Entry(manager_reg_form_frame, textvariable=operator_emailVar)
    # emailEntry.grid(row=4, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Passport No", width=20, font=("bold", 10)).grid(row=5, column=0)
    # passportEntry = tk.Entry(manager_reg_form_frame, textvariable=operator_passportnoVar)
    # passportEntry.grid(row=5, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Contact No", width=20, font=("bold", 10)).grid(row=6, column=0)
    # contactEntry = tk.Entry(manager_reg_form_frame, textvariable=operator_contactVar)
    # contactEntry.grid(row=6, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Bank Account", width=20, font=("bold", 10)).grid(row=7, column=0)
    # bankEntry = tk.Entry(manager_reg_form_frame, textvariable=operator_bankaccountVar)
    # bankEntry.grid(row=7, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Working Hours", width=20, font=("bold", 10)).grid(row=8, column=0)
    # workingHrsEntry = tk.Entry(manager_reg_form_frame, textvariable=operator_workinghoursVar)
    # workingHrsEntry.grid(row=8, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Shift Hours", width=20, font=("bold", 10)).grid(row=9, column=0)
    # shiftEntry = tk.Entry(manager_reg_form_frame, textvariable=operator_shiftVar)
    # shiftEntry.grid(row=9, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Allowances", width=20, font=("bold", 10)).grid(row=10, column=0)
    # allowanceEntry = tk.Entry(manager_reg_form_frame, textvariable=operator_allowancesVar)
    # allowanceEntry.grid(row=10, column=1)
 
    # tk.Label(manager_reg_form_frame, text="Password", width=20, font=("bold", 10)).grid(row=12, column=0)
    # passEntry = tk.Entry(manager_reg_form_frame, textvariable=operator_passwordVar, show='*')
    # passEntry.grid(row=12, column=1)
    Button(reg_frame_mn, text='Submit',width=20,bg='blue',fg='white',pady=5,command= lambda: addManager(mnregisterScreen)).place(x=680,y=460)
    #tk.Button(manager_reg_form_frame, text='Submit', width=20, bg='blue', fg='white', pady=5, command=addManager).grid(row=13, column=1)

def OperatorLoginActivity():
    # ============================background image============================
    '''
    bg_frame = Image.open('images/background1.png')
    photo = ImageTk.PhotoImage(bg_frame)
    bg_panel = Label(win, image=photo)
    bg_panel.image = photo
    bg_panel.pack(fill='both', expand='yes')
    '''
    # ====== Login Frame =========================

    #LoginActivity.lgn_frame.destroy()
    lgn_frame_op = Frame(win, bg='#d4d4ff', width=950, height=600)
    lgn_frame_op.place(x=470, y=200)

    # ========================================================

    txt = "WELCOME OPERATOR"
    heading = Label(lgn_frame_op, text=txt, font=('yu gothic ui', 25, "bold"), bg="#d4d4ff",
                            fg='black',
                            bd=10,
                            relief=FLAT)
    heading.place(x=300, y=30, width=350, height=30)

    # ============ Left Side Image ================================================

    side_image = Image.open('images/electric.png')
    photo = ImageTk.PhotoImage(side_image)
    side_image_label = Label(lgn_frame_op, image=photo, bg='#d4d4ff')
    side_image_label.image = photo
    side_image_label.place(x=5, y=100)

    # ============ Sign In Image =============================================

    sign_in_image = Image.open('images/hyy.png')
    photo = ImageTk.PhotoImage(sign_in_image)
    sign_in_image_label = Label(lgn_frame_op, image=photo, bg='#d4d4ff')
    sign_in_image_label.image = photo
    sign_in_image_label.place(x=620, y=130)

    # ============ Sign In label =============================================

    form_frame = Frame(lgn_frame_op, bg='#964b85', width=315, height=250)
    form_frame.place(x=550, y=300)

    sign_in_label = Label(lgn_frame_op, text="Sign In", bg="#d4d4ff", fg="black",
                                font=("yu gothic ui", 17, "bold"))
    sign_in_label.place(x=650, y=240)
    emailLabel = Label(form_frame, text="Email",width=10,font=("bold", 10))
    emailLabel.place(x=20,y=20)
    emailEntry = Entry(form_frame,width = 25,textvar=operator_emailVar)
    emailEntry.place(x=120,y=20)
    passwordLabel = Label(form_frame, text="Password",width=10,font=("bold", 10))
    passwordLabel.place(x=20,y=65)

    passwordEntry = Entry(form_frame,width = 25, textvar=operator_passwordVar)
    passwordEntry.place(x=120,y=65) 

    # //////////////// Password icon ////////////////////////////////////

    def show():
        hide_button = Button(form_frame, image=hide_image, command=hide, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
        hide_button.place(x=280, y=65)
        passwordEntry.config(show='')

    def hide():
        show_button = Button(form_frame, image=show_image, command=show, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
        show_button.place(x=280, y=65)
        passwordEntry.config(show='*')

    show_image = ImageTk.PhotoImage \
        (file='images/show.png')

    hide_image = ImageTk.PhotoImage \
        (file='images/hide.png')

    show_button = Button(form_frame, image=show_image, command=hide, relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand2")
    show_button.place(x=280, y=65)

    # //////////////////// Clear email and password entry ////////////////

    emailEntry.delete(0,END)
    passwordEntry.delete(0,END)
    # ///////////////////// Password icon eye ///////////////////////////////

    Button(form_frame, text='Login Now',width=23,bg='blue',fg='white',pady=5, command=loginNowOp).place(x=60,y=120)

    Button(form_frame,text="Have no Accout! Create one",bg="red",fg="white",font=("bold",10), command=OperatorRegisterActivity).place(x=60,y=170)


def ManagerLoginActivity():
    # ============================background image============================
    '''
    bg_frame = Image.open('images/background1.png')
    photo = ImageTk.PhotoImage(bg_frame)
    bg_panel = Label(win, image=photo)
    bg_panel.image = photo
    bg_panel.pack(fill='both', expand='yes')
    '''
    # ====== Login Frame =========================

    #LoginActivity.lgn_frame.destroy()
    lgn_frame_op = Frame(win, bg='#d4d4ff', width=950, height=600)
    lgn_frame_op.place(x=470, y=200)

    # ========================================================

    txt = "WELCOME MANAGER"
    heading = Label(lgn_frame_op, text=txt, font=('yu gothic ui', 25, "bold"), bg="#d4d4ff",
                            fg='black',
                            bd=10,
                            relief=FLAT)
    heading.place(x=300, y=30, width=350, height=30)

    # ============ Left Side Image ================================================

    side_image = Image.open('images/man.png')
    photo = ImageTk.PhotoImage(side_image)
    side_image_label = Label(lgn_frame_op, image=photo, bg='#d4d4ff')
    side_image_label.image = photo
    side_image_label.place(x=5, y=100)

    # ============ Sign In Image =============================================

    sign_in_image = Image.open('images/hyy.png')
    photo = ImageTk.PhotoImage(sign_in_image)
    sign_in_image_label = Label(lgn_frame_op, image=photo, bg='#d4d4ff')
    sign_in_image_label.image = photo
    sign_in_image_label.place(x=620, y=130)

    # ============ Sign In label =============================================

    form_frame = Frame(lgn_frame_op, bg='#964b85', width=315, height=250)
    form_frame.place(x=550, y=300)

    sign_in_label = Label(lgn_frame_op, text="Sign In", bg="#d4d4ff", fg="black",
                                font=("yu gothic ui", 17, "bold"))
    sign_in_label.place(x=650, y=240)
    emailLabel = Label(form_frame, text="Email",width=10,font=("bold", 10))
    emailLabel.place(x=20,y=20)
    emailEntry = Entry(form_frame,width = 25,textvar=manager_emailVar)
    emailEntry.place(x=120,y=20)
    passwordLabel = Label(form_frame, text="Password",width=10,font=("bold", 10))
    passwordLabel.place(x=20,y=65)

    passwordEntry = Entry(form_frame,width = 25, textvar=manager_passwordVar)
    passwordEntry.place(x=120,y=65) 

    # //////////////// Password icon ////////////////////////////////////

    def show():
        hide_button = Button(form_frame, image=hide_image, command=hide, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
        hide_button.place(x=280, y=65)
        passwordEntry.config(show='')

    def hide():
        show_button = Button(form_frame, image=show_image, command=show, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
        show_button.place(x=280, y=65)
        passwordEntry.config(show='*')

    show_image = ImageTk.PhotoImage \
        (file='images/show.png')

    hide_image = ImageTk.PhotoImage \
        (file='images/hide.png')

    show_button = Button(form_frame, image=show_image, command=hide, relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand2")
    show_button.place(x=280, y=65)

    # //////////////////// Clear email and password entry ////////////////

    emailEntry.delete(0,END)
    passwordEntry.delete(0,END)


    # ///////////////////// Password icon eye ///////////////////////////////
    
    Button(form_frame, text='Login Now',width=23,bg='blue',fg='white',pady=5, command= lambda: manager_landing(win)).place(x=60,y=120)

    Button(form_frame,text="Have no Accout! Create one",bg="red",fg="white",font=("bold",10), command=ManagerRegisterActivity).place(x=60,y=170)

def change_password(email):
    def save_password():
        old_password = old_password_entry.get()
        new_password = new_password_entry.get()
        
        if not old_password or not new_password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        # Check if the old password matches the one in the database
        cursor.execute("SELECT password FROM customers WHERE email=?", (email,))
        result = cursor.fetchone()
        
        if result and result[0] == old_password:
            # Update the password in the database
            cursor.execute("UPDATE customers SET password=? WHERE email=?", (new_password, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Password changed successfully.")
            old_password_entry.delete(0, tk.END)
            new_password_entry.delete(0, tk.END)
            top.destroy()
        else:
            messagebox.showerror("Error", "Old password does not match.")
    
    top = tk.Toplevel(win)
    top.geometry('200x200')
    top.title("Change Password")
 
    # Labels and Entry widgets
    old_password_label = tk.Label(top, text="Old Password:")
    old_password_label.pack()
    old_password_entry = tk.Entry(top)
    old_password_entry.pack()
 
    new_password_label = tk.Label(top, text="New Password:")
    new_password_label.pack()
    new_password_entry = tk.Entry(top)
    new_password_entry.pack()

 
    # Change Password button in the pop-up window
    change_password_button = tk.Button(top, text="Change Password", command=save_password)
    change_password_button.pack()





menu_bar = tk.Menu(win)
# Create a top-level menu
menu = tk.Menu(menu_bar, tearoff=0)
# Add menu items and associate them with functions
menu.add_command(label="Operator", command = OperatorLoginActivity)
menu.add_command(label="Manager", command = ManagerLoginActivity)
menu.add_command(label="Customer", command=LoginActivity)
# Add the menu to the menu bar
menu_bar.add_cascade(label="Admin Portal", menu=menu)
# Configure the root window to use the menu bar
win.config(menu=menu_bar)




LoginActivity()
win.mainloop()