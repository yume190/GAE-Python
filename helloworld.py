from google.appengine.api import users
import webapp2
import cgi
import threading
import time
#import requests
from urllib2 import *
from google.appengine.ext import ndb
import datetime
import json

# class MyThread (threading.Thread):
#     def __init__(self,url,jsonText):
#         threading.Thread.__init__(self)
#         self.url = url
#         self.jsonText = jsonText

#     def run(self):
#         while True:
#             self.jsonText = urlopen(self.url).read()
#             time.sleep(10)

jsonText = "123"
url = 'http://117.56.62.20:8080/LCDForwardAgent/config?IStopID=11734'
# myThread = MyThread(url,jsonText)
# myThread.start()

# url = 'http://117.56.62.20:8080/LCDForwardAgent/config?IStopID=11734'
# a = urlopen(url).read()
# r = requests.get('http://117.56.62.20:8080/LCDForwardAgent/config?IStopID=11735')

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/t32" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
  </body>
</html>
"""

def bus_key(guestbook_name="yume"):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)

class Bus(ndb.Model):
    """Models an individual Guestbook entry."""
    # author = ndb.UserProperty()
    # content = ndb.StringProperty(indexed=False)
    # date = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty()

class Test1(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World! Yume!!!')

class Test2(webapp2.RequestHandler):

    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Test31(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

class Test32(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

class Test4(webapp2.RequestHandler):
    def get(self):
        #url = 'http://117.56.62.20:8080/LCDForwardAgent/config?IStopID=11735'
        #b = urlopen(url).read()
        # self.response.headers['Content-Type'] = 'application/json'
        # jsonText += " o "
        # self.response.write(jsonText)

        bus_query = Bus.query(ancestor=bus_key('yume')).order(-Bus.date)
        buses = bus_query.fetch(5)

        output = "Yume Say : <br>"
        for bus in buses:
            # content = json.loads(bus.content)
            # content[u"Y"] = u"D"
            # output += str(bus.date) + " : " + json.dumps(content) + "<br>"
            output += str(bus.date) + " : " + bus.content + "<br>"
        self.response.write(output)

class Test5(webapp2.RequestHandler):
    def get(self):
        url = 'http://117.56.62.20:8080/LCDForwardAgent/config?IStopID=11734'
        jsonText = ""
        jsonText = urlopen(url).read()

        currentTime = datetime.datetime.now()
        strCurrentTime = str(currentTime)

        bus = Bus(parent=bus_key("yume"))
        # bus.content = strCurrentTime + " " +jsonText
        bus.content = jsonText
        bus.date = datetime.datetime.now() + datetime.timedelta(hours=8)
        bus.put()

application = webapp2.WSGIApplication([
    ('/t1', Test1),
    ('/t2', Test2),
	('/t31', Test31),
    ('/t32', Test32),
    ('/t4', Test4),
    ('/t5', Test5),
], debug=True)
