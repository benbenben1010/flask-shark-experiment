#{{{ imports
import flask
from flask import Flask
import json
import time
#}}}

#{{{ setup
app = Flask(__name__)
meetings_filename = "/home/ben/dev/cloudrooms/meetings.json"
#}}}

#{{{ /rooms  get_meetings_for_all_rooms()
@app.route('/rooms')
def get_meetings_for_all_rooms():
  rooms = _get_meeting_times_from_json_file()
  return flask.jsonify(rooms)
#}}}

#{{{ /rooms/<room_name  get_meetings for room(room_name)
@app.route('/rooms/<room_name>')
def get_meetings_for_room(room_name):
  rooms = _get_meeting_times_from_json_file()
  for room in rooms['rooms']:
    if room['name'] == room_name:
      return flask.jsonify(room)
  return "Room \"%s\" not found" % room_name
#}}}

#{{{ /rooms-display  display_meetings_for_all_rooms()
@app.route('/rooms-display')
def display_meetings_for_all_rooms():
  rooms = _get_meeting_times_from_json_file()
  displayable = {}
  for room in rooms['rooms']:
    to_add = {}
    #to_add['room_name'] = room['name']
    to_add['cur_status'] = room['current_meeting']['status']
    if to_add['cur_status'] == 'Occupied':
      to_add['cur_subject'] = room['current_meeting']['subject']
      to_add['cur_date'] = _formatted_time_date(room['current_meeting']['start'])
      to_add['cur_start'] = _formatted_time_hours(room['current_meeting']['start'])
      to_add['cur_end'] = _formatted_time_hours(room['current_meeting']['end'])

    to_add['next_status'] = room['next_meeting']['status']
    if to_add['next_status'] == 'Occupied':
      to_add['next_subject'] = room['next_meeting']['subject']
      to_add['next_date'] = _formatted_time_date(room['next_meeting']['start'])
      to_add['next_start'] = _formatted_time_hours(room['next_meeting']['start'])
      to_add['next_end'] = _formatted_time_hours(room['next_meeting']['end'])
    #displayable.append(to_add)
    displayable[room['name']] = to_add
  return flask.render_template('rooms.html', rooms=displayable)
#}}}

#{{{ /rooms-display/<room_name>  display_meetings_for_room(room_name)
@app.route('/rooms-display/<room_name>')
def display_meetings_for_room(room_name):
  rooms = _get_meeting_times_from_json_file()
  displayable = {}
  for room in rooms['rooms']:
    if not room['name'] == room_name:
      continue
    to_add = {}
    to_add['cur_status'] = room['current_meeting']['status']
    if to_add['cur_status'] == 'Occupied':
      to_add['cur_subject'] = room['current_meeting']['subject']
      to_add['cur_date'] = _formatted_time_date(room['current_meeting']['start'])
      to_add['cur_start'] = _formatted_time_hours(room['current_meeting']['start'])
      to_add['cur_end'] = _formatted_time_hours(room['current_meeting']['end'])

    to_add['next_status'] = room['next_meeting']['status']
    if to_add['next_status'] == 'Occupied':
      to_add['next_subject'] = room['next_meeting']['subject']
      to_add['next_date'] = _formatted_time_date(room['next_meeting']['start'])
      to_add['next_start'] = _formatted_time_hours(room['next_meeting']['start'])
      to_add['next_end'] = _formatted_time_hours(room['next_meeting']['end'])
    displayable[room['name']] = to_add
    return flask.render_template('rooms.html', rooms=displayable)
  return "Room \"%s\" not found" % room_name
#}}}

#{{{ _get_meeting_times_from_json_file()
def _get_meeting_times_from_json_file():
  fd = open(meetings_filename, 'r')
  json_str = fd.readline()
  return json.loads(json_str)
#}}}

#{{{ _formatted_time(seconds)
def _formatted_time_date(seconds):
  time_dict = time.localtime(seconds)
  return time.strftime("%a, %m/%d/%Y", time_dict)
#}}}

#{{{ _formatted_time_short(seconds)
def _formatted_time_hours(seconds):
  time_dict = time.localtime(seconds)
  return time.strftime("%I:%M%p", time_dict)
#}}}

#{{{ /test/<name>  test_temp(name)  TESTING_ONLY
@app.route('/test/<name>')
def test_temp(name):
  rooms = {'key1':'val1', 'key2' : 'val2'}
  return flask.render_template('test.html', name=rooms)
#}}}

#{{{ main
if __name__ == '__main__':
  app.debug = True
  app.run()
#}}}
