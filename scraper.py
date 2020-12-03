from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlopen
import re

blacklist = []  # List of unwanted words


def multiple_replace(list, text):
    # Create a regex from the words in the blacklist, ignoring case.
    regex = re.compile("(%s)" % "|".join(map(re.escape, list)), re.IGNORECASE)

    # Return a version of the text with the unwanted words subbed out.
    return regex.sub('', text)


def hostname(url):
    o = urlparse(url)

    hn = o.hostname     # Example: www.apple.com

    split = hn.split('.')

    VendorWithoutDomain = split[1]

    VendorWithDomain = split[1] + '.' + split[2]

    blacklist.append(VendorWithoutDomain)

    blacklist.append(VendorWithDomain)

    return blacklist


# This function DOESN'T cause an issue with time. The web automated stuff did, which has been replaced for now.
def reafter(t):
    t = t.encode('ascii', 'ignore').decode('ascii', 'ignore')  # Remove Unicode

    t = str.translate(t, {ord(i): None for i in r"'\'"})  # Remove backslashes

    t = re.sub(r'\s\s+[\s+]', '', t)  # Remove \n|\t|\r # Trim additional whitespace

    rep1 = re.compile(re.escape('footer') + '^.*?', re.IGNORECASE)  # Remove headers and footers, if there are any

    rep2 = re.compile('^.*' + re.escape('header'), re.IGNORECASE)

    t = re.sub(rep1, '', t)

    t = re.sub(rep2, '', t)

    t = multiple_replace(blacklist, t)

    return t


def parse(t):
    hostname(t)

    page = urlopen(t)

    # Read the page, decode utf-8
    html_read = page.read().decode("utf-8")

    soup = BeautifulSoup(html_read, "html.parser")

    p = soup.find_all(re.compile(".*"), {"id": re.compile(".*" + re.escape("nav") + ".*", re.IGNORECASE)})  # Find all tags with nav in their id

    for match in p:
        match.decompose()  # Removes all tags with nav in their id, along with their content

    text = soup.get_text(separator=' ', strip=True)

    text = reafter(text)

    return text


def main():
    print(parse("https://privacy.microsoft.com/en-us/privacystatement"))


if __name__ == '__main__':
    main()
