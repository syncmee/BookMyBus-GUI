from tkinter import *
from tkinter import messagebox
import smtplib
from tkinter import ttk
from datetime import datetime
import pandas as pd
import random
from tkcalendar import DateEntry
from twilio.rest import Client



icon_path = "./icon.ico"
current_date = datetime.today().replace(microsecond=0)
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day

email = "bookmybus.info@gmail.com"
mail_password = "yxfw xcmz othz yzdo"

#Login Page
### Functions
def new_user():
    user = username_entry.get()
    pw = password_entry.get()
    content = pd.read_csv("userdata.csv")
    x = content.username.to_list()
    if len(user) == 0 or len(pw) == 0:
        messagebox.showerror(title="Error", message="Fields are empty. "
                                                    "\nPlease fill all the details before saving.")
    else:
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
        messagebox.showinfo(title="BookMyBus", message="Login Successful")
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        login_page.destroy()

    else:
        messagebox.showerror(title="BookMyBus", message="Wrong Username or Password."
                                                        "\nPlease enter correct details.")
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')

### Login Window

login_page = Tk()
login_page.title("Book My Bus")
login_page.wm_iconbitmap(icon_path)
login_page.config(padx=50, pady=50)

### Logo
img = PhotoImage(file="logo2.png")
canvas = Canvas(width=500, height=278, highlightthickness=0)
canvas.create_image(250, 139, image=img)
canvas.grid(row=0, column=1)

### Label
username = Label(text="Username:")
username.grid(column=0, row=1)
password = Label(text="Password:")
password.grid(column=0, row=2)

### Buttons
login = Button(text="Login", width=15, command=existing_user)
login.grid(column=2, row=1, columnspan=2)
new_user = Button(text="New User", width=15, command=new_user)
new_user.grid(column=2, row=2, columnspan=2)

### Text-Inputs
username_entry = Entry(width=22)
username_entry.grid(row=1, column=1)
username_entry.focus()
password_entry = Entry(width=22)
password_entry.grid(row=2, column=1)

login_page.mainloop()

# User Panel
def user_panel():
    ### Functions
    def open_booking_page():
        booking_page = Toplevel(userpage)
        book_ticket_page(booking_page)

    def open_cancel_page():
        cancel_page = Toplevel(userpage)
        cancel_ticket_page(cancel_page)

    def open_check_pnr_page():
        check_pnr_page = Toplevel(userpage)
        check_status_page(check_pnr_page)

    ### User Panel Window
    userpage = Tk()
    userpage.wm_iconbitmap(icon_path)
    userpage.title("User Panel -BookMyBus")
    userpage.config(padx=50, pady=50)

    ### Logo
    img = PhotoImage(file="logo.png")
    canvas = Canvas(userpage, width=225, height=225, highlightthickness=0)
    canvas.create_image(115, 115, image=img)
    canvas.grid(row=0, column=1)

    ### Buttons
    book_ticket = Button(userpage, text="Book Ticket", width=10, command=open_booking_page)
    book_ticket.grid(row=1, column=1)

    cancel_ticket = Button(userpage, text="Cancel Ticket", width=10, command=open_cancel_page)
    cancel_ticket.grid(row=2, column=1)

    check_pnr = Button(userpage, text="PNR Status", width=10, command=open_check_pnr_page)
    check_pnr.grid(row=3, column=1)
    userpage.mainloop()

