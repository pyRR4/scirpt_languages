from kivy.app import App
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from StrukturyDanych.lists import read_log


class LogApp(App):
    def build(self):
        #Builder.load_file("log.kv")
        self.title = "Log browser"
        return LogWindow()


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

    def expand_label(self):
        self.text_size = (self.width, None)
        self.height = self.texture_size[1]

    def shrink_label(self):
        self.text_size = (None, None)
        self.height = 56

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
        log_window = self.find_log_window()
        if log_window:
            log_window.refresh_data(index, is_selected)
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

    def find_log_window(self):
        parent = self.parent
        while parent:
            if isinstance(parent, LogWindow):
                return parent
            parent = parent.parent
        return None


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []


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

    def load_file(self): #ZABEZPIECZYĆ!!!
        f_path = self.path.text
        with open(f_path, 'r', encoding='utf8') as f:
            self.logs = read_log(f)

        self.rv.data = [{'viewclass': 'SelectableLabel', 'text': log[8], 'selected': False} for log in self.logs]

    def refresh_data(self, index, is_selected):
        if is_selected:
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


class LogLabel(Label):
    pass

# spacing: (0.01 * self.parent.height)
#                 padding: (0.04 * self.parent.height)

