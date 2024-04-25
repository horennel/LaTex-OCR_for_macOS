from pix2text import Pix2Text
from PIL import ImageGrab
import pyperclip
import rumps

from threading import Thread
from queue import Queue

WORKING_TITLE = 'working'
LISTENING_EVENT_INTERVAL = 1.5  # (s)

SUCCESS = 0
NO_COPY_ERROR = 1
UN_KNOWN_ERROR = 2

FREE_MODE = 0
FORMULA_AUTO_MODE = 1
MIXED_AUTO_MODE = 2
TEXT_AUTO_MODE = 3

F = 'Formula OCR'
M = 'Mixed OCR'
T = 'Text OCR'
A = 'Auto On/Off'


class Message(object):
    def __init__(self, msg_type, message=None):
        if msg_type == SUCCESS:
            self.title = "Success!"
            self.subtitle = 'Success!Copied to clipboard.'
            self.message = ''
        else:
            self.title = 'Error!'
            if msg_type == NO_COPY_ERROR:
                self.subtitle = 'You did not copy the screenshot.'
                self.message = 'Please copy the picture first.'
            elif msg_type == UN_KNOWN_ERROR:
                self.subtitle = 'Unknown error'
                self.message = message

    def to_json(self):
        attrs = vars(self)
        attrs = {k: v for k, v in attrs.items() if not k.startswith('__') and not callable(v)}
        return attrs


class LatexOrcApplication(rumps.App):
    def __init__(self, name):
        super(LatexOrcApplication, self).__init__(name=name, icon='./icons/menu_bar_logo_auto_off.png',
                                                  quit_button="Quit")
        self.p2t = Pix2Text(analyzer_config=dict(model_name='mfd'))
        self.q = Queue(maxsize=1)
        self.last_img = 1
        self.mode = FREE_MODE

    @rumps.clicked("Formula OCR")
    def recognize_formula(self, sender):
        if self.mode == FREE_MODE:
            image = self.get_image()
            if image:
                ocr_task = Thread(target=self.start_ocr_and_copy, args=(F, image))
                ocr_task.start()
        else:
            self.mode_state_change(sender, F)

    @rumps.clicked("Mixed OCR")
    def recognize_mixed(self, sender):
        if self.mode == FREE_MODE:
            image = self.get_image()
            if image:
                ocr_task = Thread(target=self.start_ocr_and_copy, args=(M, image))
                ocr_task.start()
        else:
            self.mode_state_change(sender, M)

    @rumps.clicked("Text OCR")
    def recognize_text(self, sender):
        if self.mode == FREE_MODE:
            image = self.get_image()
            if image:
                ocr_task = Thread(target=self.start_ocr_and_copy, args=(T, image))
                ocr_task.start()
        else:
            self.mode_state_change(sender, T)

    @rumps.notifications
    def notification_center(self, info):
        if 'Unknown' in info.subtitle:
            error_window = rumps.Window(title='Error Message', default_text=info.message)
            error_window.icon = './icons/menu_bar_logo_auto_off.png'
            error_window.run()

    @rumps.clicked("Auto On/Off")
    def onoff(self, sender):
        if sender.state == 0:
            formula_ocr_button = self.menu[F]
            formula_ocr_button.state = 1
            formula_ocr_button.set_callback(None)
            sender.state = 1
            self.mode = FORMULA_AUTO_MODE
            self.icon = './icons/menu_bar_logo_auto_on.png'
        else:
            self.mode = FREE_MODE
            self.clicked_open([F, M, T])
            sender.state = 0
            self.icon = './icons/menu_bar_logo_auto_off.png'

    @rumps.timer(LISTENING_EVENT_INTERVAL)
    def automatic_ocr(self, _):
        if self.mode != FREE_MODE:
            image = ImageGrab.grabclipboard()
            if image and image != self.last_img:
                self.q.put(image)
                self.last_img = image

    @staticmethod
    def get_image():
        image = ImageGrab.grabclipboard()
        if not image:
            rumps.notification(**Message(NO_COPY_ERROR).to_json())
            return None
        return image

    def start_ocr_and_copy(self, ocr_func, image, is_auto_ocr=False):
        if is_auto_ocr is False:
            self.clicked_close([F, M, T])
        self.title = WORKING_TITLE
        try:
            if ocr_func == F:
                result = self.p2t.recognize_formula(image)
            elif ocr_func == M:
                result = self.p2t.recognize(image, resized_shape=608, return_text=True)
            else:
                result = self.p2t.recognize_text(image)
            pyperclip.copy(result)
            rumps.notification(**Message(SUCCESS).to_json())
        except Exception as e:
            rumps.notification(**Message(UN_KNOWN_ERROR, str(e)).to_json())
        if is_auto_ocr is False:
            self.clicked_open([F, M, T], False)
        self.title = None

    def auto_ocr(self):
        while True:
            image = self.q.get()
            if self.mode == FORMULA_AUTO_MODE:
                self.start_ocr_and_copy(F, image, is_auto_ocr=True)
            elif self.mode == MIXED_AUTO_MODE:
                self.start_ocr_and_copy(M, image, is_auto_ocr=True)
            elif self.mode == TEXT_AUTO_MODE:
                self.start_ocr_and_copy(T, image, is_auto_ocr=True)

    def clicked_open(self, menus_name, change_state=True):
        for menu_name in menus_name:
            menu = self.get_menu(menu_name)
            menu.set_callback(self.menu_bind(menu_name))
            if change_state is True and menu_name != A:
                menu.state = 0

    def clicked_close(self, menus_name):
        for menu_name in menus_name:
            self.get_menu(menu_name).set_callback(None)

    def mode_state_change(self, sender, mode_name):
        sender.state = 1
        self.clicked_close([mode_name])
        if mode_name == F:
            self.mode = FORMULA_AUTO_MODE
            self.clicked_open([M, T])
        elif mode_name == M:
            self.mode = MIXED_AUTO_MODE
            self.clicked_open([F, T])
        elif mode_name == T:
            self.mode = TEXT_AUTO_MODE
            self.clicked_open([F, M])

    def get_menu(self, menu_name):
        return self.menu[menu_name]

    def menu_bind(self, menu_name):
        bind = {
            F: self.recognize_formula,
            M: self.recognize_mixed,
            T: self.recognize_text,
            A: self.onoff
        }
        return bind[menu_name]

    def run(self, **options):
        self.mode = FREE_MODE
        t = Thread(target=self.auto_ocr)
        t.start()
        super().run(**options)


if __name__ == "__main__":
    LatexOrcApplication(name='').run()