# Book Ticket
def book_ticket_page(booking_page):
    ### Functions
    def book():
        get_selected_date()
        if len(name_entry.get()) == 0 or len(mail_entry.get()) == 0 or len(age_entry.get()) == 0:
            messagebox.showerror(title="Error", message="Fields are empty. "
                                                        "\nPlease fill all the details before saving.")
        else:
            isok = messagebox.askokcancel(title="Book Ticket Information",
                                          message=f"These are the details entered\n"
                                                  f"Name: {name_entry.get().title()} \n"
                                                  f"Age: {age_entry.get()}\n"
                                                  f"From: {clicked.get()}\n"
                                                  f"To: {clicked1.get()}\n"
                                                  f"Departure: {selected_date}\n"
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
                        '[DESTINATION]', clicked1.get()).replace('[DATE]', str(selected_date)).replace('[PNR]', pnr)
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
                    'travel_date': [selected_date],
                    'email': [mail_entry.get()]
                }
                # Make data frame of above data
                df = pd.DataFrame(data)
                # append data frame to CSV file
                df.to_csv('passenger.csv', mode='a', index=False, header=False)
                account_sid = 'ACb03858ea1c7e8285e0ad7c598465cde4'
                auth_token = '0141fa636f585d8b31a25d7c19eb1825'
                client = Client(account_sid, auth_token)
                client.messages.create(
                    from_='+19403267061',
                    body=f"Thank you for booking your bus journey with us. Here are your booking details:\n\n"
                         f"Booking PNR : {pnr}\n"
                         f"Passenger Name: {name_entry.get().title()}\n"
                         f"Age: {age_entry.get()}\n"
                         f"Source: {clicked.get()}\n"
                         f"Destination: {clicked1.get()}\n"
                         f"Travel Date: {selected_date}\n\n"
                         f"Please ensure to carry a copy of this email and a valid ID proof while boarding the bus.\n\n"
                         f"We wish you a pleasant journey!\n\n"
                         f"Best regards,\n"
                         "BookMyBus Team",
                    to='+918810459229'
                )
                messagebox.showinfo(title="Ticket Information", message=f"PNR: {pnr}\n"
                                                                        f"Name: {name_entry.get()}")
                booking_page.destroy()



    def get_selected_date():
        global selected_date
        selected_date = date_entry.get()

    ### Booking Window
    booking_page.wm_iconbitmap(icon_path)
    booking_page.title("Book Ticket -BookMyBus")
    booking_page.config(padx=50, pady=50)

    ### Logo
    img = PhotoImage(file="logo2.png")
    canvas = Canvas(booking_page, width=500, height=278, highlightthickness=0)
    canvas.create_image(250, 139, image=img)
    canvas.grid(row=0, column=1)

    ### Labels
    book_name = Label(booking_page, text="Name:")
    book_name.grid(column=0, row=1)
    book_age = Label(booking_page, text="Age:")
    book_age.grid(column=0, row=2)
    book_source = Label(booking_page, text="From:")
    book_source.grid(column=0, row=3)
    book_destination = Label(booking_page, text="To:")
    book_destination.grid(column=0, row=4)
    book_date = Label(booking_page, text="Date:")
    book_date.grid(column=0, row=5)
    book_mail = Label(booking_page, text="E-Mail:")
    book_mail.grid(column=0, row=6)

    ### Text-Inputs
    name_entry = Entry(booking_page, width=24)
    name_entry.grid(row=1, column=1)
    name_entry.focus()

    age_entry = Entry(booking_page, width=24)
    age_entry.grid(row=2, column=1)

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
    clicked = StringVar()
    clicked.set("Delhi")
    drop = OptionMenu(booking_page, clicked, *source)
    drop.grid(row=3, column=1)
    drop.config(width=17)

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
    clicked1 = StringVar()
    clicked1.set("Ladakh")
    drop1 = OptionMenu(booking_page, clicked1, *destination)
    drop1.grid(row=4, column=1)
    drop1.config(width=17)

    date_entry = DateEntry(booking_page, width=20, year=current_year, month=current_month, day=current_day, background='green', foreground='red', borderwidth=2)
    date_entry.grid(row=5, column=1)
    # date_button = Button(booking_page, text="Confirm Date", command=get_selected_date)
    # date_button.grid(row=5, column=2)

    mail_entry = Entry(booking_page, width=24)
    mail_entry.grid(row=6, column=1)

    ### Buttons
    confirm = Button(booking_page, text="Book Ticket", width=20, command=book)
    confirm.grid(column=1, row=7)
    confirm.config(width=20)

    booking_page.mainloop()

