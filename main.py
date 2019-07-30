import jinja2
import webapp2
from google.appengine.api import users
import os
import models

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HomePage(webapp2.RequestHandler):
    def get(self):
        result_template = the_jinja_env.get_template('templates/mainpage.html')
        search_data={}
        self.response.write(result_template.render(search_data))
    def post(self):
        result_template = the_jinja_env.get_template('templates/mainpage.html')
        search_data={}
        self.response.write(result_template.render(search_data))

class ResultsPage(webapp2.RequestHandler):
    def post(self):
        result_template = the_jinja_env.get_template('templates/resultpage.html')
        age = self.request.get("age")
        mode_of_transportation = self.request.get("mode of travel")
        range = self.request.get("distance")
        data = search(age=age,mode_of_transportation=mode_of_transportation,range=range)
        search.put()
        search_data = {
            "age": age,
            "transportation": mode_of_transportation,
            "range": range
        }
        self.response.write(result_template.render(search_data))

class SignPage(webapp2.RequestHandler):
    def get(self):
      result_template = the_jinja_env.get_template('templates/sign_up.html')
      user = users.get_current_user()
      # self.response.write(result_template.render())
      if user:
          email_address = user.nickname()
          # Generate a sign out link - this does it all in one line.
          logout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/'))
          # Show that sign out link on screen:
          self.response.write(
          "You're logged in as " + email_address + "<br>" + logout_link_html)
      else:
          # This line creates a URL to log in with your Google Credentials.
          login_url = users.create_login_url('/')
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          self.response.write('Please log in.<br>' + login_html_element)
      #     # This line uses string templating to create an anchor (link) element.
      #     login_html_element = '<a href="%s">Sign in</a>' % login_url
      #     # This line puts that URL on screen in a clickable anchor elememt.
      #     self.response.write('Please log in.<b>' + login_html_element)


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/results', ResultsPage), #this maps the root url to the Main Page Handler
    ('/signup', SignPage),
], debug=True)
