from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class LogApp(App):
    def build(self):
        #Builder.load_file("log.kv")
        return LogWindow()


class LogWindow(Widget):
    pass


class LogButton(Button):
    pass
