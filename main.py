# Module imports
from flask import Flask, request, session, redirect
from flask import render_template as rt_default
from pyndb import PYNDatabase
from os import urandom, path
from time import sleep, mktime
from datetime import datetime
import feedparser, requests, json
import fetchtwitter
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import re
import csv
from misc import check_for_keys, errorpage, fix_html
from uuid import uuid4

# Ensures certain variables are always passed to render_template
def render_template(*args, **kwargs):
    return rt_default(*args, STUDENT_CONTACTS=STUDENT_CONTACTS, session=session, len=len, list=list, **kwargs)

# Autochecking functions
def check_for_rss_updates(name, mark_as_read=True):
    info = default_integrations.inputs.rss.get(name)
	# check if new version exists
    feed = feedparser.parse(info.url.val)
    if not latest_posts.has(name):  # For first-time runs
        if mark_as_read == True:
            latest_posts.set(name, feed['entries'][0])
        return feed['entries']  # We return the whole list
    check = 0
    while True:  # Iterate until finding the latest stored update
        if feed['entries'][check]['title'] == latest_posts.get(name).val['title']:  # The object is a FeedParserDict, so it won't be converted to a Node
            # ['title'] --- Just in case the post updates
            # no changes
            break
        else:
            check += 1
    if check == 0:
        return False
    else:
        if mark_as_read == True:
            latest_posts.set(name, feed['entries'][0])
        return feed['entries'][0:check]

def check_for_twitter_updates(name, mark_as_read=True):  # func will 'catch-up' to missed posts over time...
    info = default_integrations.inputs.twitter.get(name)
	# check if new version exists
    timeline = fetchtwitter.user(info.username.val)
    if not latest_posts.has(name):  # For first-time runs
        if mark_as_read == True:
            latest_posts.set(name, timeline[list(timeline.keys())[0]])  # Sets the latest post to the newest ID
        return timeline # We return the whole dictionary
    check = 0
    new = {}
    while True:  # Iterate until finding the latest stored update
        if timeline[list(timeline.keys())[0]]['conversation_id'] == latest_posts.get(name).conversation_id.val:
            # found last entry
            break
        else:
            check = 1  # check > 0 = there are new posts
            new[list(timeline.keys())[0]] = timeline[list(timeline.keys())[0]]  # Copies the value to the new posts list
            del timeline[list(timeline.keys())[0]]
    if check == 0:
        return False
    else:
        if mark_as_read == True:
            latest_posts.set(name, new[list(new.keys())[0]])
        return new

# Autochecking 2nd level functions
def pull_feeds():
    results = PYNDatabase({'rss': {}, 'twitter': {}})
    for integration in default_integrations.inputs.rss.values():  # pulls all rss feeds and saves results
        results.rss.set(integration, check_for_rss_updates(integration))
    for integration in default_integrations.inputs.twitter.values():  # pulls all twitter feeds and saves results
        results.twitter.set(integration, check_for_twitter_updates(integration))
    return results

def parse_feeds(results):  # Converts the returned posts into a unified format
    all_results = []
    for integration in results.rss.values():
        # if not posts.has(integration):  # First-run helper
        #     posts.set(integration, [])
        if results.rss.get(integration).val != False:
            for value in results.rss.get(integration).val:  # each value is a new post
                post = {
                    "title": value['title'],
                    "content": fix_html(value['summary']),  # Strips out any html tags and fixes non-breaking spaces
                    "link": value['links'][0]['href'],
                    "datetime": datetime.fromtimestamp(mktime(value['published_parsed'])),
                    "source": f"rss.{integration}",
                    "id": str(uuid4())
                }
                # posts.set(integration, posts.get(integration).val + [post])  # Appends this new post to the integration-sorted list
                all_results.append(post)  # Appends to the temporary list
                alert(integration, post)
    url = re.compile("https:\/\/(.*?)/..........")  # All urls will be t.co ones
    for integration in results.twitter.values():
        # if not posts.has(integration):  # First-run helper
        #     posts.set(integration, [])
        if results.twitter.get(integration).val != False:
            for value in results.twitter.get(integration).values():  # each value is a new post
                value = results.twitter.get(integration).get(value)
                urls = value.urls.val
                content = value.tweet.val
                date = value.date.val.split('-')
                time = value.time.val.split(':')
                dt = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
                for u in urls:  # Replaces t.co urls with real ones
                    content = url.sub(u, content, 1)
                post = {
                    "title": f"New Twitter update from {value.username.val}",
                    "content": content,
                    "link": value.link.val,
                    "datetime": dt,
                    "source": f"twitter.{integration}",
                    "id": str(uuid4())
                }
                all_results.append(post) # Appends this new post to the temporary list
                alert(integration, post)
    all_results = sorted(all_results, key=lambda d: d['datetime'])  # Sorts posts chronologically
    all_results.reverse()
    for result in all_results:
        posts.set(result['id'], result)  # Adds results to the list by id


# Autochecking 3rd level functions
def autograb():
    parse_feeds(pull_feeds())


# New post alerts
def alert(name, post):
    # Does nothing atm
    print(post['title'])


# Constants
PORT = 12345

