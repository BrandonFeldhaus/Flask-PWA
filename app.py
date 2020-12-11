import os

from flask import Flask, make_response, send_from_directory
from flask import render_template, request
from find_mac import get_ips
from scraper import parse
import sys


import requests

app = Flask(__name__)

'''
This adds index.html to the pages, if its a post request that it started by the submit button
retrieves ip from form box, run the get_ips function, return list of ip and macs,
Returns the html, passes info to the html to display
'''
@app.route('/', methods=['GET', 'POST'])
def main_page():
    errors = []
    results = []
    if request.method == "POST":
        try:
            target_ip = request.form['url']
            results = get_ips(target_ip)
        except:
            errors.append(sys.exc_info()[0])

    return render_template('index.html', errors=errors, results=results)


'''
Adds the manifest.json which is used by chrome to determine download options such as logo, banner, etc
'''
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')


'''
Add the offline html to route to be able to cache it
'''
@app.route('/offline.html')
def offline():
    return send_from_directory('/static/pages/offlinepages', 'offline.html')


'''
Add the service worker file to route to be able to cache
Content-type is there to eliminate a MIME error
'''
@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js'), 200, {'Content-Type': 'text/javascript'}

'''
'''

@app.route('/anotherpage.html', methods=['GET', 'POST'])
def scrape():
    errors = []
    results = ""
    if request.method == "POST":
        try:
            target_url = request.form['urlname']
            results = parse(target_url)

        except:
            errors.append("unable to get url...")

    return render_template('/anotherpage.html', errors=errors, results=results)


'''
If you wish to change the port or debug mode and youre using PyCharm, edit your configurations.
I found debug mode will reload assets if they arent showing changes on local host and changing the port number helps
eliminate certain caches
'''
if __name__ == '__main__':
    app.run()
