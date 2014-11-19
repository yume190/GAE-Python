from google.appengine.api import users
import webapp2
import cgi
import threading
import time
from urllib2 import *
from google.appengine.ext import ndb
import datetime
import json
import re

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

class Fabric(ndb.Model):
    data = ndb.StringProperty()

class Test1(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World! Yume!!!  2 machine')

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

class Test6(webapp2.RequestHandler):
    def get(self):
        chapter = self.request.get('Chapter')
        if chapter == "":
            chapter = 0
        else:
            chapter = int(chapter) - 1

        self.response.headers['Content-Type'] = 'application/json'
        # self.response.write('{"Name":"Yume"}')
        # a=[1,2,3,4]
        url = "http://new.comicvip.com/show/cool-10130.html?ch=11"
        a=EightComic(url)

        b={}
        # b["Chapters"]=a.chapters
        # b["ItemId"]=a.itemId
        # b["Hash"]=a.hash
        # b["Pages"]=[]

        # for x in a.myParse:
        #     b["Pages"].append(x.getPages())

            # b["Pages"].append([x.chapter,x.sid,x.did,x.itemId,x.pages])

        b["Pages"] = a.myParse[chapter].getPages()

        self.response.write(json.dumps(b))

class Test7(webapp2.RequestHandler):
    def post(self):
        f = Fabric()
        f.data = self.request.get('verification')
        f.put()


class EightComicParse(object):
    """docstring for EightComicParse"""
    def __init__(self, arg,itemId):
        super(EightComicParse, self).__init__()
        self.hash = arg[-40:]
        numbers = re.findall(r'\d+',arg)
        self.chapter = int(numbers[0])
        self.sid = int(numbers[1]) / 10
        self.did = int(numbers[1]) % 10
        self.itemId = itemId
        self.pages = int(numbers[2][:2])

    def get(self,page):
        img = ""
        # if page >= 100:
        #     count = page % 100
        #     img = self.hash[3*(count%10)+count/10:3*(count%10)+3+count/10]
        # else:
        #     img = self.hash[3*(page%10)+page/10:3*(page%10)+3+page/10]
        p1 = (page + 0) % 10
        p2 = (page + 1)
        a=page
        img = self.hash[3*(a%10)+a/10:3*(a%10)+3+a/10]

        return "http://img%d.8comic.com/%d/%d/%d/%s_%s.jpg" % (self.sid, self.did, self.itemId, self.chapter, str(p2).zfill(3), img)

    def getPages(self):
        result = []
        for page in range(self.pages):
            result.append(self.get(page))
        return result

class EightComic:

    def __init__(self,url):

        patternChapters = r"var chs=[a-zA-Z0-9\']+"
        patternItemId = r"var ti=[a-zA-Z0-9\']+"
        patternhash = r"var cs=[a-zA-Z0-9\']+"
        baseUrl = "http://img7.8comic.com/"

        self.url = url
        r = urlopen(url).read()
        self.chapters = int(re.findall(patternChapters,r)[0].split("=")[1])
        self.itemId = int(re.findall(patternItemId,r)[0].split("=")[1])
        self.hash = re.findall(patternhash,r)[0].split("=")[1].split("'")[1]

        patternParse = r'[a-z]{1,2}\d+[a-z]\d{2}[a-z]\d{2}[a-z\d]{40}'
        hashs = re.findall(patternParse,self.hash)
        self.myParse = [EightComicParse(h,self.itemId) for h in hashs]

application = webapp2.WSGIApplication([
    ('/t1', Test1),
    ('/t2', Test2),
	('/t31', Test31),
    ('/t32', Test32),
    ('/t4', Test4),
    ('/t5', Test5),
    ('/t6', Test6),
    ('/t7', Test7),
], debug=True)
