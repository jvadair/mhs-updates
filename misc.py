from flask import render_template
from re import sub
from datetime import datetime

name_codes = {
    "&quot;": '"',
    "&amp;": '&',
    "&apos;": "'",
    "&lt;": '<',
    "&gt;": '>',
    "&nbsp;": " ",
}

def check_for_keys(d: dict, *args):
    for arg in args:
        if not arg in d.keys():
            return False
    # If all pass
    return True

def errorpage(text):
    return render_template('error.html', error=text)

def fix_html(html):
    html = sub('<[^<]+?>', '', html)  # Removes <tags/>
    for name_code in name_codes.items():
        html = html.replace(name_code[0], name_code[1])
    return html

# Custom logging function
class Log:

    colors = {
        'normal': '\033[0m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'gray': '\033[38;5;245m',
    }

    def __init__(self, loglevel=1):
        # Log levels:
        # 0: DEBUG
        # 1: INFO
        # 2: WARN
        # 3: ERROR
        self.loglevel = loglevel
    
    def time(self):
        return datetime.now().strftime('%x - %X')

    def debug(self, *args, color=str(colors['gray'])):
        if self.loglevel == 0:
            print(self.time() + color, '[DEBUG]', *args, '\033[0m')

    def info(self, *args, color=''):
        if self.loglevel <= 1:
            print(self.time() + color, '[INFO]', *args, '\033[0m')

    def warn(self, *args, color=str(colors['yellow'])):
        if self.loglevel <= 2:
            print(self.time() + color, '[WARN]', *args, '\033[0m')

    def error(self, *args, color=str(colors['red'])):
        if self.loglevel <= 3:
            print(self.time() + color, '[ERROR]', *args, '\033[0m')
        