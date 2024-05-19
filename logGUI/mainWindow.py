import datetime
import os.path
import re

from kivy.app import App
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from StrukturyDanych.lists import read_log


class LogApp(App):
    def __init__(self, **kwargs):
        super(LogApp, self).__init__(**kwargs)
        self.log_window = None

    def build(self):
        self.title = "Log browser"
        self.log_window = LogWindow()
        return self.log_window


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    def select_with_touch(self, node, touch=None):
        if super().select_with_touch(node, touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        touch.grab(self)
        self.clear_selection()
        if self.select_node(node):
            self.selected_nodes.append(node)
        return True


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        log_window = App.get_running_app().log_window
        if log_window:
            log_window.refresh_data(index, is_selected)
        if index < len(rv.data):
            if is_selected:
                print("selection changed to {0}".format(rv.data[index]))
            else:
                print("selection removed for {0}".format(rv.data[index]))


class LogPopup(Popup):
    popup_text = ObjectProperty(None)

    def __init__(self, text, **kwargs):
        super(LogPopup, self).__init__(**kwargs)
        self.popup_text.text = text


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

    def select_node(self, index):
        if index is not None:
            self.layout_manager.deselect_node(index)
        self.layout_manager.select_node(index)


class LogWindow(Widget):

    path = ObjectProperty(None)
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)
    host = ObjectProperty(None)
    date = ObjectProperty(None)
    time = ObjectProperty(None)
    timezone = ObjectProperty(None)
    status_code = ObjectProperty(None)
    method = ObjectProperty(None)
    resource = ObjectProperty(None)
    bytes = ObjectProperty(None)
    logs = ObjectProperty(None)
    rv = ObjectProperty(None)
    selected_index = ObjectProperty(None)

    def show_file_chooser(self):
        file_chooser = FileChooser(self.set_path)
        file_chooser.file_chooser.path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
        file_chooser.open()

    def set_path(self, pth):
        self.path.text = pth

    def filter_logs(self):
        new_data = []
        end_text = self.end_date.text
        start_text = self.start_date.text
        end_date = None
        start_date = None
        if end_text != "":
            try:
                end_date = datetime.datetime.strptime(end_text, "%d-%m-%Y")
            except ValueError:
                pass #popup!!!!
        if start_text != "":
            try:
                start_date = datetime.datetime.strptime(start_text, "%d-%m-%Y")
            except ValueError:
                pass #popup!!!!
        if self.logs:
            if end_date and start_date:
                for log in self.logs:
                    if start_date < log[1] < end_date:
                        new_data.append(log)

            elif self.logs and end_date:
                for log in self.logs:
                    if log[1] < end_date:
                        new_data.append(log)

            elif self.logs and start_date:
                for log in self.logs:
                    if start_date < log[1]:
                        new_data.append(log)

            else:
                new_data = self.logs

            self.rv.data = [{'viewclass': 'SelectableLabel', 'text': log[8], 'selected': False} for log in new_data]

        else: #popup!
            pass

    def next_log(self):
        if self.rv.data and self.selected_index is not None and self.selected_index < (len(self.rv.data) - 1):
            self.selected_index += 1
            self.rv.select_node(self.selected_index)
            self.scroll_to_index(self.selected_index)

    def previous_log(self):
        if self.rv.data and self.selected_index is not None and self.selected_index > 0:
            self.selected_index -= 1
            self.rv.select_node(self.selected_index)
            self.scroll_to_index(self.selected_index)

    def scroll_to_index(self, index):
        if self.rv:
            total_count = len(self.rv.data)
            if total_count == 0:
                return
            layout = self.rv.layout_manager
            if layout:
                proportion = index / total_count
                scroll_y = 1 - proportion
                self.rv.scroll_y = scroll_y

    def load_file(self):
        f_path = self.path.text
        if os.path.isfile(f_path):
            with open(f_path, 'r', encoding='utf8') as f:
                self.logs = read_log(f)

            self.filter_logs()

            if self.rv.data is []:
                popup = LogPopup("Wybrany plik nie zawiera logów, które można wyświetlić!")
                popup.open()
        else:
            popup = LogPopup("Niepoprawna ścieżka do pliku lub plik nie istnieje!")
            popup.open()

    def refresh_data(self, index, is_selected):
        if is_selected:
            self.selected_index = index
            self.host.text = (self.logs[index])[0]
            no_hour_date = (self.logs[index])[1].date()
            hour = (self.logs[index])[1].time()
            self.date.text = str(no_hour_date)
            self.time.text = str(hour)
            self.timezone.text = str((self.logs[index])[7])
            self.status_code.text = str((self.logs[index])[5])
            self.method.text = (self.logs[index])[2]
            self.resource.text = (self.logs[index])[3]
            self.bytes.text = str((self.logs[index])[6])
        else:
            self.host.text = ""
            self.date.text = ""
            self.time.text = ""
            self.timezone.text = ""
            self.status_code.text = ""
            self.method.text = ""
            self.resource.text = ""
            self.bytes.text = ""


class LogGrid(GridLayout):
    pass


class LogTextInput(TextInput):
    pass


class DateInput(TextInput):
    date_regex = re.compile(r'^\d{2}-\d{2}-\d{4}$')

    def __init__(self, **kwargs):
        super(DateInput, self).__init__(**kwargs)

    def insert_text(self, substring, from_undo=False):
        allowed_chars = '0123456789-'
        text = self.text

        if len(text) == 2 or len(text) == 5:
            substring = '-' + substring

        if len(text) < 10 and all(char in allowed_chars for char in substring):
            super(DateInput, self).insert_text(substring, from_undo=from_undo)

    def on_focus(self, instance, value):
        if not value:
            if not self.date_regex.match(self.text):
                self.text = ''
                self.hint_text = 'Invalid date format. Use DD-MM-YYYY'
            else:
                log_window = App.get_running_app().log_window
                box_lay = self.parent.parent
                log_label = None
                for child in box_lay.children:
                    if isinstance(child, Label):
                        log_label = child
                if log_label:
                    log_window.filter_logs()


class LogLabel(Label):
    pass


class FileChooser(Popup):
    def __init__(self, on_selection, **kwargs):
        super(FileChooser, self).__init__(**kwargs)
        self.file_chooser = self.ids.filechooser
        self.file_chooser.bind(selection=lambda chooser, selection: self.on_file_select(on_selection, selection))

    def on_file_select(self, on_selection, selection):
        if selection:
            on_selection(selection[0])
        self.dismiss()

