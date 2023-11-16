import mysql.connector
import random
from kivy.core.text import LabelBase
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.toast import toast
import random
import string
import mysql.connector
from datetime import datetime

host = "sql12.freesqldatabase.com"
user = "sql12662532"
password = "viDRIhzYSq"
database = "sql12662532"

db = mysql.connector.connect(
    host = "sql12.freesqldatabase.com",
    user = "sql12662532",
    password = "viDRIhzYSq",
    database = "sql12662532",
    )

cursor = db.cursor()
Window.size = (360, 600)

class DropDownHandler:
    def show_custom_dropdown(self, caller, items):
        menu_items = self.create_menu_items(items, caller)
        self.dropdown_menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.dropdown_menu.open()

    def create_menu_items(self, options, caller):
        return [{"viewclass": "OneLineListItem",
                 "text": option,
                 "on_release": lambda x=option: self.menu_callback(x, caller)} for option in options]

    def menu_callback(self, text_item, caller):
        caller.text = text_item
        self.dropdown_menu.dismiss()
        caller.focus = False

class MyApp(MDApp):
    dropdown_handler = DropDownHandler()

    def build(self):
        self.screen_manager = MDScreenManager()
        self.screen_manager.add_widget(Builder.load_file("Screens\LoginScreen\signup.kv"))
        self.screen_manager.add_widget(Builder.load_file("Screens\LoginScreen\login.kv"))
        self.screen_manager.add_widget(Builder.load_file("Screens\HomeScreen\homescreen.kv"))
        self.screen_manager.add_widget(Builder.load_file("Screens\HomeScreen\screenreport.kv"))
        self.screen_manager.add_widget(Builder.load_file("Screens\LoginScreen\main.kv"))
        self.screen_manager.add_widget(Builder.load_file("Screens\HomeScreen\homescreen_admin.kv"))

        return self.screen_manager

    def generate_user_id(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(10))

    def get_db_connection(self):
        return mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12662532",
            password="viDRIhzYSq",
            database="sql12662532"
        )

    def convert_date_format(self, date_string):
        try:
            date_object = datetime.strptime(date_string, '%m/%d/%Y')
            return date_object.strftime('%Y-%m-%d')
        except ValueError as e:
            print(f"Error converting date: {e}")
            return None

    def on_signup(self, name, email, password, birthdate):
        user_id = self.generate_user_id()
        formatted_birthdate = self.convert_date_format(birthdate)
        if formatted_birthdate is None:
            toast("Invalid date format provided. Please use MM/DD/YYYY.")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO UserProfiles (ProfileID, UserName, Email, Birthdate, UserPassword, CreditScore) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, name, email, formatted_birthdate, password, 100)
            )
            conn.commit()
            toast("Signup successful! Please log in.")
            self.screen_manager.current = 'login'
        except mysql.connector.Error as err:
            print("Error: ", err)
            toast("An error occurred during signup.")
        finally:
            cursor.close()
            conn.close()

    def on_login(self, email, password):
        conn = self.get_db_connection()
        cursor = conn.cursor(buffered=True)
        try:
            cursor.execute("SELECT * FROM UserProfiles WHERE Email = %s AND UserPassword = %s", (email, password))
            user = cursor.fetchone()
            if user:
                # Store user information
                self.current_user = {
                    "user_id": user[0],  # Assuming ProfileID is the first column
                    "name": user[1],     # Adjust indices based on your table structure
                    "email": user[2],
                    # ... Include other relevant details ...
                }
                self.screen_manager.current = 'homescreen'
                toast(f"Login successful! Welcome, {self.current_user['name']}.")
            else:
                toast("User not found or incorrect password!")
        except mysql.connector.Error as err:
            print("Error: ", err)
            toast("An error occurred during login.")
        finally:
            cursor.close()
            conn.close()
    
    # Reporting functions
    def show_incident_type_dropdown(self, caller):
        incident_types = ["Medical Emergency", "Natural Disaster", "Security Threat", "Others"]
        self.dropdown_handler.show_custom_dropdown(caller, incident_types)

    def show_urgency_dropdown(self, caller):
        urgency_levels = ["Low", "Medium", "High"]
        self.dropdown_handler.show_custom_dropdown(caller, urgency_levels)

    def submit_data(self):
        # Assuming 'screenreport' is the name of the screen where your 'title' widget resides
        screen_report = self.root.get_screen('screenreport')

       
        reportInitial = random.randint(10, 999)
        reportID = str(reportInitial)
        title = screen_report.ids.title.text
        incident_type = screen_report.ids.choice1.text
        image_path = screen_report.ids.imagepath.text
        details = screen_report.ids.details.text
        urgency = screen_report.ids.urgency.text
        status = "pending"
        date_created = datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            "INSERT INTO report (reportID, title, checklist, image_path, details, urgency, status, dateCreated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (reportID, title, incident_type, image_path, details, urgency, status, date_created)
        )
        db.commit()

        # Clear the text fields
        screen_report.ids.title.text = ""
        screen_report.ids.choice1.text = ""
        screen_report.ids.imagepath.text = ""
        screen_report.ids.details.text = ""
        screen_report.ids.urgency.text = ""


    def show_success_dialog(self):
        self.dialog = MDDialog(
            text="Successfully Submitted!",
            radius=[20, 20, 20, 20],
            size_hint=(0.7, None),
            height=dp(200)
        )
        self.dialog.ids.text.text_color = (0, 0, 0, 1)
        self.dialog.ids.text.font_name = "BPoppins"
        self.dialog.ids.text.font_size = "20sp"
        self.dialog.ids.text.halign = "center"
        self.dialog.ids.text.valign = "center"
        self.dialog.open()
        Clock.schedule_once(self.dismiss_dialog, 2)

    def dismiss_dialog(self, dt):
        self.dialog.dismiss()

if __name__ == "__main__":
    LabelBase.register(name="MPoppins", fn_regular="Screens\\Assets\\Poppins\\Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="Screens\\Assets\\Poppins\\Poppins-SemiBold.ttf")

    MyApp().run()
