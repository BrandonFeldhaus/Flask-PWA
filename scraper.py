from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import re

# This function causes the issue with time
def reafter(t):
    t = t.encode('ascii', 'ignore').decode('ascii', 'ignore')  # Remove Unicode

    t = str.translate(t, {ord(i): None for i in r"'\'"})  # Remove backslashes

    t = re.sub(r'[\s+]', ' ', t)  # Remove \n|\t|\r

    t = re.sub(r'\s\s+', ' ', t)  # Trim additional whitespace

    rep1 = re.compile(re.escape('footer') + '^.*?', re.IGNORECASE)  # Remove footers, if there are any

    rep2 = re.compile('^.*?' + re.escape('Last Updated'), re.IGNORECASE)    # Remove all text before "Last Updated", if there is one

    t = re.sub(rep1, '', t)

    t = re.sub(rep2, '', t)

    return t


def parse(t):
    opts = Options()

    # set_headless is deprecated
    opts.headless = True

    browser = Firefox(options=opts)

    browser.get(t)

    separator = ' '  # To separate all concatenated words

    soup = BeautifulSoup(browser.page_source, "html.parser")

    text = soup.get_text(separator, strip=True)

    text = reafter(text)

    return text


def main():
    parse("https://privacy.microsoft.com/en-us/privacystatement")


if __name__ == '__main__':
    main()