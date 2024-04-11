import os

os.environ['TK_SILENCE_DEPRECATION'] = '1'

from tkinter import *
from PIL import ImageTk, Image
import sqlite3
# import cv2
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.pyplot as plt
from datetime import time
from tkinter import ttk
import numpy as np
from PIL import Image
from tkinter import messagebox

class manager() :

    def __init__(self, window) :
        
        '''
        Inital the window to show.



        '''
        # Create the manager page.  
        self.window = Toplevel(window)
        self.window.geometry('2000x1500')
        self.window.title('Manager Page')
        self.window.configure(bg='#d4d4ff')

        # bg_frame = Image.open('images/Bike.png')
        # photo = ImageTk.PhotoImage(bg_frame)
        # bg_panel = Label(self.window, image=photo)
        # bg_panel.image = photo
        # bg_panel.pack(fill='both', expand='yes')

        # The manager enter the time and find vehicle' status during the period.
        self.label1 = Label(self.window, text='Enter the period you want to find : ')
        self.label1.place(x=550, y=70)

        time_choices = [  
            time(8, 0),   # 08:00 AM
            time(10, 0),  
            time(12, 0),  # 12:00 PM
            time(14, 0),
            time(16, 0),
            time(18, 0),  # 06:00 PM
            time(20, 0),
            time(22, 0),
            time(0, 0)   
        ]
        
        self.timebox1 = ttk.Combobox(self.window, values=time_choices, state='readonly', font=('Helvetica', 12))
        self.timebox1.place(x=780, y=70, width=80, height=25)

        self.label2 = Label(self.window, text=' - ')
        self.label2.place(x=880, y=70)       

        self.timebox2 = ttk.Combobox(self.window, values=time_choices, state='readonly', font=('Helvetica', 12))
        self.timebox2.place(x=900, y=70, width=80, height=25)

        self.button1 = Button(self.window, text='Find', command=self.show_vehicle)
        self.button1.place(x=1000, y=70, width=50, height=25)

        self.button2 = Button(self.window, text='Clear', command=self.clear)
        self.button2.place(x=1050, y=70, width=50, height=25)

        # self.button3 = Button(self.window, text='Show location', command=self.heatmap)
        # self.button3.place(x=1100, y=70, width=100, height=25)

        self.button4 = Button(self.window, text='Show figures', command=self.show_figure)
        self.button4.place(x=1100, y=70, width=100, height=25)


        self.conn = sqlite3.connect('Database.db')

        with self.conn:

            self.cursor = self.conn.cursor()

        self.visualize_status()
        self.visualize_usage_date()
        self.visualize_type_usage()
        self.visualize_revenue()

        self.figure1 = PhotoImage(file='images/Vehicle_status_chart.png')
        # self.figure1 = self.figure1.subsample(2, 2)
        self.img1 = Label(self.window, image=self.figure1)
        self.img1.place(x=100, y=100)

        self.figure2 = PhotoImage(file='images/Vehicle_date_chart.png')
        # self.figure2 = self.figure2.subsample(2, 2)
        self.img2 = Label(self.window, image=self.figure2)
        self.img2.place(x=700, y=100)

        self.figure3 = PhotoImage(file='images/Vehicle_type_chart.png')
        # self.figure3 = self.figure3.subsample(2, 2)
        self.img3 = Label(self.window, image=self.figure3)
        self.img3.place(x=100, y=520)

        self.figure4 = PhotoImage(file='images/Revenue_chart.png')
        # self.figure4 = self.figure4.subsample(2, 2)
        self.img4 = Label(self.window, image=self.figure4)
        self.img4.place(x=700, y=520)

        # self.label3 = Label(text='Enter the operator you want to find : ')
        # self.label3.place(x=50, y=100)

        # self.idbox = Entry(text='')
        # self.idbox.place(x=280, y=100, width=100)

        # self.button4 = Button(text='Add')
        # self.button4.place(x=400, y=100, width=50, height=25)

        # self.button5 = Button(text='Revoke')
        # self.button5.place(x=450, y =100, width=60, height=25)
        self.window.mainloop()
        
    def visualize_status(self) :

        self.cursor.execute('''SELECT is_available, is_servicing, is_charged FROM BIKES''')

        result = self.cursor.fetchall()

        available_count = 0
        servicing_count = 0
        charged_count = 0
        number = []

        for i in result :

            if i[0] :

                available_count += 1

            elif i[1] :

                servicing_count += 1

            else :

                charged_count += 1
        
        categories = ['Available', 'Servicing', 'Charging']
        number.append(available_count)
        number.append(servicing_count)
        number.append(charged_count)

        plt.figure(figsize=(5, 4))
        plt.bar(categories, number, color=['green', 'red', 'blue'])

        # Add title and label
        plt.xlabel('Bike Status')
        plt.ylabel('Number of bikes')
        plt.title('Vehicle Status')

        # Show number and label
        for i, count in enumerate(number):
            plt.text(i, count, str(count), ha='center', va='bottom')

        # Save image
        plt.savefig('images/Vehicle_status_chart.png')
        # plt.show()

    def visualize_usage_date(self) :

        self.cursor.execute('''SELECT substr(alloted_time, 6, 5) FROM user_util''')

        result = self.cursor.fetchall()

        date = [i[0] for i in result]

        date_dic = {}

        for i in date :

            if i in date_dic :

                date_dic[i] += 1
            
            else :

                date_dic[i] = 1

        date_dic = dict(sorted(date_dic.items()))
        categories = list(date_dic.keys())
        number = list(date_dic.values())

        plt.figure(figsize=(5, 4))
        plt.plot(categories, number, linestyle='-', color='g', markersize=8, linewidth=1)

        plt.ylim(0, 5)
        # Add title and label
        plt.xlabel('Date')
        plt.ylabel('Number of bikes')
        plt.title('Vehicle usage over period')

        # Show number and label
        for i, count in enumerate(number):
            plt.text(i, count+0.2, str(count), ha='center', va='bottom')

        # Save image
        plt.savefig('images/Vehicle_date_chart.png')
        # plt.show()

    def visualize_type_usage(self) :

        self.cursor.execute('''SELECT bike_id FROM user_util ''')

        result = self.cursor.fetchall()
    
        bike_type = []

        for i in result :

            self.cursor.execute('''SELECT BIKE_TYPE FROM BIKES WHERE BIKE_ID = ?''', (i))
            bike_type.append(str(self.cursor.fetchall()[0][0]))

        type_dic = {}

        for i in bike_type :

            if i in type_dic :

                type_dic[i] += 1

            else :

                type_dic[i] = 1

        categories = list(type_dic.keys())
        number = list(type_dic.values())

        plt.figure(figsize=(5, 4))
        plt.bar(categories, number, color=['blue', 'red', 'green'])

        plt.ylim(0, 5)
        # Add title and label
        plt.xlabel('Vehicle Type')
        plt.ylabel('Number of bikes')
        plt.title('Vehicle usage of all types')

        # Show number and label
        for i, count in enumerate(number):
            plt.text(i, count, str(count), ha='center', va='bottom')

        # Save image
        plt.savefig('images/Vehicle_type_chart.png')
        # plt.show()

    def visualize_revenue(self) :

        self.cursor.execute('''SELECT payment_id, amount, payment_status FROM payment WHERE payment_status = 1''')

        result = self.cursor.fetchall()

        date_payment = []

        for i in result :

            self.cursor.execute('''SELECT substr(return_time, 6, 5) FROM user_util WHERE payment_id = ? and payment_status = 1''', (i[0], ))

            for x in self.cursor.fetchall():
                if x != "":
                    date_payment.append(str(x[0]))

        amount = [i[1] for i in result]
        
        revenue_dic = {}

        for d, a in zip(date_payment, amount) :

            if d in revenue_dic :

                revenue_dic[d] += a
            
            else :

                revenue_dic[d] = a

        revenue_dic = dict(sorted(revenue_dic.items()))
        categories = list(revenue_dic.keys())
        number = list(revenue_dic.values())

        plt.figure(figsize=(5, 4))
        plt.plot(categories, number, linestyle='-', color='r', markersize=8, linewidth=1)

        # Add title and label
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Revenue over period')

        # Show number and label
        for i, count in enumerate(number):
            plt.text(i, count+5, str(count), ha='center', va='bottom')

        # Save image
        plt.savefig('images/Revenue_chart.png')
        # plt.show()


    def show_vehicle(self) :

        '''
        The function is for showing vehicles' status during the defined time period.



        '''
        self.clear()

        self.cursor.execute("SELECT id, bike_id, payment_status, substr(alloted_time, 12, 8), substr(return_time, 12, 8) FROM user_util")
        
        results = self.cursor.fetchall()

        self.listbox = Listbox(self.window)
        self.listbox.place(x=580, y=200, width=700, height=400)
        
        start = self.timebox1.get()
        end = self.timebox2.get()

        if start == '' or end == '' :
            
            messagebox.showwarning("Warning", "Please choose the start time and the end time!")

        elif start > end :

            messagebox.showwarning("Warning", "You can not choose the end time early than the start time!")

        results = [i for i in results if i[3] >= start and i[4] <= end]

        bike_status = []

        for i in results :

            self.cursor.execute("SELECT is_available, is_servicing, is_charged FROM BIKES WHERE BIKE_ID = ?", (int(i[1]), ))
            bike_status.append(self.cursor.fetchall()[0])
        
        status = []

        for i in bike_status :

            if i == (0, 1, 0) :

                status.append('is_servicing')
            
            elif i == (1, 0, 0) :

                status.append('is_available')

            else :

                status.append('is_charged')


        self.label3 = Label(self.window, text='Bike id')
        self.label4 = Label(self.window, text='User id')
        self.label5 = Label(self.window, text='Bike status')
        self.label6 = Label(self.window, text='Payment status')

        self.label3.place(x=580, y=170)  
        self.label4.place(x=730, y=170)   
        self.label5.place(x=880, y=170) 
        self.label6.place(x=1030, y=170)

        # self.data_list = []

        for i, vehicle_data in enumerate(results) :

            self.listbox.insert(END, str(vehicle_data[1]) + ' '*40 + str(vehicle_data[0]) + ' '*46 + str(status[i]) + ' '*46  + str(vehicle_data[2]) + '\n')
        #     self.label7 = Label(self.window, text=vehicle_data[1])
        #     self.label8 = Label(self.window, text=vehicle_data[0])
        #     self.label9 = Label(self.window, text=status[i])
        #     self.label0 = Label(self.window, text=vehicle_data[2])    

        #     self.data_list.append(self.label7)
        #     self.data_list.append(self.label8)
        #     self.data_list.append(self.label9)
        #     self.data_list.append(self.label0)

        #     self.label7.place(x=50, y=120 + (i + 1) * 20)  
        #     self.label8.place(x=150, y=120 + (i + 1) * 20)   
        #     self.label9.place(x=250, y=120 + (i + 1) * 20) 
        #     self.label0.place(x=350, y=120 + (i + 1) * 20)

    def clear(self) :

        if hasattr(self, 'label3') :

            self.label3.destroy()

        if hasattr(self, 'label4') :

            self.label4.destroy()

        if hasattr(self, 'label5') :
            
            self.label5.destroy()

        if hasattr(self, 'label6') :
        
            self.label6.destroy()
        
        if hasattr(self, 'photobox') :

            self.photobox.destroy()
        
        if hasattr(self, 'img1') :

            self.img1.destroy()
        
        if hasattr(self, 'img2') :

            self.img2.destroy()

        if hasattr(self, 'img3') :
            
            self.img3.destroy()

        if hasattr(self, 'img4') :

            self.img4.destroy()
        
        if hasattr(self, 'listbox') :

            self.listbox.destroy()

    # def authority_change(self, add=True) :

    #     '''
    #     The function is for changing of authority.

    #     '''
    #     # Connect to the database.
    #     # conn = sqlite3.connect('Database.db')

    #     # with conn:

    #     #     cursor = conn.cursor()
    #     #     cursor.execute()  
    #     if add :

    # def show_heatmap(self, img_path) :

    #     # Read the image
    #     image = cv2.imread(img_path)  
    #     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #     img_width, img_height = gray_image.shape

    #     np.random.seed(417)

    #     # Connect to the database.
    #     self.cursor.execute("SELECT BIKE_LOCATION FROM BIKES")

    #     results = self.cursor.fetchall()
    #     results = [str(i[0]) for i in results]

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
    #     plt.savefig("heatmap_on_image.png", bbox_inches="tight", pad_inches=0, dpi=300)
    #     # plt.show()

    # def heatmap(self) :

    #     '''
    #     The function is for bicycles' visualization.

    #     '''
    #     self.clear()
    #     self.show_heatmap("/Users/fan/Desktop/Group project/glasgow map.jpg")
    #     self.photo = PhotoImage(file='heatmap_on_image.png')
    #     self.photo = self.photo.subsample(2, 2)
    #     self.photobox = Label(self.window, image=self.photo)
    #     self.photobox.place(x=130, y=130, width=1200, height=600)

    def show_figure(self) :
        
        self.clear()

        self.visualize_status()
        self.visualize_usage_date()
        self.visualize_type_usage()
        self.visualize_revenue()

        self.figure1 = PhotoImage(file='images/Vehicle_status_chart.png')
        # self.figure1 = self.figure1.subsample(2, 2)
        self.img1 = Label(self.window, image=self.figure1)
        self.img1.place(x=100, y=100)

        self.figure2 = PhotoImage(file='images/Vehicle_date_chart.png')
        # self.figure2 = self.figure2.subsample(2, 2)
        self.img2 = Label(self.window, image=self.figure2)
        self.img2.place(x=700, y=100)

        self.figure3 = PhotoImage(file='images/Vehicle_type_chart.png')
        # self.figure3 = self.figure3.subsample(2, 2)
        self.img3 = Label(self.window, image=self.figure3)
        self.img3.place(x=100, y=520)

        self.figure4 = PhotoImage(file='images/Revenue_chart.png')
        # self.figure4 = self.figure4.subsample(2, 2)
        self.img4 = Label(self.window, image=self.figure4)
        self.img4.place(x=700, y=520)


# window = Tk()
# manager(window)

