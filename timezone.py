from flask import Flask, render_template, request
from datetime import datetime, timedelta
import time
import pytz
from pytz import timezone
from timezonefinder import TimezoneFinder
from geopy import geocoders
gn = geocoders.GeoNames(username="paytonrodman")

Flask_App = Flask(__name__)

@Flask_App.route('/', methods=['GET'])
def index():
    """
    Displays index page
    """
    return render_template('index.html')

@Flask_App.route('/result/', methods=['POST'])
def result():
    """
    Sends information from form input
    """
    time_input = request.form['Time']
    from_input = request.form['From']
    to_input = request.form['To']
    date_input = request.form['Date']

    time_object = datetime.strptime(time_input, '%H:%M').time()
    date_object = datetime.strptime(date_input, '%Y-%m-%d').date()
    naive_datetime = datetime.combine(date_object, time_object) # datetime without timezone information

    tf = TimezoneFinder()

    try:
        from_loc = gn.geocode(from_input)
        from_TZname = tf.timezone_at(lng=from_loc.longitude, lat=from_loc.latitude)
        from_timezone = timezone(from_TZname)
        from_datetime = from_timezone.localize(naive_datetime) # add timezone information to input datetime
        from_date = "{:%d, %b %Y}".format(from_datetime.date())
        #from_time = time.strftime("{%I:%M %p}", from_datetime.time())
        from_time = datetime.strptime(str(from_datetime.time()), '%H:%M:%S')
        from_time = from_time.strftime('%I:%M %p')


        to_loc = gn.geocode(to_input)
        to_TZname = tf.timezone_at(lng=to_loc.longitude, lat=to_loc.latitude)

        # Convert meeting date/time between timezones
        to_datetime = from_datetime.astimezone(timezone(to_TZname))
        to_date = "{:%d, %b %Y}".format(to_datetime.date())
        #to_time = time.strftime("{%I:%M %p}", to_datetime.time())
        to_time = datetime.strptime(str(to_datetime.time()), '%H:%M:%S')
        to_time = to_time.strftime('%I:%M %p')

        return render_template(
                               'index.html',
                               FromDate=from_date,
                               FromTime=from_time,
                               FromLoc=from_input,
                               FromTZ=from_TZname,
                               ToDate=to_date,
                               ToTime=to_time,
                               ToLoc=to_input,
                               ToTZ=to_TZname,
                               success=True)

    except AttributeError:
        return render_template(
                'index.html',
                FromDate="Unknown",
                FromTime="Unknown",
                FromLoc=from_input,
                FromTZ="Unknown",
                ToDate="Unknown",
                ToTime="Unknown",
                ToLoc=to_input,
                ToTZ="Unknown",
                success=False,
                error="\"From\" place not found. Please try a larger city nearby.")




if __name__ == '__main__':
    Flask_App.debug = True
    Flask_App.run()