# Object inits
default_integrations = PYNDatabase('integrations.json')
posts = PYNDatabase('db/posts.pyndb', autosave=True)
config = PYNDatabase('config.json', autosave=True)
latest_posts = PYNDatabase('db/latest.pyndb', autosave=True)
app = Flask(__name__)
with open('contacts.csv', mode='r') as inp:
    reader = csv.reader(inp)
    STUDENT_CONTACTS = {rows[30]:rows[0] for rows in reader}


# Testing ground
# ...


print('Hang tight, grabbing posts really quick...')
autograb()
print('Done!')

# Start background tasks
scheduler = BackgroundScheduler()
scheduler.add_job(func=autograb, trigger="interval", seconds=5*60)
scheduler.start()
# MAKE SURE THE EXIT STATEMENT IS ENABLED


""" MHS Updates API v1
    ------------------
  + Remember, all routes must return something 
    for Flask to forward to the client.

  + All routes must be added to VALID_ROUTES

  + Format for API methods:
    def method(self, request, *args)
    ------------------
    jvadair 2022
"""
API_KEY = config.api_key.val


VALID_ROUTES = (
    "SetCredentials",
    "Tea",
    "Login",
    "Logout",
    "SetPreferences",
    "ChangePassword"
)

class InvalidRoute(Exception):
    pass

class API:

    # --- Helper functions

    def __init__(self):
        pass

    def handle(self, route, request, *args):
        # print(VALID_ROUTES, route)
        if route in VALID_ROUTES:  # Prevents potential abuse of certain non-route functions
            return getattr(self, route)(request, *args)  # Forwards response back to Flask
        else:
            # raise InvalidRoute('The requested API path doesn\'t exist.')
            return 'The requested API path doesn\'t exist.', 404

    def handle_new_users(self, data):
        for item in data:
            if not path.exists('db/users/' + item[1]):
                if config.has('allowed_domains') and item[1].split('@')[1] not in config.allowed_domains.val:
                    pass
                else:
                    userdb = PYNDatabase('db/users/' + item[1], password=item[2])  # The user data is encrypted with their password
                    userdb.create('preferences')
                    userdb.save()

    # --- API routes

    def Tea(self, request, *args):
        return '', 418  # I'm a little teapot

    def SetCredentials(self, request, *args):
        data = request.json
        # Received data format:
        # List of lists, whose indexes are
        # 0: Timestamp
        # 1: Email Address
        # 2: Password
        headers = request.headers
        if headers.get('X-API-Key') == API_KEY:
            self.handle_new_users(data)
            return 'Success!'
        else:
            return 'Invalid API Key.', 401  # Unauthorized

    def Login(self, request, *args):
        data = dict(request.form)
        if not check_for_keys(data, 'email', 'password'):
            return 'Invalid response', 400  # Bad request
        if path.exists('db/users/' + data['email']):
            try:
                userdb = PYNDatabase('db/users/' + data['email'], password=data['password'])
                session['logged_in'] = True
                session['email'] = data['email']
                session['password'] = data['password']  # So that the user doesn't have to re-enter their password, but their data can remain encrypted.
                return redirect('/')
            except PYNDatabase.Universal.Error.InvalidPassword:
                return errorpage('Invalid password.')
        else:
            return errorpage('User not found.')
    
    def Logout(self, request, *args):
        if session.get('logged_in'):
            session['logged_in'] = False
            del session['email']
            del session['password']
            return redirect('/')
        else:
            return errorpage('You are not logged in.'), 401
    
    def SetPreferences(self, request, *args):
        if session.get('email'):
            userdb = PYNDatabase('db/users/' + session.get('email'), password=session.get('password'))
            data = dict(request.form)
            print(data)
            for pref in data.keys():
                userdb.preferences.set(pref, data[pref])
                return redirect('/account')
        else:
            return errorpage('You are not logged in.'), 401

    def ChangePassword(self, request, *args):
        if session.get('email'):
            try:
                data = dict(request.form)
                userdb = PYNDatabase('db/users/' + session.get('email'), password=data.get('old_password'))
                if data.get('new_password'):
                    userdb.password = data['new_password']
                    session['password'] = data['new_password']
                    userdb.save()
                    return redirect('/account')
                else:
                    return errorpage('You must enter a password.'), 400
            except PYNDatabase.Universal.Error.InvalidPassword:
                return errorpage('Invalid password.'), 401
        else:
            return errorpage('You are not logged in.'), 401

# Loads the API object
api = API()


# Flask routes
@app.before_request
def check_permissions():
    if request.path not in ('/', '/auth') and not session.get('logged_in'):
        if not request.path.startswith('/api') and not request.path.startswith('/static'):
            return redirect('/')

@app.route('/api/v1/<route>', methods=['POST'])
def call_api(route):
    return api.handle(route, request)

@app.route('/')
def index():
    return render_template('landing.html', posts=posts)

@app.route('/post/<post_id>/')
def send_post(post_id):
    return render_template('post.html', post=posts.get(post_id).val)

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/signup')
@app.route('/login')
@app.route('/register')
@app.route('/signin')
def auth_aliases():
    return redirect('/auth')

# Test routes
@app.route('/template/<template_name>')
def send_template(template_name):
    return render_template(template_name)


# Run
if __name__ == '__main__':
    app.secret_key = urandom(15)
    app.run(host='0.0.0.0', port=PORT, debug=False)

# Shut down the scheduler when exiting the ap
atexit.register(lambda: scheduler.shutdown())