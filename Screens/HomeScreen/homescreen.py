from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window

Window.size = (300, 500)

class HomeScreen(MDBoxLayout):
    pass

class MyApp(MDApp):
    def build(self):
        return Builder.load_file("homescreen.kv")

if __name__ == "__main__":
    MyApp().run()
