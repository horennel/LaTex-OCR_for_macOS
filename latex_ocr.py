from pix2text import Pix2Text, merge_line_texts
from PIL import ImageGrab
import pyperclip
import rumps

from threading import Thread

SUCCESS = 0
NO_COPY_ERROR = 1
UN_KNOWN_ERROR = 2


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
        super(LatexOrcApplication, self).__init__(name=name, icon='./icons/menu_bar_logo.png', quit_button="Quit")
        self.p2t = Pix2Text(analyzer_config=dict(model_name='mfd'))

    @rumps.clicked("Formula OCR")
    def recognize_formula(self, _):
        # Only recognize formula
        image = self.get_image()
        if image:
            ocr_task = Thread(target=self.start_ocr_and_copy, args=(self.p2t.recognize_formula, image, 608))
            ocr_task.start()

    @rumps.clicked("Mixed OCR")
    def recognize_mixed(self, _):
        # Identify mixed image
        image = self.get_image()
        if image:
            ocr_task = Thread(target=self.start_ocr_and_copy, args=(self.p2t.recognize, image, 608))
            ocr_task.start()

    @rumps.notifications
    def notification_center(self, info):
        if 'Unknown' in info.subtitle:
            error_window = rumps.Window(title='Error Message', default_text=info.message)
            error_window.icon = './icons/menu_bar_logo.png'
            error_window.run()

    @rumps.clicked("On / Off")
    def onoff(self, _):
        formula_ocr_button = self.menu['Formula OCR']
        if formula_ocr_button.callback is None:
            formula_ocr_button.set_callback(self.recognize_formula)
        else:
            formula_ocr_button.set_callback(None)
        mixed_ocr_button = self.menu['Mixed OCR']
        if mixed_ocr_button.callback is None:
            mixed_ocr_button.set_callback(self.recognize_mixed)
        else:
            mixed_ocr_button.set_callback(None)

    def get_image(self):
        image = ImageGrab.grabclipboard()
        if not image:
            rumps.notification(**Message(NO_COPY_ERROR).to_json())
            return None
        return image

    def start_ocr_and_copy(self, ocr_func, image, resized_shape):
        formula_ocr_button = self.menu['Formula OCR']
        formula_ocr_button.set_callback(None)
        mixed_ocr_button = self.menu['Mixed OCR']
        mixed_ocr_button.set_callback(None)
        onoff_button = self.menu['On / Off']
        onoff_button.set_callback(None)
        self.title = 'IN OCR'
        try:
            result = ocr_func(image, resized_shape=resized_shape)
            if isinstance(result, str) is False:
                result = merge_line_texts(result, auto_line_break=True)
            pyperclip.copy(result)
            rumps.notification(**Message(SUCCESS).to_json())
        except Exception as e:
            rumps.notification(**Message(UN_KNOWN_ERROR, str(e)).to_json())
        formula_ocr_button.set_callback(self.recognize_formula)
        mixed_ocr_button.set_callback(self.recognize_mixed)
        onoff_button.set_callback(self.onoff)
        self.title = None


if __name__ == "__main__":
    LatexOrcApplication(name='').run()
