import customtkinter
import os
from PIL import Image
import sqlite3 
import pyqrcode
import png
from pyqrcode import QRCode
import smtplib
import ssl
from email.message import EmailMessage
from customtkinter import *
import folium
from geopy.geocoders import Nominatim
from geopy import distance


conn = sqlite3.connect('customer2.db')
c = conn.cursor()

 #create table
c.execute("""CREATE TABLE users (
      user_id text PRIMARY KEY,
      no_of_persons INTEGER NOT NULL,
      no_of_adults INTEGER NOT NULL,
      no_of_children INTEGER NOT NULL,
      nationality text NOT NULL,
      monument_name text NOT NULL,
      phno INTEGER NOT NULL,
      email text NOT NULL,
      id_type text NOT NULL,
      unique_no INTEGER NOT NULL
   
 )""")

c.execute("""CREATE TABLE monuments5 (
      monument_id TEXT PRIMARY KEY,
      monument_name TEXT NOT NULL,
      monument_location TEXT NOT NULL
 )""")

# c.execute("""CREATE TABLE tickets5 (
#      ticket_id TEXT PRIMARY KEY,
#      monument_id TEXT,
#      ticket_price INTEGER NOT NULL,
#      status TEXT NOT NULL,
#      FOREIGN KEY(monument_id) REFERENCES monuments5(monument_id)
#  )""")



# c.execute("""CREATE TABLE transs(
#     transaction_id text PRIMARY KEY,
#     user_id text NOT NULL,
#     ticket_id text NOT NULL,
#     amount INTEGER NOT NULL
#     FOREIGN KEY(user_id) REFERENCES users(user_id),
#     FOREIGN KEY(ticket_id) REFERENCES tickets5(ticket_id)
#  )""")

# c.execute("""CREATE TABLE trans5(
#     transaction_id text PRIMARY KEY,
#     user_id text NOT NULL,
#     amount INTEGER NOT NULL
# )""")


mon = [
    ('M101','TAJ MAHAL','Agra'),
    ('M102','RED FORT','Delhi'),
    ('M103','Meenakshi Temple','Madurai'),
    ('M104','Golden Temple','Amritsar'),
    ('M105','Gateway of India','Mumbai')
]
#c.executemany("INSERT INTO monuments5 VALUES (?,?,?)",mon)

#print("executed....")

