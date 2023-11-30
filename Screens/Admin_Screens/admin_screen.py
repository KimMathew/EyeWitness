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
from kivy.uix.image import Image
import string
from datetime import datetime, timedelta
from Screens.Enforcer_Screens.status import StatusScreen  # Import the StatusScreen
from Screens.User_Screens.reportHistory import ReportHistory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy_garden.graph import Graph, MeshLinePlot
from Screens.User_Screens.userInbox import UserInbox
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import time
from kivymd.uix.button import MDIconButton
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.button import MDFlatButton
from database.database import DatabaseManager


# Database initialization
database = DatabaseManager()
db = database.get_my_db()
cursor = db.cursor()

#Displaying Statistics
class StatsLayout(Screen):
    def __init__(self, **kwargs):
        super(StatsLayout, self).__init__(**kwargs)
        Clock.schedule_once(self.initialize_graph)

    def initialize_graph(self, dt):
        # Set up the default graph properties
        # Replace 'graph_id' with the actual id of your Graph widget
        InitialGraph = ['first_graph', 'second_graph', 'third_graph', 'last_graph']

        for graph_name in InitialGraph:
            graph_widget = self.ids[graph_name]
            graph_widget.xlabel = 'Date'
            graph_widget.ylabel = 'Value'
            graph_widget.x_grid = True
            graph_widget.y_grid = True
            graph_widget.x_grid_label = True
            graph_widget.y_grid_label = True
            graph_widget.padding = 5
            graph_widget.xlog = False
            graph_widget.ylog = False
            graph_widget.tick_color = [80/255, 196/255, 242/255, 1]
            graph_widget.border_color = [24/255, 106/255, 232/255, 1]
            graph_widget.label_options = {'color': [0, 0, 0, 1], 'font_name': 'MPoppins'}
            graph_widget.background_color = [1, 1, 1, 1]
            graph_widget.grid_color = [0.6, 0.6, 0.6, 1]


            # Optional: Set default range if you know the expected range of your data
            graph_widget.xmin = 738812  # Adjust these values based on your data
            graph_widget.xmax = 738852
            graph_widget.ymin = 0
            graph_widget.ymax = 15

    def update_graph(self, graph_id, timeframe, incident_type):
        # Fetch data from the database
        data = self.fetch_data_from_db(timeframe)

        # Process the data for graphing
        processed_data = self.process_data(data)

        print(f"Processed Data: {processed_data}")

        # Get the graph widget reference
        graph_widget = self.ids[graph_id]

        # Clear existing plots
        for plot in graph_widget.plots[:]:
            graph_widget.remove_plot(plot)

        # Plot only the specific incident type for each graph
        points = processed_data.get(incident_type, [])
        if points:  # Check if there are points to plot for the specific incident type
            color = {'Medical Emergency': [1, 0, 0, 1],  # Red
                    'Natural Disaster': [0, 1, 0, 1],     # Green
                    'Security Threat': [0, 0, 1, 1], # Blue
                    'Others': [1, 1, 0, 1]}.get(incident_type, [1, 1, 1, 1])  # Default to white

            plot = MeshLinePlot(color=color)
            plot.points = points
            graph_widget.add_plot(plot)
        else:
            print(f"No data to plot for {incident_type}.")

    def fetch_data_from_db(self, timeframe):
        results = []  # Initialize results to an empty list in case of errors
        conn = None
        cursor = None  # Initialize cursor here
        try:
            conn = mysql.connector.connect(
                host="sql12.freesqldatabase.com",
                user="sql12662532",
                passwd="viDRIhzYSq",
                database="sql12662532"
            )
            cursor = conn.cursor()

            # Determine the date range for the query based on the timeframe
            end_date = datetime.today()
            if timeframe == "1 Month":
                start_date = end_date - timedelta(days=30)
            elif timeframe == "3 Months":
                start_date = end_date - timedelta(days=90)
            elif timeframe == "6 Months":
                start_date = end_date - timedelta(days=180)
            elif timeframe == "1 Year":
                start_date = end_date - timedelta(days=365)
            elif timeframe == "All":
                start_date = datetime(2000, 1, 1)  # Fetch all records from an early date
            else:
                start_date = end_date  # For unexpected timeframes, no records will be fetched
            # SQL query to get the date, incident type, and count
            query = (
                "SELECT dateCreated, checklist, COUNT(*) "
                "FROM report "
                "WHERE checklist IN ('Medical Emergency', 'Natural Disaster', 'Security Threat', 'Others') "
                "AND dateCreated BETWEEN %s AND %s "
                "AND status != 'False Report' "
                "GROUP BY dateCreated, checklist "
                "ORDER BY dateCreated, checklist"
            )

            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")

            print(f"{start_date_str} to {end_date_str}")

            cursor.execute(query, (start_date_str, end_date_str))
            results = cursor.fetchall()

            print(f"Data: {results}")

        except mysql.connector.Error as e:
            print(f"Error fetching data from db: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return results

    def process_data(self, data):
        # data is expected to be in the format: [(date, incident_type, count), ...]
        processed_data = {
            "Medical Emergency": [],
            "Natural Disaster": [],
            "Security Threat": [],
            "Others": []
        }

        for date, incident_type, count in data:
            print(f"Original Data: {date}, {incident_type}, {count}")  # Debugging print statement
            # Convert date to a datetime object if it's a string
            if isinstance(date, str):
                try:
                    date = datetime.strptime(date, "%Y-%m-%d").date()
                except ValueError as e:
                    print(f"Date conversion error: {e}")
                    continue
            # Append the tuple (date.toordinal(), count) to the corresponding list
            if incident_type in processed_data:
                processed_data[incident_type].append((date.toordinal(), count))
            else:
                print(f"Incident type '{incident_type}' not in processed_data keys")

        return processed_data

    def first_spinner(self, spinner, text):
        self.update_graph('first_graph', text, 'Medical Emergency')

        end_date = datetime.today()
        if text == "1 Month":
            start_date = end_date - timedelta(days=30)
        elif text == "3 Months":
            start_date = end_date - timedelta(days=90)
        elif text == "6 Months":
            start_date = end_date - timedelta(days=180)
        elif text == "1 Year":
            start_date = end_date - timedelta(days=365)
        elif text == "All":
            # Assuming 'All' means a significantly large range
            start_date = datetime(2000, 1, 1)
        else:
            # Default case if none match
            start_date = end_date

        self.update_graph_range('first_graph', start_date, end_date)

    def second_spinner(self, spinner, text):
        self.update_graph('second_graph', text, 'Natural Disaster')

        end_date = datetime.today()
        if text == "1 Month":
            start_date = end_date - timedelta(days=30)
        elif text == "3 Months":
            start_date = end_date - timedelta(days=90)
        elif text == "6 Months":
            start_date = end_date - timedelta(days=180)
        elif text == "1 Year":
            start_date = end_date - timedelta(days=365)
        elif text == "All":
            # Assuming 'All' means a significantly large range
            start_date = datetime(2000, 1, 1)
        else:
            # Default case if none match
            start_date = end_date

        self.update_graph_range('second_graph', start_date, end_date)

    def third_spinner(self, spinner, text):
        self.update_graph('third_graph', text, 'Security Threat')

        end_date = datetime.today()
        if text == "1 Month":
            start_date = end_date - timedelta(days=30)
        elif text == "3 Months":
            start_date = end_date - timedelta(days=90)
        elif text == "6 Months":
            start_date = end_date - timedelta(days=180)
        elif text == "1 Year":
            start_date = end_date - timedelta(days=365)
        elif text == "All":
            # Assuming 'All' means a significantly large range
            start_date = datetime(2000, 1, 1)
        else:
            # Default case if none match
            start_date = end_date

        self.update_graph_range('third_graph', start_date, end_date)

    def last_spinner(self, spinner, text):
        self.update_graph('last_graph', text, 'Others')

        end_date = datetime.today()
        if text == "1 Month":
            start_date = end_date - timedelta(days=30)
        elif text == "3 Months":
            start_date = end_date - timedelta(days=90)
        elif text == "6 Months":
            start_date = end_date - timedelta(days=180)
        elif text == "1 Year":
            start_date = end_date - timedelta(days=365)
        elif text == "All":
            # Assuming 'All' means a significantly large range
            start_date = datetime(2000, 1, 1)
        else:
            # Default case if none match
            start_date = end_date

        self.update_graph_range('last_graph', start_date, end_date)

    def update_graph_range(self, graph_id, start_date, end_date):
        # Get the graph widget by id
        graph_widget = self.ids[graph_id]

        # Convert dates to ordinal and set as xmin and xmax
        graph_widget.xmin = start_date.toordinal()
        graph_widget.xmax = end_date.toordinal()

# For View Reports of Admin
class CustomTwoLineListItem(TwoLineListItem):
    def __init__(self, primary_font_name="BPoppins", secondary_font_name="MPoppins", primary_font_size=20, secondary_font_size=16, primary_color=[0, 0, 0, 1], secondary_color=[0, 0, 0, 1], **kwargs):
        super().__init__(**kwargs)
        # Override primary label properties
        self.ids._lbl_primary.font_name = primary_font_name
        self.ids._lbl_primary.font_size = primary_font_size 
        self.ids._lbl_primary.color = primary_color

        # Override secondary label properties
        self.ids._lbl_secondary.font_name = secondary_font_name
        self.ids._lbl_secondary.font_size = secondary_font_size
        self.ids._lbl_secondary.color = secondary_color

# Custom content class for the dialog
class DialogContent(BoxLayout):
    pass

class AllReportHistory(Screen):
    user_id = None  # Add a user_id attribute comg from main.py
    
    dropdown = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout for Back Button and ScrollView
        layout = BoxLayout(orientation='vertical')

        # ScrollView and List View for Reports
        scroll = ScrollView()
        self.list_view = MDList()
        self.list_view.clear_widgets()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        
        self.refresh_list()
        self.add_widget(layout)  # Add the layout to the screen

    def go_back(self, instance):
        # Switch to home screen
        self.manager.current = 'homescreen'
    
    def on_enter(self, *args):
        super(AllReportHistory, self).on_enter(*args)
        self.refresh_list()


    def refresh_list(self):
        self.list_view.clear_widgets()  # Clear the current list
        self.populate_list()  # Repopulate the list with fresh data

    def populate_list(self):
        # Clear the existing list items before repopulating
        self.list_view.clear_widgets()

        # SQL query to select only reports with status not equal to 'resolved' or 'False Report'
        cursor.execute("SELECT ReportId, Title FROM report")
        rows = cursor.fetchall()

        red_color = [1, 0, 0, 1]  # Red color in RGBA
        black_color = [0, 0, 0, 1]  # Black color in RGBA

        for row in rows:
            color = red_color if row[1] == 'SOS' else black_color

            item = CustomTwoLineListItem(
                text='Report ID: ' + str(row[0]),
                secondary_text='Title: ' + row[1],
                primary_color=color,
                on_release=lambda x, row=row: self.open_dialog(row)
            )
            self.list_view.add_widget(item)

    # Method to update the text for TwoPartLabel
    def set_two_part_label_text(self, label_id, prefix, data_text):
        setattr(self.dialog_content.ids[label_id].ids.label_prefix, 'text', prefix)
        setattr(self.dialog_content.ids[label_id].ids.label_dynamic, 'text', str(data_text))


    def open_dialog(self, row):
        self.selected_report_id = row[0]  # Store the selected ReportId

        # Fetch data for the selected report
        cursor.execute("SELECT Title, Checklist, image_Path, Details, Urgency, Status, ProfileID, dateCreated, Location FROM report WHERE ReportId = %s", (self.selected_report_id,))
        data = cursor.fetchone()

        # Create dialog content
        self.dialog_content = DialogContent()

        if data:
            # Update label texts
            self.set_two_part_label_text('title', "Title:", data[0])
            self.set_two_part_label_text('checklist', "Checklist:", data[1])
            self.set_two_part_label_text('image_path', "Image Path:", data[2])
            if data[8]:
                self.set_two_part_label_text('location', "Location Link:", data[8])
            else:
                self.set_two_part_label_text('location', "Location Link:", "Unknown")
            self.set_two_part_label_text('details', "Details:", data[3])
            self.set_two_part_label_text('urgency', "Urgency:", data[4])
            self.set_two_part_label_text('status', "Status:", data[5])
            self.set_two_part_label_text('dateCreated', "Report Date :", data[7])


            # Fetch username for the selected report
            self.selected_profile_id = data[6]
            cursor.execute("SELECT ReportId, Title FROM report WHERE status != 'resolved' AND status != 'False Report'")
            data2 = cursor.fetchone()

            if data2:
                self.set_two_part_label_text('username', "Reported by:", str(data2[0]))
            else:
                self.set_two_part_label_text('username', "Reported by:", "Unknown")

        self.dialog = MDDialog(type="custom",
                            content_cls=self.dialog_content,
                            size_hint=(0.8, None),
                            buttons=[
                                MDRaisedButton(
                                    text="Close",
                                    font_name="BPoppins",
                                    font_size="14sp",
                                    theme_text_color="Custom",
                                    text_color=(1, 1, 1, 1),
                                    md_bg_color=(24/255, 106/255, 232/255, 1),
                                    on_release=self.dismiss_dialog
                                )
                            ])
        self.dialog.open()
        

    def menu_callback(self):
        self.dropdown.open()

    # For Cancel Button
    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

# For view  users of admin

# Custom content class for the dialog
class UserContent(BoxLayout):
    pass

class UserAccounts(Screen):
    
    dropdown = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_profile_id = None  # Initialize selected_profile_id

        # Layout for Back Button and ScrollView
        layout = BoxLayout(orientation='vertical')
        
        # ScrollView and List View for Reports
        scroll = ScrollView()
        self.list_view = MDList()
        self.list_view.clear_widgets()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        self.refresh_list()
        self.add_widget(layout)  # Add the layout to the screen

    def go_back(self, instance):
        # Switch to home screen
        self.manager.current = 'homescreen'
    
    def on_enter(self, *args):
        super(UserAccounts, self).on_enter(*args)
        self.refresh_list()


    def refresh_list(self):
        self.list_view.clear_widgets()  # Clear the current list
        self.populate_list()  # Repopulate the list with fresh data

    def populate_list(self):
        # Clear the existing list items before repopulating
        self.list_view.clear_widgets()

        # SQL query to select only reports with status not equal to 'resolved' or 'False Report'
        cursor.execute("SELECT ProfileID, UserName FROM UserProfiles")
        rows = cursor.fetchall()


        for row in rows:

            item = CustomTwoLineListItem(
                text='Profile ID: ' + row[0],
                secondary_text='Username: ' + row[1],
                on_release=lambda x, row=row: self.open_dialog(row)
            )
            self.list_view.add_widget(item)

    # Method to update the text for TwoPartLabel
    def set_two_part_label_text(self, label_id, prefix, data_text):
        setattr(self.dialog_content.ids[label_id].ids.label_prefix, 'text', prefix)
        setattr(self.dialog_content.ids[label_id].ids.label_dynamic, 'text', str(data_text))


    def open_dialog(self, row):
        self.selected_profile_id = row[0]  # Store the selected ReportId

        # Fetch data for the selected report
        cursor.execute("SELECT Username, Email, Birthdate, UserPassword, CreditScore, AccountType FROM UserProfiles WHERE ProfileID = %s", (self.selected_profile_id,))
        data = cursor.fetchone()

        # Process the email and UserPassword data
        if '@' not in data[1]:
            raise ValueError("Invalid email format")
        name, domain = data[1].split('@')
        # Keep the first character and the last character before the @ symbol, mask the rest
        masked_name = name[0] + "*" * (len(name) - 2) + name[-1] if len(name) > 2 else name
        masked_email = masked_name + "@" + domain

        masked_pass = "*" * (len(data[3]))

        # Create dialog content
        self.dialog_content = UserContent()

        if data:
            # Update label texts
            self.set_two_part_label_text('username', "Username", data[0])
            self.set_two_part_label_text('email', "Email:", masked_email) #make obscure
            self.set_two_part_label_text('birthdate', "Birthdate:", data[2])
            self.set_two_part_label_text('password', "User Password:", masked_pass) #make it asterisk
            self.set_two_part_label_text('creditscore', "Credit Score:", data[4])
            if data[5]:
                self.set_two_part_label_text('type', "Account Type:", data[5])
            else:
                self.set_two_part_label_text('type', "Account Type:", "User")


        self.dialog = MDDialog(type="custom",
                            content_cls=self.dialog_content,
                            size_hint=(0.8, None),
                            buttons=[
                                MDFlatButton(
                                    text="Close",
                                    font_name="BPoppins",
                                    font_size="14sp",
                                    theme_text_color="Custom",
                                    text_color=(0, 0, 0, 1),
                                    on_release=self.dismiss_dialog
                                ),
                                MDRaisedButton(
                                    text="Select Acount Type",
                                    font_name="BPoppins",
                                    font_size="14sp",
                                    theme_text_color="Custom",
                                    text_color=(1, 1, 1, 1),
                                    md_bg_color=(24/255, 106/255, 232/255, 1),
                                    on_release=self.menu_callback  # Provide a reference to the method
                                )
                            ])
        self.dialog.open()

        
    def create_dropdown_menu(self, button_instance):
        menu_items = [
            {"viewclass": "OneLineListItem", "text": "User"},
            {"viewclass": "OneLineListItem", "text": "Admin"},
            {"viewclass": "OneLineListItem", "text": "Enforcer"}
        ]

        self.dropdown = MDDropdownMenu(
            caller=button_instance,  # Use the button instance as the caller
            items=menu_items,
            width_mult=4
        )

        for item in menu_items:
            item['on_release'] = lambda x=item['text']: self.option_callback(x)

    def menu_callback(self, button_instance):
        self.create_dropdown_menu(button_instance)
        self.dropdown.open()



    def option_callback(self, option_text):
        self.new_status = option_text
        profileID = self.selected_profile_id
        self.new_status = option_text  # Update self.new_status with the selected option
        print(option_text)
        print(profileID)

        cursor.execute("UPDATE UserProfiles SET AccountType = %s WHERE ProfileID = %s", 
                    (self.new_status, profileID ))

        db.commit()
        self.dropdown.dismiss()
        self.refresh_list()
        self.dismiss_dialog()
    
    # For Cancel Button
    def dismiss_dialog(self, *args):
        self.dialog.dismiss()