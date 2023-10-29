from kivy.core.text import LabelBase
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (360, 600)


class MyApp(MDApp):
    def build(self):
        screen_manager = MDScreenManager()
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("Screens\HomeScreen\homescreen.kv"))
        
        return screen_manager

if __name__ == "__main__":
    LabelBase.register(name = "MPoppins", fn_regular="C:\\Fonts\\Poppins\\Poppins-Medium.ttf")
    LabelBase.register(name = "BPoppins", fn_regular="C:\\Fonts\\Poppins\\Poppins-SemiBold.ttf")

    MyApp().run()