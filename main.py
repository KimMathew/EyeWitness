from kivy.core.text import LabelBase
from kivymd.uix.menu import MDDropdownMenu 
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.icon_definitions import md_icons
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.metrics import dp

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
        screen_manager = MDScreenManager()
        screen_manager.add_widget(Builder.load_file("Screens\HomeScreen\homescreen.kv"))
        screen_manager.add_widget(Builder.load_file("Screens\HomeScreen\screenreport.kv"))
        screen_manager.add_widget(Builder.load_file("Screens\LoginScreen\main.kv"))
        screen_manager.add_widget(Builder.load_file("Screens\LoginScreen\login.kv"))
        screen_manager.add_widget(Builder.load_file("Screens\LoginScreen\signup.kv"))
        screen_manager.add_widget(Builder.load_file("Screens\HomeScreen\homescreen_admin.kv"))
        
        return screen_manager
    
    # For DropDown
    def show_incident_type_dropdown(self, caller):
        incident_type = ["Medical Emergency", "Natural Disaster", "Security Threat", "Others"]
        self.dropdown_handler.show_custom_dropdown(caller, incident_type)
        

    def create_menu_items(self, options, caller):
        return self.dropdown_handler.create_menu_items(options, caller)

    def menu_callback(self, text_item, caller):
        self.dropdown_handler.menu_callback(text_item, caller)

    def show_urgency_dropdown(self, caller):
        urgency_items = ["Low", "Medium", "High"]
        self.dropdown_handler.show_custom_dropdown(caller, urgency_items)

    # Dialog for Submitting
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
        # Schedule the dialog to be dismissed after 2 seconds
        Clock.schedule_once(self.dismiss_dialog, 2)

    def dismiss_dialog(self, dt):
        self.dialog.dismiss()
        # Schedule the transition to the home screen to happen after a short delay
        Clock.schedule_once(self.transition_to_home, 0.5)

    def transition_to_home(self, dt):
        self.root.current = 'homescreen'

if __name__ == "__main__":
    LabelBase.register(name = "MPoppins", fn_regular="Screens\\Assets\\Poppins\\Poppins-Medium.ttf")
    LabelBase.register(name = "BPoppins", fn_regular="Screens\\Assets\\Poppins\\Poppins-SemiBold.ttf")

    MyApp().run()