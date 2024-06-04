import datetime
from tkinter import *
from tkinter import messagebox
import smtplib
from datetime import *
import pandas as pd
import random

current_date = datetime.today().replace(microsecond=0)
email = "bookmybus.info@gmail.com"
mail_password = "yxfw xcmz othz yzdo"

#Login Page
### funcitons
def new_user():
    user = username_entry.get()
    pw = password_entry.get()
    content = pd.read_csv("userdata.csv")
    x = content.username.to_list()
    if user in x:
        messagebox.showerror(title="Error", message="Username Already Exists. "
                                                    "\nPlease choose a new username.")
    else:
        isok = messagebox.askokcancel(title="Confirm Details",
                                      message=f"These are the details entered \nUsername:{user} \nPassword:{pw}")
        if isok:
            data = {
                'username': [user],
                'password': [pw]
            }

            df = pd.DataFrame(data)
            df.to_csv('userdata.csv', mode='a', index=False, header=False)
            messagebox.showinfo(title="BookMyBus", message="User Added Successfully")
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            login_page.destroy()

def existing_user():
    user = username_entry.get()
    pw = password_entry.get()
    content = pd.read_csv("userdata.csv")
    x = content.username.to_list()
    y = content.password.to_list()
    if user in x and pw in y:
        messagebox.showinfo(title="BookMyBus",message="Login Successful")
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        login_page.destroy()
    else:
        messagebox.showerror(title="BookMyBus", message="Wrong Username or Password."
                                                    "\nPlease enter correct details.")
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')


### Window
login_page = Tk()
login_page.title("Book My Bus")
login_page.config(padx=50,pady=50)

### Logo
img = PhotoImage(file="logo.png")
canvas = Canvas(width=225, height=225, highlightthickness=0)
canvas.create_image(115,115, image= img)
canvas.grid(row=0,column=1)

### Label
username = Label(text="Username:")
username.grid(column=0,row=1)
password = Label(text="Password:")
password.grid(column=0,row=2)

### Buttons
login = Button(text="Login",width=15,command=existing_user)
login.grid(column=2, row=1, columnspan=2)
new_user = Button(text="New User",width=15,command=new_user)
new_user.grid(column=2,row=2,columnspan=2)

### Text-Inputs
username_entry = Entry(width=22)
username_entry.grid(row=1,column=1)
username_entry.focus()
password_entry = Entry(width=22)
password_entry.grid(row=2,column=1)


login_page.mainloop()


# User Panel
### Window
userpage = Tk()
userpage.title("Book My Bus")
userpage.config(padx=50,pady=50)

### Logo
img = PhotoImage(file="logo.png")
canvas = Canvas(width=225, height=225, highlightthickness=0)
canvas.create_image(115,115, image= img)
canvas.grid(row=0,column=1)

### Buttons
book_ticket = Button(text="Book Ticket",width=10,command=userpage.destroy)
book_ticket.grid(row=1,column=1)

cancel_ticket = Button(text="Cancel Ticket",width=10)
cancel_ticket.grid(row=2,column=1)

check_pnr = Button(text="PNR Status",width=10)
check_pnr.grid(row=3,column=1)

userpage.mainloop()


