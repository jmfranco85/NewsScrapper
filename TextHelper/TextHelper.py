"""
Created on 23 jun. 2017

@author: jmfranco
"""

from html.parser import HTMLParser
import html as Html


def clean_html(html_text):
    unescaped_html = Html.unescape(html_text)
    html_stripper = HTMLStripper()
    html_stripper.feed(unescaped_html)
    str_without_tags = html_stripper.get_data()
    return " ".join(str_without_tags.split())


class HTMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)



