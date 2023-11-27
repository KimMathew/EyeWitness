import mysql.connector
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDIconButton

# Kivy Builder String for the custom content layout
KV = '''

<TwoPartLabel@BoxLayout>:
    orientation: 'horizontal'
    size_hint_y: None
    size_hint_x: 1
    padding: 1

    MDLabel:
        id: label_prefix
        font_name: "BPoppins"
        halign: "left"  
        size_hint_x: 1
        size_hint_y: None
        text: ""
        font_size: "15sp"
        text_size: self.width, None

    MDLabel:
        id: label_dynamic
        font_name: "MPoppins"
        halign: "center"  
        size_hint_x: 1
        size_hint_y: None
        text: ""
        font_size: "14sp"
        text_size: self.width, None
        

<Separator@MDSeparator>:
    height: "1dp"
'''

class CustomTwoLineListItem(TwoLineListItem):
    def __init__(self, primary_font_name="BPoppins", secondary_font_name="MPoppins", 
                 primary_font_size=20, secondary_font_size=16, 
                 primary_color=[0, 0, 0, 1], secondary_color=[0, 0, 0, 1], **kwargs):
        super().__init__(**kwargs)
        # Override primary label properties
        self.ids._lbl_primary.font_name = primary_font_name
        self.ids._lbl_primary.font_size = primary_font_size 
        self.ids._lbl_primary.color = primary_color

        # Override secondary label properties
        self.ids._lbl_secondary.font_name = secondary_font_name
        self.ids._lbl_secondary.font_size = secondary_font_size
        self.ids._lbl_secondary.color = secondary_color
        self.ids._lbl_secondary.text_size = (self.width, None)  # Set the width to the label's width
        self.ids._lbl_secondary.size_hint_y = None  # Allow the label to grow vertically
        self.ids._lbl_secondary.halign = 'left'  # Horizontal alignment
        self.ids._lbl_secondary.valign = 'top'  # Vertical alignment

        # Bind size to properly resize with the layout
        self.bind(size=self._update_text_size)

    def _update_text_size(self, instance, value):
        self.ids._lbl_secondary.text_size = (value[0], None)


# Custom content class for the dialog
class DialogContent(BoxLayout):
    pass

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

class UserInbox(Screen):
    user_id = None  # Add a user_id attribute comg from main.py
    
    dropdown = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)

        # Layout for Back Button and ScrollView
        layout = BoxLayout(orientation='vertical')

        # Back Button
        back_button = MDIconButton(
            icon="arrow-left",
            font_size="30sp",
            theme_text_color="Custom",
            text_color=(26/255, 24/255, 58/255, 255/255),
            on_release=self.go_back,
        )
        
        # Add Back Button to Layout
        layout.add_widget(back_button)
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
        super(UserInbox, self).on_enter(*args)
        self.refresh_list()


    def refresh_list(self):
        self.list_view.clear_widgets()  # Clear the current list
        self.populate_list()  # Repopulate the list with fresh data

    def populate_list(self):
        # Clear the existing list items before repopulating
        self.list_view.clear_widgets()

        # SQL query to select only reports with status not equal to 'resolved' or 'False Report'
        query = "SELECT ProfileID, ReportID, Message FROM UserInbox WHERE ProfileID = %s"
        cursor.execute(query, (self.user_id,))
        rows = cursor.fetchall()

        for row in rows:
            
            item = CustomTwoLineListItem(
                text='Report ID: ' + str(row[1]),
                secondary_text= row[2],
            )
            self.list_view.add_widget(item)

    # Method to update the text for TwoPartLabel
    def set_two_part_label_text(self, label_id, prefix, data_text):
        setattr(self.dialog_content.ids[label_id].ids.label_prefix, 'text', prefix)
        setattr(self.dialog_content.ids[label_id].ids.label_dynamic, 'text', str(data_text))

        

    def menu_callback(self):
        self.dropdown.open()

    # For Cancel Button
    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