# Book Ticket
### functions
def book():
    if len(name_entry.get()) == 0 or len(mail_entry.get()) == 0 or len(age_entry.get()) == 0:
        messagebox.showerror(title="Error",message="Fields are empty. "
                                                   "\nPlease fill all the details before saving.")
    else:
        isok = messagebox.askokcancel(title="Book Ticket Information",
                                      message=f"These are the details entered\n"
                                              f"Name: {name_entry.get()} \n"
                                              f"Age: {age_entry.get()}\n"
                                              f"From: {clicked.get()}\n"
                                              f"To: {clicked1.get()}\n"
                                              f"Departure: {date_entry.get()}\n"
                                              f"E-Mail: {mail_entry.get()}\n"                                               
                                              f"Do you want to continue?")
        if isok:
            pnr = "BMB" + ''.join(random.sample([str(x) for x in range(10)], 4))
            with open("email_template.txt") as bm:
                booking_mail = bm.read()
            with smtplib.SMTP("smtp.gmail.com") as connection:
                name = name_entry.get().title()
                formatted_email = booking_mail.replace('[NAME]', name).replace('[AGE]', str(age_entry.get())).replace(
                    '[SOURCE]', clicked.get()).replace(
                    '[DESTINATION]', clicked1.get()).replace('[DATE]', str(date_entry.get())).replace('[PNR]', pnr)
                connection.starttls()
                connection.login(user=email, password=mail_password)
                connection.sendmail(from_addr=email,
                                    to_addrs=mail_entry.get(),
                                    msg=f"Subject:Bus Booking Confirmation - BookMyBus \n\n"
                                        f"Dear {name},\n\nYour Booking was successfully booked at BookMyBus on {current_date}\n\n"
                                        f"{formatted_email}"
                                    )
            content = pd.read_csv("passenger.csv")
            data = {
                'pnr': [pnr],
                'name': [name],
                'age': [age_entry.get()],
                'source': [clicked.get()],
                'destination': [clicked1.get()],
                'travel_data': [date_entry.get()],
                'email': [mail_entry.get()]
            }
            # Make data frame of above data
            df = pd.DataFrame(data)
            # append data frame to CSV file
            df.to_csv('passenger.csv', mode='a', index=False, header=False)
            messagebox.showinfo(title="Ticket Information", message=f"PNR: {pnr}\n"
                                                                    f"Name: {name_entry.get()}")
            booking_page.destroy()



### Window
booking_page = Tk()
booking_page.title("Book My Bus")
booking_page.config(padx=50,pady=50)

### Logo
img = PhotoImage(file="logo.png")
canvas = Canvas(width=225, height=225, highlightthickness=0)
canvas.create_image(115,115, image= img)
canvas.grid(row=0,column=1)

### Labels
book_name = Label(text="Name:")
book_name.grid(column=0,row=1)
book_age = Label(text="Age:")
book_age.grid(column=0,row=2)
book_source = Label(text="From:")
book_source.grid(column=0,row=3)
book_destination = Label(text="To:")
book_destination.grid(column=0,row=4)
book_date = Label(text="Date:")
book_date.grid(column=0,row=5)
book_mail = Label(text="E-Mail:")
book_mail.grid(column=0,row=6)

### Text-Inputs
name_entry = Entry(width=24)
name_entry.grid(row=1,column=1)
name_entry.focus()

age_entry = Entry(width=24)
age_entry.grid(row=2,column=1)


source = [
    "Uttar Pradesh",
    "Rajasthan",
    "Maharashtra",
    "Delhi",
    "Ladakh",
    "Himachal Pradesh",
    "Uttarakhand",
    "Jammu & Kashmir",
    "West Bengal",
    "Sikkim"
]


# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set( "Delhi" )

# Create Dropdown menu
drop = OptionMenu( booking_page , clicked , *source)
drop.grid(row=3,column=1)
drop.config(width=17)

####################

destination = [
    "Uttar Pradesh",
    "Rajasthan",
    "Maharashtra",
    "Delhi",
    "Ladakh",
    "Himachal Pradesh",
    "Uttarakhand",
    "Jammu & Kashmir",
    "West Bengal",
    "Sikkim"
]

# datatype of menu text
clicked1 = StringVar()

# initial menu text
clicked1.set( "Ladakh" )

# Create Dropdown menu
drop = OptionMenu( booking_page , clicked1 , *destination)
drop.grid(row=4,column=1)
drop.config(width=17)

date_entry = Entry(width=24)
date_entry.grid(row=5,column=1)
date_entry.insert(END, "DD-MM-YYYY")

mail_entry = Entry(width=24)
mail_entry.grid(row=6,column=1)


### Buttons
confirm = Button(text="Book Ticket",width=20,command=book)
confirm.grid(column=1, row=7, columnspan=2)


booking_page.mainloop()
