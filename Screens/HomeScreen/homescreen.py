from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.core.window import Window

Window.size = (360, 600)

class HomeScreen(MDBoxLayout):
    pass

class MyApp(MDApp):
    def build(self):
        return Builder.load_file("homescreen.kv")

if __name__ == "__main__":
    MyApp().run()