# Cancel Ticket
def cancel_ticket_page(cancel_page):
    ### Functions
    def cancel():
        cancel_name = cancel_name_entry.get().title()
        cancel_pnr = pnr_entry.get()
        passenger_list = pd.read_csv("passenger.csv")
        names = passenger_list.name.to_list()
        pnrs = passenger_list.pnr.to_list()
        if cancel_name in names and cancel_pnr in pnrs:
            if len(cancel_pnr) == 0 or len(cancel_name) == 0:
                messagebox.showerror(title="Error", message="Fields are empty. "
                                                            "\nPlease fill all the details before saving.")
            else:
                isok = messagebox.askokcancel(title="Cancel Ticket Information",
                                              message=f"These are the details entered\n"
                                                      f"PNR: {cancel_pnr}\n"
                                                      f"Name: {cancel_name}")
                if isok:
                    filtered_data = passenger_list[passenger_list['pnr'] == cancel_pnr]
                    user_email = filtered_data["email"].tolist()[0]
                    user_name = filtered_data["name"].tolist()[0]
                    age = filtered_data["age"].tolist()[0]
                    source = filtered_data["source"].tolist()[0]
                    destination = filtered_data["destination"].tolist()[0]
                    travel_date = filtered_data["travel_date"].tolist()[0]
                    df = passenger_list.drop(passenger_list[passenger_list['pnr'] == cancel_pnr].index)
                    df.to_csv("passenger.csv", mode="w", index=False)
                    messagebox.showinfo(title="BookMyBus", message="Ticket is cancelled")

                    with open("cancel_ticket.txt") as bm:
                        cancel_mail = bm.read()
                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        name = user_name.title()
                        formatted_email = cancel_mail.replace('[NAME]', name).replace('[AGE]',
                                                                                       str(age)).replace(
                            '[SOURCE]', source).replace(
                            '[DESTINATION]', destination).replace('[DATE]', travel_date).replace('[PNR]', cancel_pnr)
                        connection.starttls()
                        connection.login(user=email, password=mail_password)
                        connection.sendmail(from_addr=email,
                                            to_addrs=user_email,
                                            msg=f"Subject:Bus Booking Cancellation - BookMyBus \n\n"
                                                f"Dear {name},\n\nThis email confirms the cancellation of your bus ticket booking with BookMyBus "
                                                f"(PNR: {cancel_pnr}) on {current_date}\n\n"
                                                f"{formatted_email}")
                    cancel_page.destroy()
        else:
            messagebox.showerror(title="Error", message="Ticket Not Found.\n"
                                                        "Please Check again")


    ### Cancel Window
    cancel_page.title("Cancel Ticket -BookMyBus")
    cancel_page.wm_iconbitmap(icon_path)
    cancel_page.config(padx=50, pady=50)

    ### Logo
    cancel_page.img = PhotoImage(file="logo2.png")  # Save a reference to the image
    canvas = Canvas(cancel_page, width=500, height=278, highlightthickness=0)
    canvas.create_image(250, 139, image=cancel_page.img)
    canvas.grid(row=0, column=1)

    ### Label
    pnr = Label(cancel_page, text="PNR Number:")
    pnr.grid(column=0, row=1)
    name = Label(cancel_page, text="Name:")
    name.grid(column=0, row=2)

    ### Buttons
    cancel = Button(cancel_page, text="Cancel", width=15, command=cancel)
    cancel.grid(column=2, row=1, columnspan=2)

    ### Text-Inputs
    pnr_entry = Entry(cancel_page, width=22)
    pnr_entry.grid(row=1, column=1)
    pnr_entry.focus()
    pnr_entry.insert(END, "BMB")
    cancel_name_entry = Entry(cancel_page, width=22)
    cancel_name_entry.grid(row=2, column=1)

# Check Status
def check_status_page(check_pnr_page):
    ### Functions
    def check_status():
        pnr_check = status_pnr.get()
        status_name = status_name_entry.get().title()
        passenger_list = pd.read_csv("passenger.csv")
        names = passenger_list.name.to_list()
        pnr_list = passenger_list.pnr.to_list()
        if status_name in names and pnr_check in pnr_list:
            if len(pnr_check) == 0 or len(status_name) == 0:
                messagebox.showerror(title="Error", message="Fields are empty. "
                                                            "\nPlease fill all the details before saving.")
            else:
                filtered_data = passenger_list[passenger_list['pnr'] == pnr_check]
                user_email = filtered_data["email"].tolist()[0]
                user_name = filtered_data["name"].tolist()[0]
                age = filtered_data["age"].tolist()[0]
                source = filtered_data["source"].tolist()[0]
                destination = filtered_data["destination"].tolist()[0]
                travel_date = filtered_data["travel_date"].tolist()[0]
                messagebox.showinfo(title="Ticket Information", message=f"Ticket Found\n"
                                                                        f"Name: {user_name}\n"
                                                                        f"Age: {age}\n"
                                                                        f"From: {source}\n"
                                                                        f"To: {destination}\n"
                                                                        f"Departure: {travel_date}\n"
                                                                        f"Mail: {user_email}")
                check_pnr_page.destroy()
        else:
            messagebox.showerror(title="Error", message="Ticket Not Found.\n"
                                                        "Please enter correct information")

    ### Status Window
    check_pnr_page.title("Check Status -BookMyBus")
    check_pnr_page.wm_iconbitmap(icon_path)
    check_pnr_page.config(padx=50, pady=50)

    ### Logo
    check_pnr_page.img = PhotoImage(file="logo2.png")  # Save a reference to the image
    canvas = Canvas(check_pnr_page, width=500, height=278, highlightthickness=0)
    canvas.create_image(250, 139, image=check_pnr_page.img)
    canvas.grid(row=0, column=1)

    ### Label
    pnr = Label(check_pnr_page, text="PNR Number:")
    pnr.grid(column=0, row=1)
    name = Label(check_pnr_page, text="Name:")
    name.grid(column=0, row=2)

    ### Buttons
    check = Button(check_pnr_page, text="Check", width=15, command=check_status)
    check.grid(column=2, row=1, columnspan=2)

    ### Text-Inputs
    status_pnr = Entry(check_pnr_page, width=22)
    status_pnr.grid(row=1, column=1)
    status_pnr.focus()
    status_pnr.insert(END, "BMB")
    status_name_entry = Entry(check_pnr_page, width=22)
    status_name_entry.grid(row=2, column=1)

user_panel()
