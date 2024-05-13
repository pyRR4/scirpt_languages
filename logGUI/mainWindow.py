from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.config import Config


class LogApp(App):
    def build(self):
        #Builder.load_file("log.kv")
        self.title = "Log browser"
        return LogWindow()


class LogWindow(Widget):
    path = ObjectProperty(None)
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)
    scrolled_list = ObjectProperty(None)
    host = ObjectProperty(None)
    date = ObjectProperty(None)
    time = ObjectProperty(None)
    timezone = ObjectProperty(None)
    status_code = ObjectProperty(None)
    method = ObjectProperty(None)
    resource = ObjectProperty(None)
    size = ObjectProperty(None)


class LogGrid(GridLayout):
    pass
