import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3
from tkinter import messagebox
import random
import time
from PIL import ImageTk
from PIL import Image
 
# Connect to the SQLite database
conn = sqlite3.connect('Database.db')
with conn:
    cursor=conn.cursor()
 
def generate_bike_id():
    cursor.execute("SELECT MAX(BIKE_ID) FROM BIKES")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id else 1
 
 
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------####### Tracking Functionality ########---------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------
def tracking_functionality(operator_window):
    # Initialize the main window
    window = tk.Toplevel(operator_window)
    window.title("Bike Tracking")
    window.geometry('1166x718')
 
    # Create a dropdown menu to select bike locations
    location_label = tk.Label(window, text="Select Location:")
    location_label.pack()
    location_var = tk.StringVar()
    location_var.set("Select Location")
    location_dropdown = tk.OptionMenu(window, location_var, *get_locations())
    location_dropdown.pack()
 
    # Create a function to update the bike list when a location is selected
    def update_bike_list(*args):
        selected_location = location_var.get()
        print(selected_location)
        bikes = get_bikes_at_location(selected_location)
        update_bike_display(bikes)
 
    location_var.trace("w", update_bike_list)
 
    # Create labels for bike details
    labels_frame = tk.Frame(window)
    labels_frame.pack()
    labels = ["Bike ID", "Type", "Name", "Model", "Available for Rent", "Is Servicing Needed", "Is Bike Charged"]
    for label in labels:
        tk.Label(labels_frame, text=label, padx=10, width=15).pack(side=tk.LEFT)
 
    # Create a function to update the bike details display
    def update_bike_display(bikes):
        print(len(bikes))
        for widget in bike_display_frame.winfo_children():
            widget.destroy()
 
        for bike in bikes:
            print("Inside For")
            bike_id,bike_type, name, model, location, isavail, isservice, ischarged = bike
            print(f"bike_id: {bike_id}, name: {name}, bike_type: {bike_type}, model: {model}, location: {location}")
 
            row_frame = tk.Frame(bike_display_frame)
            row_frame.pack()
 
            name_label = tk.Label(row_frame, text=bike_id, width=15)
            name_label.pack(side=tk.LEFT)
 
            type_label = tk.Label(row_frame, text=bike_type, width=15)
            type_label.pack(side=tk.LEFT)
 
            model_label = tk.Label(row_frame, text=name, width=15)
            model_label.pack(side=tk.LEFT)
 
            name_label = tk.Label(row_frame, text=model, width=15)
            name_label.pack(side=tk.LEFT)
 
            '''type_label = tk.Label(row_frame, text=location, width=15)
            type_label.pack(side=tk.LEFT)'''
 
            model_label = tk.Label(row_frame, text=isavail, width=15)
            model_label.pack(side=tk.LEFT)
 
            type_label = tk.Label(row_frame, text=isservice, width=15)
            type_label.pack(side=tk.LEFT)
 
            model_label = tk.Label(row_frame, text=ischarged, width=15)
            model_label.pack(side=tk.LEFT)
 
    # Create a frame to display bike details
    bike_display_frame = tk.Frame(window)
    bike_display_frame.pack()
 
 
def get_locations():
    # Connect to the SQLite database
    conn = sqlite3.connect("Database.db")
    cursor = conn.cursor()
 
    # Fetch unique bike locations from the database
    cursor.execute("SELECT DISTINCT BIKE_LOCATION FROM BIKES")
    locations = [row[0] for row in cursor.fetchall()]
    return locations
 
def get_bikes_at_location(location):
    # Connect to the SQLite database
    conn = sqlite3.connect("Database.db")
    cursor = conn.cursor()
 
    # Fetch bike details for a specific location
    cursor.execute("SELECT * FROM BIKES WHERE BIKE_LOCATION=?", (location,))
    bikes = cursor.fetchall()
    return bikes
 
