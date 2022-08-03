from flask import render_template
from re import sub

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