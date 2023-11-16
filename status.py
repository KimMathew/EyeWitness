import mysql.connector
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

# Kivy Builder String for the custom content layout
KV = '''
<Button@MDRaisedButton>:
    size_hint: 0.66, 0.065
    background_color: 0, 0, 0, 0
    font_name: "BPoppins"
    canvas.before:
        Color:
            rgba: 52/255, 0, 231/255, 255/255
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [5] 

<DialogContent>:
    orientation: "vertical"
    size_hint_y: None
    height: "400dp"

    BoxLayout:
        size_hint_y: None
        height: self.minimum_height  # Adjust the height to fit the content
        
        MDLabel:
            text: "Update Status"
            font_name: "BPoppins"
            font_size: "22sp"
            size_hint_y: None
            height: self.texture_size[1]

    ScrollView:
        size_hint_y: None
        height: 440  # Adjust based on your dialog box size

        GridLayout:
            cols: 1
            size_hint_y: None
            size_hint_x: 1  # Take full width of the ScrollView
            height: self.minimum_height
            spacing: "30dp"
            padding: [30, 50, 30, 0]  # Padding: [left, top, right, bottom]
            pos_hint: {'center_x': 0.5, 'top': 1}  # Adjust pos_hint as needed

            MDLabel:
                id: title
                font_name: "MPoppins"
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: (1)
                height: self.texture_size[1]
                
            MDLabel:
                id: checklist
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
            
            MDLabel:
                id: image_path
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
                
            MDLabel:
                id: details
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
                
            MDLabel:
                id: urgency
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
            
            MDLabel:
                id: status
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]

    # Added        
    GridLayout:
        cols: 2
        spacing: "15sp"
        size_hint_y: None
        height: "48dp"  # Fixed height for the button area

        Button:
            id: button
            text: "False Report"
            # on_release: app.menu_callback()
            
        Button:
            id: button
            text: "Select Status"
            on_release: app.menu_callback()
'''

class CustomTwoLineListItem(TwoLineListItem): # Added
    def __init__(self, primary_font_name="BPoppins", secondary_font_name="MPoppins", primary_font_size=20, secondary_font_size=16, **kwargs):
        super().__init__(**kwargs)
        # Override primary label
        self.ids._lbl_primary.font_name = primary_font_name
        self.ids._lbl_primary.font_size = primary_font_size 
        # Override secondary label
        self.ids._lbl_secondary.font_name = secondary_font_name
        self.ids._lbl_secondary.font_size = secondary_font_size

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

class ListApp(MDApp):
    
    dropdown = ObjectProperty()
    
    def build(self):
        Builder.load_string(KV)  # Load the Kivy Builder string
        self.screen = Screen()
        # self.theme_cls.primary_palette = "Green"
        scroll = ScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        self.populate_list()
        self.screen.add_widget(scroll)
        return self.screen

    def populate_list(self):
        cursor.execute("SELECT ReportId, Title FROM report")
        rows = cursor.fetchall()

        for row in rows:
            item = CustomTwoLineListItem( # Added
                text='Report ID: ' + str(row[0]),
                secondary_text='Title: ' + row[1],
                on_release=lambda x, row=row: self.open_dialog(row)
            )
            self.list_view.add_widget(item)

    # displaying the reports
    def open_dialog(self, row):
        self.selected_report_id = row[0]  # Store the selected ReportId

        # Fetch data for the selected report
        cursor.execute("SELECT Title, Checklist, image_Path, Details, Urgency, Status FROM report WHERE ReportId = %s", (self.selected_report_id,))
        data = cursor.fetchone()

        # Create dialog content
        self.dialog_content = DialogContent()

        if data:
            # Update label texts
            self.dialog_content.ids.title.text = "Title: " + str(data[0])
            self.dialog_content.ids.checklist.text = "Checklist: " + str(data[1])
            self.dialog_content.ids.image_path.text = "Image Path: " + str(data[2])
            self.dialog_content.ids.details.text = "Details: " + str(data[3])
            self.dialog_content.ids.urgency.text = "Urgency: " + str(data[4])
            self.dialog_content.ids.status.text = "Status: " + str(data[5])

        self.dialog = MDDialog(type="custom",
                               content_cls=self.dialog_content,  # Use custom content class
                               size_hint=(0.8, None),
                               buttons=[
                                   MDFlatButton(
                                       text="Submit",
                                       theme_text_color="Custom",
                                       text_color=self.theme_cls.primary_color,
                                       on_release=self.submit_data
                                   ),
                               ])
        self.dialog.open()
        self.create_dropdown_menu()

    def create_dropdown_menu(self):
        menu_items = [
            {"viewclass": "OneLineListItem", "text": "Preparing to deploy"},
            {"viewclass": "OneLineListItem", "text": "On the Process"},
            {"viewclass": "OneLineListItem", "text": "Resolved"}
        ]

        self.dropdown = MDDropdownMenu(
            caller=self.dialog_content.ids.button,
            items=menu_items,
            width_mult=4
        )

        for item in menu_items:
            item['on_release'] = lambda x=item['text']: self.option_callback(x)

    def menu_callback(self):
        self.dropdown.open()

    def option_callback(self, option_text):
        self.new_status = option_text
        print(option_text)
        self.dropdown.dismiss()

    def submit_data(self, instance):
        cursor.execute("UPDATE report SET status = %s WHERE ReportId = %s", (self.new_status, self.selected_report_id))
        db.commit()
        self.dialog.dismiss()

if __name__ == "__main__":
    # Added Font Directory
    LabelBase.register(name = "MPoppins", fn_regular="Screens\\Assets\\Poppins\\Poppins-Medium.ttf")
    LabelBase.register(name = "BPoppins", fn_regular="Screens\\Assets\\Poppins\\Poppins-SemiBold.ttf")

    ListApp().run()