def open_operator_window(root):
    # Create a new window for the operator
    operator_window = Toplevel(root)
    operator_window.title("Operator Dashboard")
    operator_window.geometry('1166x718')
    operator_window.resizable(0,0)
    operator_window.state('zoomed')
 
    bg_frame = Image.open('images/background3.png')
    photo = ImageTk.PhotoImage(bg_frame)
    bg_panel = Label(operator_window, image=photo)
    bg_panel.image = photo
    bg_panel.pack(fill='both', expand='yes')
 
    # ====== Login Frame =========================
   
    operator_window_frame = Frame(operator_window, bg='#d4d4ff', width=950, height=600)
    operator_window_frame.place(x=470, y=200)
   
    # Welcome Label
    welcome_label = Label(operator_window_frame, text="Welcome Operator",width=20,fg="blue",font=("bold", 20))
    welcome_label.place(x=150,y=53)
   
    track_add_remove_frame = Frame(operator_window_frame, bg='#d4d4ff', width=800, height=500)
    track_add_remove_frame.place(x=150, y=100)
 
    bike_data_frame = Frame(operator_window_frame, width=800, height=500)
    bike_data_frame.place(x=50, y=200)
 
    scrollbar = tk.Scrollbar(bike_data_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")
 
    # Create a Canvas widget for the bike data
    canvas = tk.Canvas(bike_data_frame, yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
 
    # Configure the scrollbar to work with the canvas
    scrollbar.config(command=canvas.yview)
 
    # Create a frame to hold your actual bike data
    actual_bike_data_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=actual_bike_data_frame, anchor="nw")
    # ////////////////////////////// Bike Registration functionality ///////////////////////////////////////////////
 
    def bike_registration():
 
        # Labels and Entry fields
        isavailable_var = BooleanVar()
        isservicing_var = BooleanVar()
        ischarged_var = BooleanVar()
 
        bike_reg_frame = Frame(operator_window, bg='#d4d4ff', width=950, height=600)
        bike_reg_frame.place(x=470, y=200)
 
        side_image = Image.open('images/man.png')
        photo = ImageTk.PhotoImage(side_image)
        side_image_label = Label(bike_reg_frame, image=photo, bg='#d4d4ff')
        side_image_label.image = photo
        side_image_label.place(x=50, y=150)
 
        form_frame = Frame(bike_reg_frame, bg='#ffe16b',width=950, height=600)
        form_frame.place(x=500, y=200)
 
        txt = "BIKE REGISTRATION"
        heading = Label(bike_reg_frame, text=txt, font=('yu gothic ui', 25, "bold"), bg="#d4d4ff",
                                    fg='black',
                                    bd=10,
                                    relief=FLAT)
        heading.place(x=300, y=30, width=300, height=30)
 
        bike_id_label = ttk.Label(form_frame, text="Bike ID")
        bike_id = ttk.Entry(form_frame, state='readonly')
        bike_id.insert(0, generate_bike_id())
 
        bike_type_label = ttk.Label(form_frame, text="Bike Type")
        bike_type_combo = ttk.Combobox(form_frame, values=['electric bike', 'electric car', 'electric motorbike', 'electric scooter'])
 
        bike_name_label = ttk.Label(form_frame, text="Bike Name")
        bike_name_entry = ttk.Entry(form_frame)
 
        bike_model_label = ttk.Label(form_frame, text="Bike Model")
        bike_model_entry = ttk.Entry(form_frame)
 
        bike_location_label = ttk.Label(form_frame, text="Bike Location")
        bike_location_combo = ttk.Combobox(form_frame, values=['Glasgow University', 'City Centre', 'Scotstounhill', 'Partick', 'Rutherglen'])
 
 
        bike_isavailable_check = ttk.Checkbutton(form_frame, text="Available",variable=isavailable_var)
        bike_isservicing_check = ttk.Checkbutton(form_frame, text="In Service", variable=isservicing_var)
        bike_ischarged_check = ttk.Checkbutton(form_frame, text="Charged",variable=ischarged_var)
 
        bike_id_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        bike_id.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        bike_type_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        bike_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        bike_name_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        bike_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        bike_model_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        bike_model_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        bike_location_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        bike_location_combo.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        bike_isavailable_check.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        bike_isservicing_check.grid(row=6, column=0, padx=5, pady=5, sticky='w')
        bike_ischarged_check.grid(row=7, column=0, padx=5, pady=5, sticky='w')
 
        # Function to insert data into the database
        def insert_data():
            #bike_id = generate_bike_id()
            cursor.execute('''
                INSERT INTO BIKES ( BIKE_TYPE, BIKE_NAME, BIKE_MODEL, BIKE_LOCATION, is_available, is_servicing, is_charged)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ( bike_type_combo.get(), bike_name_entry.get(), bike_model_entry.get(), bike_location_combo.get(), isavailable_var.get(), isservicing_var.get(), ischarged_var.get()))
            conn.commit()
            reset_form()
            bike_id.delete(0, 'end')
 
        # Function to reset the form
        def reset_form():
            bike_type_combo.delete(0, 'end')
            bike_name_entry.delete(0, 'end')
            bike_model_entry.delete(0, 'end')
            bike_location_combo.delete(0, 'end')
            '''bike_isavailable_check.deselect()
            bike_isservicing_check.deselect()
            bike_ischarged_check.deselect()'''
 
        submit_button = ttk.Button(form_frame, text="Submit", command=insert_data)
        submit_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)
 
   
    # Buttons to Add Remove and track Bikes
    add_bikes_button = tk.Button(track_add_remove_frame, text="Add Bikes", command=bike_registration)
    add_bikes_button.grid(column=0,row=0)
 
    # //////////////////////// Bike Removal Functionality /////////////////////////////////////////////
 
 
    def bike_removal():
        bike_rem_frame = Frame(operator_window, bg='#d4d4ff', width=950, height=600)
        bike_rem_frame.place(x=470, y=200)
 
        side_image = Image.open('images/no-bicycle-icon.png')
        photo = ImageTk.PhotoImage(side_image)
        side_image_label = Label(bike_rem_frame, image=photo, bg='#d4d4ff')
        side_image_label.image = photo
        side_image_label.place(x=120, y=150)
 
        removal_form_frame = Frame(bike_rem_frame, bg='#ffe16b',width=950, height=600)
        removal_form_frame.place(x=470, y=200)
 
        txt = "BIKE REMOVAL"
        heading = Label(bike_rem_frame, text=txt, font=('yu gothic ui', 25, "bold"), bg="#d4d4ff",
                                    fg='black',
                                    bd=10,
                                    relief=FLAT)
        heading.place(x=300, y=30, width=300, height=30)
       
        bikeid_label = ttk.Label(removal_form_frame, text="Bike ID")
        bikeid_entry = ttk.Entry(removal_form_frame)
        bikeid_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        bikeid_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
 
        def remove_bike():
            bike_id = bikeid_entry.get()
            if bike_id:
                try:
                    # Execute the SQL query to delete the bike with the specified ID
                    cursor.execute("DELETE FROM bikes WHERE bike_id=?", (bike_id,))
                    conn.commit()
                    bikeid_entry.delete(0, 'end')
                    # Optionally, show a confirmation message
                    messagebox.showinfo("Bike Removed", f"Bike with ID {bike_id} has been removed.")
                except sqlite3.Error as e:
                    # Handle any potential database errors
                    messagebox.showerror("Error", "An error occurred while removing the bike.")
            else:
                messagebox.showerror("Error", "Please enter a valid Bike ID.")
 
        submit_button = ttk.Button(removal_form_frame, text="Remove Bike", command=remove_bike)
        submit_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
 
    remove_bikes_button = tk.Button(track_add_remove_frame, text="Remove Bikes", command=bike_removal)
    remove_bikes_button.grid(column=1,row=0)
    track_bikes_button = tk.Button(track_add_remove_frame, text="Track Bikes", command= lambda: tracking_functionality(operator_window))
    track_bikes_button.grid(column=2,row=0)
 
   
 
 
# ---------------------------------------------------------------------------------------------------------------------------
# -------------------------------------####### Charging Functionality ########-----------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

    def charge_action(bike_id):
        cursor.execute("SELECT is_charged FROM bikes WHERE bike_id = ?", (bike_id,))
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            # The bike is already charged
            messagebox.showinfo("No Charging Needed", f"Bike {bike_id} is already charged.")
        else:
            # The bike is not charged, proceed with the charging
            cursor.execute("UPDATE bikes SET is_available = 0, is_charged = 0 WHERE bike_id = ?", (bike_id,))
            conn.commit()
            charge_button.config(state=tk.DISABLED)
            
            # Simulate a 5-second charging delay
            time.sleep(5)
            
            # Enable is_available and is_charged in the bikes table
            cursor.execute("UPDATE bikes SET is_available = 1, is_charged = 1 WHERE bike_id = ?", (bike_id,))
            conn.commit()
            charge_button.config(state=tk.NORMAL)
            
            # Show a message confirming the bike is charged and available
            messagebox.showinfo("Bike Charged", f"Bike {bike_id} is now charged and available.")

    # Function to handle the "Charge" button click
    '''def charge_action(bike_id):
        # Disable is_available and is_charged in the bikes table
        cursor.execute("UPDATE bikes SET is_available = 0, is_charged = 0 WHERE bike_id = ?", (bike_id,))
        conn.commit()
        charge_button.config(state=tk.DISABLED)
        # Simulate a 5-second charging delay
        time.sleep(5)
 
        # Enable is_available and is_charged in the bikes table
        cursor.execute("UPDATE bikes SET is_available = 1, is_charged = 1 WHERE bike_id = ?", (bike_id,))
        conn.commit()
        charge_button.config(state=tk.NORMAL)
        # Show a message confirming the bike is charged and available
        messagebox.showinfo("Bike Charged", f"Bike {bike_id} is now charged and available.")
        # messagebox.showinfo("Charge Bike", f"Charge the bike with ID: {bike_id}")'''
 
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------####### Repair Functionality ########-----------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------
    def repair_action(bike_id):
        cursor.execute("SELECT is_servicing FROM bikes WHERE bike_id = ?", (bike_id,))
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            # The bike is already in servicing state
            messagebox.showinfo("No Repair Needed", f"Bike {bike_id} is already under servicing.")
        else:
            # The bike is not in servicing state, proceed with the repair
            cursor.execute("UPDATE bikes SET is_servicing = 1, is_available = 0 WHERE bike_id = ?", (bike_id,))
            conn.commit()
            repair_button.config(state=tk.DISABLED)
            
            # Simulate a 5-second charging delay
            time.sleep(5)
            
            # Enable is_available and is_charged in the bikes table
            cursor.execute("UPDATE bikes SET is_servicing = 0, is_available = 1 WHERE bike_id = ?", (bike_id,))
            conn.commit()
            repair_button.config(state=tk.NORMAL)
            
            # Show a message confirming the bike is charged and available
            messagebox.showinfo("Bike Charged", f"Bike {bike_id} is now charged and available.")

    # Function to handle the "Repair" button click
    '''def repair_action(bike_id):
        cursor.execute("UPDATE bikes SET is_servicing = 1, is_available = 0 WHERE bike_id = ?", (bike_id,))
        conn.commit()
        repair_button.config(state=tk.DISABLED)
        # Simulate a 5-second charging delay
        time.sleep(5)
        # Enable is_available and is_charged in the bikes table
        cursor.execute("UPDATE bikes SET is_servicing = 0, is_available = 1 WHERE bike_id = ?", (bike_id,))
        conn.commit()
        repair_button.config(state=tk.NORMAL)
        # Show a message confirming the bike is charged and available
        messagebox.showinfo("Bike Charged", f"Bike {bike_id} is now charged and available.")'''
        # messagebox.showinfo("Repair Bike", f"Repair the bike with ID: {bike_id}")
    # Fetch bike information from the database
    cursor.execute("SELECT * FROM BIKES")
    bike_data = cursor.fetchall()
    print("bikes data fetched")
    print()
    print("Out of For Loop")
    print(bike_data)
 
    titles_frame = Frame(actual_bike_data_frame)
    titles_frame.pack()
    '''
    name_title_label = tk.Label(titles_frame, text="Name")
    name_title_label.pack(side=tk.LEFT)
 
    type_title_label = tk.Label(titles_frame, text="Type")
    type_title_label.pack(side=tk.LEFT)
 
    model_title_label = tk.Label(titles_frame, text="Model", )
    model_title_label.pack(side=tk.LEFT)'''
    labels = ["Name", "Type", "Model", "Charge","Repair","Pickup"]
    for label in labels:
        tk.Label(titles_frame, text=label, padx=10).pack(side=tk.LEFT)
 
    # Create and display rows for each bike
    for bike in bike_data:
        print("Inside For")
        bike_id,bike_type, name, model, location, isavail, isservice, ischarged = bike
        print(f"bike_id: {bike_id}, name: {name}, bike_type: {bike_type}, model: {model}, location: {location}")
 
        row_frame = tk.Frame(actual_bike_data_frame)
        row_frame.pack()
 
        name_label = tk.Label(row_frame, text=f"{name}")
        name_label.pack(side=tk.LEFT)
 
        type_label = tk.Label(row_frame, text=f"{bike_type}")
        type_label.pack(side=tk.LEFT)
 
        model_label = tk.Label(row_frame, text=f"{model}")
        model_label.pack(side=tk.LEFT)
 
        charge_button = tk.Button(row_frame, text="Charge", command=lambda bike_id=bike_id: charge_action(bike_id))
        charge_button.pack(side=tk.LEFT)
 
        # ---------------------------------------------------------------------------------------------------------------------------
        # ---------------------------------------####### Repair Functionality ########-----------------------------------------------
        # ---------------------------------------------------------------------------------------------------------------------------
 
        # Function to handle the "Repair" button click
        def repair_action(bike_id):
            cursor.execute("UPDATE bikes SET is_servicing = 1, is_available = 0 WHERE bike_id = ?", (bike_id,))
            conn.commit()
            repair_button.config(state=tk.DISABLED)
            # Simulate a 5-second charging delay
            time.sleep(5)
            # Enable is_available and is_charged in the bikes table
            cursor.execute("UPDATE bikes SET is_servicing = 0, is_available = 1 WHERE bike_id = ?", (bike_id,))
            conn.commit()
            repair_button.config(state=tk.NORMAL)
            # Show a message confirming the bike is charged and available
            messagebox.showinfo("Bike Charged", f"Bike {bike_id} is now charged and available.")
            # messagebox.showinfo("Repair Bike", f"Repair the bike with ID: {bike_id}")
 
 
        repair_button = tk.Button(row_frame, text="Repair", command=lambda bike_id=bike_id: repair_action(bike_id))
        repair_button.pack(side=tk.LEFT)
 
        # ---------------------------------------------------------------------------------------------------------------------------
        # ---------------------------------------####### Pickup Functionality ########-----------------------------------------------
        # ---------------------------------------------------------------------------------------------------------------------------
 
        # Function to handle the "Pick Up" button click
        def move_bikes(bike_id):
            # Create a new window for moving bikes
            move_window = tk.Toplevel(root)
            move_window.title("Move Bike")
 
            # Create a Combobox for selecting the new location
            location_label = tk.Label(move_window, text="Select new location:")
            location_label.pack()
 
            new_location_var = tk.StringVar()
            location_combo = ttk.Combobox(move_window, textvariable=new_location_var, values=['Glasgow University', 'City Centre', 'Scotstounhill', 'Partick', 'Rutherglen'])
            location_combo.pack()
 
            # Function to update the location in the database
            def update_location(bike_id):
                selected_location = new_location_var.get()
                if selected_location:
                    selected_bike_id =  bike_id
 
                    # Check if the bike is available and not in servicing
                    cursor.execute("SELECT is_available, is_servicing FROM BIKES WHERE BIKE_ID = ?", (selected_bike_id,))
                    result = cursor.fetchone()
                    if result and result[0] == 1 and result[1] == 0:
                        cursor.execute("UPDATE BIKES SET BIKE_LOCATION = ? WHERE BIKE_ID = ?", (selected_location, selected_bike_id))
                        time.sleep(5)
                        messagebox.showinfo("Success",f"The bike is moved to {selected_location}")
                        conn.commit()
                        move_window.destroy()  # Close the move window
                    else:
                        # Notify the user that the bike is not available for moving
                        messagebox.showerror("Unavailable","The bike is not available for moving.")
                        # error_label = tk.Label(move_window, text="The bike is not available for moving.")
                        # error_label.pack()
 
            # Create a button to execute the location update
            update_button = tk.Button(move_window, text="Move Bike", command=lambda: update_location(bike_id))
            update_button.pack()
 
        pickup_button = tk.Button(row_frame, text="Move Bike", command=lambda bike_id=bike_id: move_bikes(bike_id))
        pickup_button.pack(side=tk.LEFT)
 
    # Configure the canvas to update scroll region
    actual_bike_data_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# import tkinter as tk
# from tkinter import ttk
# from tkinter import *
# import sqlite3
# from tkinter import messagebox
# import random
# import time
# from PIL import ImageTk
# from PIL import Image

# # Connect to the SQLite database
# conn = sqlite3.connect('Database.db')
# with conn:
#     cursor=conn.cursor()

# def generate_bike_id():
#     cursor.execute("SELECT MAX(BIKE_ID) FROM BIKES")
#     max_id = cursor.fetchone()[0]
#     return max_id + 1 if max_id else 1


# # ---------------------------------------------------------------------------------------------------------------------------
# # ---------------------------------------####### Tracking Functionality ########---------------------------------------------
# # ---------------------------------------------------------------------------------------------------------------------------
# def tracking_functionality(operator_window):
#     # Initialize the main window
#     window = tk.Toplevel(operator_window)
#     window.title("Bike Tracking")
#     window.geometry('1166x718')

#     # Create a dropdown menu to select bike locations
#     location_label = tk.Label(window, text="Select Location:")
#     location_label.pack()
#     location_var = tk.StringVar()
#     location_var.set("Select Location")
#     location_dropdown = tk.OptionMenu(window, location_var, *get_locations())
#     location_dropdown.pack()

#     # Create a function to update the bike list when a location is selected
#     def update_bike_list(*args):
#         selected_location = location_var.get()
#         print(selected_location)
#         bikes = get_bikes_at_location(selected_location)
#         update_bike_display(bikes)

#     location_var.trace("w", update_bike_list)

#     # Create labels for bike details
#     labels_frame = tk.Frame(window)
#     labels_frame.pack()
#     labels = ["Bike ID", "Type", "Name", "Model", "Available for Rent", "Is Servicing Needed", "Is Bike Charged"]
#     for label in labels:
#         tk.Label(labels_frame, text=label, padx=10).pack(side=tk.LEFT) 

#     # Create a function to update the bike details display
#     def update_bike_display(bikes):
#         print(len(bikes))
#         for widget in bike_display_frame.winfo_children():
#             widget.destroy()

#         for bike in bikes:
#             print(len(bike))
#             bike_id, bike_type, bike_name, bike_model, location, available, servicing, charged = bike
#             row_frame = tk.Frame(bike_display_frame)
#             row_frame.pack()
#             tk.Label(row_frame, text=bike_id, padx=10).pack(side=tk.LEFT)
#             tk.Label(row_frame, text=bike_type, padx=10).pack(side=tk.LEFT)
#             tk.Label(row_frame, text=bike_name, padx=10).pack(side=tk.LEFT)
#             tk.Label(row_frame, text=bike_model, padx=10).pack(side=tk.LEFT)
#             tk.Label(row_frame, text=available, padx=10).pack(side=tk.LEFT)
#             tk.Label(row_frame, text=servicing, padx=10).pack(side=tk.LEFT)
#             tk.Label(row_frame, text=charged, padx=10).pack(side=tk.LEFT)

#     # Create a frame to display bike details
#     bike_display_frame = tk.Frame(window)
#     bike_display_frame.pack()


# def get_locations():
#     # Connect to the SQLite database
#     conn = sqlite3.connect("Database.db")
#     cursor = conn.cursor()

#     # Fetch unique bike locations from the database
#     cursor.execute("SELECT DISTINCT BIKE_LOCATION FROM BIKES")
#     locations = [row[0] for row in cursor.fetchall()]
#     return locations

# def get_bikes_at_location(location):
#     # Connect to the SQLite database
#     conn = sqlite3.connect("Database.db")
#     cursor = conn.cursor()

#     # Fetch bike details for a specific location
#     cursor.execute("SELECT * FROM BIKES WHERE BIKE_LOCATION=?", (location,))
#     bikes = cursor.fetchall()
#     return bikes

# def open_operator_window(root):
#     # Create a new window for the operator
#     operator_window = Toplevel(root)
#     operator_window.title("Operator Dashboard")
#     operator_window.geometry('1166x718')
#     operator_window.resizable(0,0)
#     operator_window.state('zoomed')

#     bg_frame = Image.open('images/background3.png')
#     photo = ImageTk.PhotoImage(bg_frame)
#     bg_panel = Label(operator_window, image=photo)
#     bg_panel.image = photo
#     bg_panel.pack(fill='both', expand='yes')

#     # ====== Login Frame =========================
    
#     operator_window_frame = Frame(operator_window, bg='#d4d4ff', width=950, height=600)
#     operator_window_frame.place(x=470, y=200)
    
#     # Welcome Label
#     welcome_label = Label(operator_window_frame, text="Welcome Operator",width=20,fg="blue",font=("bold", 20))
#     welcome_label.place(x=150,y=53)
    
#     track_add_remove_frame = Frame(operator_window_frame, bg='#d4d4ff', width=800, height=500)
#     track_add_remove_frame.place(x=150, y=100)

#     bike_data_frame = Frame(operator_window_frame, width=800, height=500)
#     bike_data_frame.place(x=50, y=200)
#     # ////////////////////////////// Bike Registration functionality ///////////////////////////////////////////////

#     def bike_registration():
#         # Labels and Entry fields
#         isavailable_var = BooleanVar()
#         isservicing_var = BooleanVar()
#         ischarged_var = BooleanVar()

#         bike_reg_frame = Frame(operator_window, bg='#d4d4ff', width=950, height=600)
#         bike_reg_frame.place(x=470, y=200)

#         form_frame = Frame(bike_reg_frame, bg='#ffe16b',width=950, height=600)
#         form_frame.place(x=200,y=60)

#         txt = "BIKE REGISTRATION"
#         heading = Label(bike_reg_frame, text=txt, font=('yu gothic ui', 25, "bold"), bg="#d4d4ff",
#                                     fg='black',
#                                     bd=10,
#                                     relief=FLAT)
#         heading.place(x=300, y=30, width=300, height=30)

#         bike_id_label = ttk.Label(form_frame, text="Bike ID")
#         bike_id = ttk.Entry(form_frame, state='readonly')
#         bike_id.insert(0, generate_bike_id())

#         bike_type_label = ttk.Label(form_frame, text="Bike Type")
#         bike_type_combo = ttk.Combobox(form_frame, values=['electric bike', 'electric car', 'electric motorbike', 'electric scooter'])

#         bike_name_label = ttk.Label(form_frame, text="Bike Name")
#         bike_name_entry = ttk.Entry(form_frame)

#         bike_model_label = ttk.Label(form_frame, text="Bike Model")
#         bike_model_entry = ttk.Entry(form_frame)

#         bike_location_label = ttk.Label(form_frame, text="Bike Location")
#         bike_location_combo = ttk.Combobox(form_frame, values=['Glasgow University', 'City Centre', 'Scotstounhill', 'Partick', 'Rutherglen'])


#         bike_isavailable_check = ttk.Checkbutton(form_frame, text="Available",variable=isavailable_var)
#         bike_isservicing_check = ttk.Checkbutton(form_frame, text="In Service", variable=isservicing_var)
#         bike_ischarged_check = ttk.Checkbutton(form_frame, text="Charged",variable=ischarged_var)

#         bike_id_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
#         bike_id.grid(row=0, column=1, padx=5, pady=5, sticky='w')
#         bike_type_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
#         bike_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
#         bike_name_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
#         bike_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
#         bike_model_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
#         bike_model_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
#         bike_location_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
#         bike_location_combo.grid(row=4, column=1, padx=5, pady=5, sticky='w')
#         bike_isavailable_check.grid(row=5, column=0, padx=5, pady=5, sticky='w')
#         bike_isservicing_check.grid(row=6, column=0, padx=5, pady=5, sticky='w')
#         bike_ischarged_check.grid(row=7, column=0, padx=5, pady=5, sticky='w')

#         # Function to insert data into the database
#         def insert_data():
#             #bike_id = generate_bike_id()
#             cursor.execute('''
#                 INSERT INTO BIKES ( BIKE_TYPE, BIKE_NAME, BIKE_MODEL, BIKE_LOCATION, is_available, is_servicing, is_charged)
#                 VALUES (?, ?, ?, ?, ?, ?, ?)
#             ''', ( bike_type_combo.get(), bike_name_entry.get(), bike_model_entry.get(), bike_location_combo.get(), isavailable_var.get(), isservicing_var.get(), ischarged_var.get()))
#             conn.commit()
#             reset_form()
#             bike_id.delete(0, 'end')

#         # Function to reset the form
#         def reset_form():
#             bike_type_combo.delete(0, 'end')
#             bike_name_entry.delete(0, 'end')
#             bike_model_entry.delete(0, 'end')
#             bike_location_combo.delete(0, 'end')
#             '''bike_isavailable_check.deselect()
#             bike_isservicing_check.deselect()
#             bike_ischarged_check.deselect()'''

#         submit_button = ttk.Button(form_frame, text="Submit", command=insert_data)
#         submit_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

    
#     # Buttons to Add Remove and track Bikes 
#     add_bikes_button = tk.Button(track_add_remove_frame, text="Add Bikes", command=bike_registration)
#     add_bikes_button.grid(column=0,row=0)

#     # //////////////////////// Bike Removal Functionality /////////////////////////////////////////////


#     def bike_removal():
#         bike_rem_frame = Frame(operator_window, bg='#d4d4ff', width=950, height=600)
#         bike_rem_frame.place(x=470, y=200)

#         removal_form_frame = Frame(bike_rem_frame, bg='#ffe16b',width=950, height=600)
#         removal_form_frame.place(x=200,y=53)

#         txt = "BIKE REMOVAL"
#         heading = Label(bike_rem_frame, text=txt, font=('yu gothic ui', 25, "bold"), bg="#d4d4ff",
#                                     fg='black',
#                                     bd=10,
#                                     relief=FLAT)
#         heading.place(x=300, y=30, width=300, height=30)
        

#         bikeid_label = ttk.Label(removal_form_frame, text="Bike ID")
#         bikeid_entry = ttk.Entry(removal_form_frame)
#         bikeid_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
#         bikeid_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

#         def remove_bike():
#             bike_id = bikeid_entry.get()
#             if bike_id:
#                 try:
#                     # Execute the SQL query to delete the bike with the specified ID
#                     cursor.execute("DELETE FROM bikes WHERE bike_id=?", (bike_id,))
#                     conn.commit()
#                     bikeid_entry.delete(0, 'end')
#                     # Optionally, show a confirmation message
#                     messagebox.showinfo("Bike Removed", f"Bike with ID {bike_id} has been removed.")
#                 except sqlite3.Error as e:
#                     # Handle any potential database errors
#                     messagebox.showerror("Error", "An error occurred while removing the bike.")
#             else:
#                 messagebox.showerror("Error", "Please enter a valid Bike ID.")

#         submit_button = ttk.Button(removal_form_frame, text="Remove Bike", command=remove_bike)
#         submit_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

#     remove_bikes_button = tk.Button(track_add_remove_frame, text="Remove Bikes", command=bike_removal)
#     remove_bikes_button.grid(column=1,row=0)
#     track_bikes_button = tk.Button(track_add_remove_frame, text="Track Bikes", command=tracking_functionality(operator_window))
#     track_bikes_button.grid(column=2,row=0)

    


# # ---------------------------------------------------------------------------------------------------------------------------
# # -------------------------------------####### Charging Functionality ########-----------------------------------------------
# # ---------------------------------------------------------------------------------------------------------------------------

#     # Function to handle the "Charge" button click
#     def charge_action(bike_id):
#         # Disable is_available and is_charged in the bikes table
#         cursor.execute("UPDATE bikes SET is_available = 0, is_charged = 0 WHERE bike_id = ?", (bike_id,))
#         conn.commit()
#         charge_button.config(state=tk.DISABLED)
#         # Simulate a 5-second charging delay
#         time.sleep(5)

#         # Enable is_available and is_charged in the bikes table
#         cursor.execute("UPDATE bikes SET is_available = 1, is_charged = 1 WHERE bike_id = ?", (bike_id,))
#         conn.commit()
#         charge_button.config(state=tk.NORMAL)
#         # Show a message confirming the bike is charged and available
#         messagebox.showinfo("Bike Charged", f"Bike {bike_id} is now charged and available.")
#         # messagebox.showinfo("Charge Bike", f"Charge the bike with ID: {bike_id}")

# # ---------------------------------------------------------------------------------------------------------------------------
# # ---------------------------------------####### Repair Functionality ########-----------------------------------------------
# # ---------------------------------------------------------------------------------------------------------------------------

#     # Function to handle the "Repair" button click
#     def repair_action(bike_id):
#         cursor.execute("UPDATE bikes SET is_servicing = 1, is_available = 0 WHERE bike_id = ?", (bike_id,))
#         conn.commit()
#         repair_button.config(state=tk.DISABLED)
#         # Simulate a 5-second charging delay
#         time.sleep(5)
#         # Enable is_available and is_charged in the bikes table
#         cursor.execute("UPDATE bikes SET is_servicing = 0, is_available = 1 WHERE bike_id = ?", (bike_id,))
#         conn.commit()
#         repair_button.config(state=tk.NORMAL)
#         # Show a message confirming the bike is charged and available
#         messagebox.showinfo("Bike Charged", f"Bike {bike_id} is now charged and available.")
#         # messagebox.showinfo("Repair Bike", f"Repair the bike with ID: {bike_id}")
#     # Fetch bike information from the database
#     cursor.execute("SELECT * FROM BIKES")
#     bike_data = cursor.fetchall()
#     print("bikes data fetched")
#     print()
#     print("Out of For Loop")
#     print(bike_data)

#     titles_frame = Frame(bike_data_frame)
#     titles_frame.pack()
#     '''
#     name_title_label = tk.Label(titles_frame, text="Name")
#     name_title_label.pack(side=tk.LEFT)

#     type_title_label = tk.Label(titles_frame, text="Type")
#     type_title_label.pack(side=tk.LEFT)

#     model_title_label = tk.Label(titles_frame, text="Model", )
#     model_title_label.pack(side=tk.LEFT)'''
#     labels = ["Name", "Type", "Model", "Charge","Repair","Pickup"]
#     for label in labels:
#         tk.Label(titles_frame, text=label, padx=10).pack(side=tk.LEFT) 

#     # Create and display rows for each bike
#     for bike in bike_data:
#         print("Inside For")
#         bike_id,bike_type, name, model, location, isavail, isservice, ischarged = bike
#         print(f"bike_id: {bike_id}, name: {name}, bike_type: {bike_type}, model: {model}, location: {location}")

#         row_frame = tk.Frame(bike_data_frame)
#         row_frame.pack()

#         name_label = tk.Label(row_frame, text=f"{name}")
#         name_label.pack(side=tk.LEFT)

#         type_label = tk.Label(row_frame, text=f"{bike_type}")
#         type_label.pack(side=tk.LEFT)

#         model_label = tk.Label(row_frame, text=f"{model}")
#         model_label.pack(side=tk.LEFT)

#         charge_button = tk.Button(row_frame, text="Charge", command=lambda bike_id=bike_id: charge_action(bike_id))
#         charge_button.pack(side=tk.LEFT)

#         # ---------------------------------------------------------------------------------------------------------------------------
#         # ---------------------------------------####### Repair Functionality ########-----------------------------------------------
#         # ---------------------------------------------------------------------------------------------------------------------------

#         # Function to handle the "Repair" button click
#         def repair_action(bike_id):
#             cursor.execute("UPDATE bikes SET is_servicing = 1, is_available = 0 WHERE bike_id = ?", (bike_id,))
#             conn.commit()
#             repair_button.config(state=tk.DISABLED)
#             # Simulate a 5-second charging delay
#             time.sleep(5)
#             # Enable is_available and is_charged in the bikes table
#             cursor.execute("UPDATE bikes SET is_servicing = 0, is_available = 1 WHERE bike_id = ?", (bike_id,))
#             conn.commit()
#             repair_button.config(state=tk.NORMAL)
#             # Show a message confirming the bike is charged and available
#             messagebox.showinfo("Bike Charged", f"Bike {bike_id} is now charged and available.")
#             # messagebox.showinfo("Repair Bike", f"Repair the bike with ID: {bike_id}")


#         repair_button = tk.Button(row_frame, text="Repair", command=lambda bike_id=bike_id: repair_action(bike_id))
#         repair_button.pack(side=tk.LEFT)

#         # ---------------------------------------------------------------------------------------------------------------------------
#         # ---------------------------------------####### Pickup Functionality ########-----------------------------------------------
#         # ---------------------------------------------------------------------------------------------------------------------------

#         # Function to handle the "Pick Up" button click
#         def pickup_action(bike_id):
#             cursor.execute("UPDATE bikes SET is_available = 0 WHERE bike_id = ?", (bike_id,))
#             conn.commit()
#             pickup_button.config(state=tk.DISABLED)
#             # Simulate a 5-second charging delay
#             time.sleep(5)
#             # Enable is_available and is_charged in the bikes table
#             cursor.execute("UPDATE bikes SET is_available = 1 WHERE bike_id = ?", (bike_id,))
#             conn.commit()
#             pickup_button.config(state=tk.NORMAL)
#             # Show a message confirming the bike is charged and available
#             messagebox.showinfo("Pick Up Bike", f"Pick up the bike with ID: {bike_id}")

#         pickup_button = tk.Button(row_frame, text="Pick Up", command=lambda bike_id=bike_id: pickup_action(bike_id))
#         pickup_button.pack(side=tk.LEFT)