c.execute("SELECT * FROM monuments5")
items = c.fetchall()
print(len(items))
for item in items:
    print(item)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ticket Booker")
        self.geometry("750x750")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        # self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "TicketEase.png")), size=(500, 250))
        # self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                  dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                  dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                      dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        #LOGO
        # self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example", image=self.logo_image,
        #                                                      compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        # self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Monument",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="User Details",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        # self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
        #                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        #                                               image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        # self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="submit",command=self.frame_2_button_event)
        self.home_frame_button_1.grid(row=2, column=0, padx=20, pady=10)
        # self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        # self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        # self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        # self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")

        
        #Combo box
        self.combobox_1 = customtkinter.CTkComboBox(self.home_frame,values=["Golden Temple", "Taj Mahal", "Red Fort","Meenakshi Temple","Gate Way Of India"])
        self.combobox_1.grid(row=1,column=0,padx=20,pady=20)

    
        # self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.second_frame.grid_columnconfigure(1,weight=1)


        self.name_label=customtkinter.CTkLabel(self.second_frame, text="Enter number of people :")
        self.name_label.grid(row=0,column=0,padx=10,pady=10)
        self.adult_label=customtkinter.CTkLabel(self.second_frame, text="Enter number of adults :")
        self.adult_label.grid(row=1,column=0,padx=10,pady=10)
        self.children_label=customtkinter.CTkLabel(self.second_frame, text="Number children under  5 years age :")
        self.children_label.grid(row=2,column=0,padx=10,pady=10)
        self.nationality_label=customtkinter.CTkLabel(self.second_frame, text="Nationality :")
        self.nationality_label.grid(row=3,column=0,padx=10,pady=10)
        self.ph_label=customtkinter.CTkLabel(self.second_frame, text="Phone number :")
        self.ph_label.grid(row=4,column=0,padx=10,pady=10)
        self.email_label=customtkinter.CTkLabel(self.second_frame, text="Email :")
        self.email_label.grid(row=5,column=0,padx=10,pady=10)
        self.type_label=customtkinter.CTkLabel(self.second_frame, text="Select type of ID :")
        self.type_label.grid(row=6,column=0,padx=10,pady=10)
        self.id_label=customtkinter.CTkLabel(self.second_frame, text="Id number :")
        self.id_label.grid(row=7,column=0,padx=10,pady=10)
        self.location_label=customtkinter.CTkLabel(self.second_frame, text="Enter your location :")
        self.location_label.grid(row=8,column=0,padx=10,pady=10)


        self.name_entry = customtkinter.CTkEntry(self.second_frame)
        self.name_entry.grid(row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.adult_entry = customtkinter.CTkEntry(self.second_frame)
        self.adult_entry.grid(row=1, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.child_entry = customtkinter.CTkEntry(self.second_frame)
        self.child_entry.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.nation_entry = customtkinter.CTkEntry(self.second_frame)
        self.nation_entry.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.ph_entry = customtkinter.CTkEntry(self.second_frame)
        self.ph_entry.grid(row=4, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.email_entry = customtkinter.CTkEntry(self.second_frame)
        self.email_entry.grid(row=5, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.id_entry = customtkinter.CTkEntry(self.second_frame)
        self.id_entry.grid(row=7, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.location_entry = customtkinter.CTkEntry(self.second_frame)
        self.location_entry.grid(row=8, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.second_frame, dynamic_resizing=False,
                                                        values=["Aadhar","PAN","Passport","Voter ID"])
        self.optionmenu_1.grid(row=6, column=1 , padx=20, pady=(20, 10))


        self.string_input_button = customtkinter.CTkButton(self.second_frame, text="UPI Payment",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=9,column=0,padx=20, pady=40)
        

        
        self.submit_button = customtkinter.CTkButton(self.second_frame, text="Submit",
                                                           command=self.insertUser)
        self.submit_button.grid(row=9,column=1,padx=20, pady=40)
        
        # create third frame
        # self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def open_input_dialog_event(self):
            dialog = customtkinter.CTkInputDialog(text="Enter The UPI transaction ID :", title="Transaction ID")
            print("UPI transaction :", dialog.get_input())
            print("Transaction Successdul.")
            
    def insertUser(self):
            #number = self.name_entry.get()
            noPersons=self.name_entry.get()
            noOfAdults = self.adult_entry.get()
            noOfChildren = self.child_entry.get()
            nationality=self.nation_entry.get()
            monumentName = 4
            phNo = self.ph_entry.get()
            email=self.email_entry.get()
            idType="Aadhar"
            uniqueNo = self.id_entry.get()

            uid = "Uid"+noPersons+noOfChildren
            #print(noPersons, noOfAdults, noOfChildren,nationality, monumentName, phNo, email, idType, uniqueNo)            
            tup=(uid, noPersons, noOfAdults, noOfChildren, nationality, monumentName, phNo, email, idType, uniqueNo)
            tup=[tup]
            
            #c.executemany("INSERT INTO users(user_id, no_of_persons, no_of_adults, no_of_children, nationality, monument_name, phno, email, id_type, unique_no) VALUES (?, ?,?,?,?,?,?,?,?,?)",tup)
    
            #c.execute("SELECT * FROM users")
            #items = c.fetchall()
#
            #for item in items:
            #    print(item)
 
            c.execute("SELECT * FROM users")
            items1 = c.fetchall()
            userId = items1[len(items1)-1][0]
            
            
            monumentId = 4
            ticketPrice = 100
            status = "SUCCESS"
            ticketId = "TId"+userId+(str)(monumentId*3)
            tup=(ticketId, monumentId, ticketPrice, status)
            tup=[tup]
            #c.executemany("INSERT INTO tickets5(ticket_id, monument_id,ticket_price,status) VALUES (?,?,?,?)",tup)
            
            c.execute("SELECT * FROM tickets5")
            items = c.fetchall()
            
            #for item in items:
            #    print(item)
            
            geolocator = Nominatim(user_agent="map_example")
            source_address=self.id_entry.get()
            # Prompt the user to enter the source and destination addresses
            #source_address = input("Enter the source address: ")
            #destination_address = input("Enter the destination address: ")
            destination_address = "Golden Temple"

            # Get the coordinates for the source address
            source_location = geolocator.geocode(source_address)
            source_latitude = source_location.latitude
            source_longitude = source_location.longitude

            # Get the coordinates for the destination address
            destination_location = geolocator.geocode(destination_address)
            destination_latitude = destination_location.latitude
            destination_longitude = destination_location.longitude

            # Create a map object
            m = folium.Map(location=[source_latitude, source_longitude], zoom_start=8)

            # Add markers for the source and destination addresses
            folium.Marker(location=[source_latitude, source_longitude], popup='Source').add_to(m)
            folium.Marker(location=[destination_latitude, destination_longitude], popup='Destination').add_to(m)

            # Calculate the distance between the source and destination
            source_coords = (source_latitude, source_longitude)
            destination_coords = (destination_latitude, destination_longitude)
            distance_km = distance.distance(source_coords, destination_coords).kilometers
            print("Distance between the source and destination:", distance_km, "km")

            # Draw a line between the source and destination
            folium.PolyLine(locations=[source_coords, destination_coords], color='red').add_to(m)

            # Save the map as an HTML file
            map_file = 'map.html'
            m.save(map_file)

            # Generate a link that opens the map location on Google Maps
            google_maps_link = f"https://www.google.com/maps/dir/?api=1&origin={source_latitude},{source_longitude}&destination={destination_latitude},{destination_longitude}"
            #print("Google Maps link:", google_maps_link)
            
            s = "Ticket Id: "+ticketId+"\nUser Id: "+userId+"\nNo of Persons: "+noPersons+"\nNo of Adults: "+noOfAdults

            # Generate QR code
            url = pyqrcode.create(s)

            # Create and save the png file naming "myqr.png"
            url.png('ticket.png', scale = 8)

            # Define email sender and receiver
            email_sender = 'py.team19@gmail.com'
            email_password = 'mieaviarstskhyvl'
            email_receiver = 'aparunpandian@gmail.com'
            #email_receiver = 'jontarg24@gmail.com'

            # Set the subject and body of the email
            subject = 'Ticket Booking Successful !!!'
            body = """
            Congratulations on booking tickets with us.

            Embark on a journey of wonder and awe as you immerse yourself in the rich history and architectural marvels that await you.
            The ticket as a QR code is a attached with this mail.
            
            \nGoogle Map Link: 
            """+ google_maps_link
            """
            HAVE A GREAT AND FUN VISIT....
            """

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            with open('ticket.png', 'rb') as file:
                image_data = file.read()

            # Add the image as an attachment
            em.add_attachment(image_data, maintype='image', subtype='jpg', filename='ticket.png')

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            
            

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        # self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        # if name == "frame_3":
        #     self.third_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    # def frame_3_button_event(self):
    #     self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    conn.commit()
    conn.close()
