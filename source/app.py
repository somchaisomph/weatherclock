import sys
import datetime
from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from TMD import Forecaster
import clock_app_layout as cl

# -- variables
_cond_ = {1:'clear.png',2:'partly_cloudy.png',3:'cloudy.png',4:'overcast.png',5:'light_rain.png',6:'moderate_rain.png',
7:'heavy_rain.png',8:'thunderstorm.png',9:'very _old.png',10:'cold.png',11:'cool.png',12:'very_hot.png'}
_month_=['','January','Febuary','March','April','May','June','July','August','September','October','November','December']
_weekday_=['Monday','Tueday','Wednesday','Thursday','Friday','Saturday','Sunday']

_lat_ = '' # latitude of your place
_lon_ = '' # longitude of your place

_today_ = datetime.datetime.now()
_step_ = 24 - _today_.hour

# -- get daily forecast
_forecast_= Forecaster().hourly_lat_lon(lat=_lat_,lon=_lon_,steps=_step_)

# ---------------------------------------------------------------------	
# -- app and server 

ext_css = ['https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/0.0.0-359252c/base.min.css',
'https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/0.0.0-359252c/components.min.css',
'https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/0.0.0-359252c/utilities.min.css']
app = dash.Dash(__name__, external_stylesheets=ext_css)
server = app.server

# ---------------------------------------------------------------------	
# -- routing
@server.route("/css/<path:filename>")
def get_css(filename):
	return send_from_directory('./css', filename)

@server.route('/image/<path:filename>')
def get_images(filename):
	return send_from_directory('./images', filename)

# ---------------------------------------------------------------------
# callback

@app.callback(Output('time-div', 'children'),
              Input('clock-interval', 'n_intervals'))
def update_clock(n):
	d = datetime.datetime.now()
	return "{:02d}:{:02d}:{:02d}".format(d.hour,d.minute,d.second)             
              
@app.callback([Output('week-div', 'children'),
               Output('month-div', 'children'),
               Output('year-div', 'children')],
              Input('date-interval', 'n_intervals'))
def update_date(n):
	d = _today_
	wd = _weekday_[d.weekday()]
	dm = "{:02d} {}".format(d.day,_month_[d.month])
	
	return [wd,dm,str(d.year)]             


@app.callback([
               Output('tmp-val', 'children'),
               Output('humid-val', 'children'),
               Output('rain-val', 'children'),
               Output('wind-val', 'children'),
               Output('cond-img','src')
              ],
              Input('weather-interval', 'n_intervals'))
def update_weather(n):
	_now = datetime.datetime.now()
	done = False
	found = None
	for x in _forecast_:
		_y = int(x['time'][0])
		_m = int(x['time'][1])
		_d = int(x['time'][2])
		_h = int(x['time'][3])
		if (_now.year == _y) and (_now.month == _m) and (_now.day == _d) and  ( _now.hour == _h) :
			done = True
			found = x
		if done :
			break
	if found :
		return [found['data']['tc'],found['data']['rh'],found['data']['rain'],found['data']['ws10m'],'image/{}'.format(_cond_[found['data']['cond']])]
	else :
		return ['','','','','']
	
	
	         
# ---------------------------------------------------------------------
# -- web component

app.layout = html.Div(id='main-div',
					children=[
						dcc.Interval(
							id='clock-interval',
							interval=1*1000, # in  1000 milliseconds
							n_intervals=0
						),
						dcc.Interval(
							id='date-interval',
							interval=60*60*1*1000, # in  one hour
							n_intervals=0
						),
						
						dcc.Interval(
							id='weather-interval',
							interval=2*1000, # in  one hour
							n_intervals=0
						),
						cl.layout # clock layout
						])
			
# ---------------------------------------------------------------------
def run_on_desktop():
	import webview
	try:
		webview.create_window('Weather Clock', server,fullscreen=False)
		webview.start(debug=True)
	except:
		print('Something went wrong !!!')
		raise

def run_as_webserver():
	try:
		app.run_server('0.0.0.0',debug=True)
	except:
		print('Something went wrong !!!')
		raise
	

if __name__ == '__main__':
	args = sys.argv
	if len(args) < 2 :
		run_as_webserver()
	elif args[1] in ['web','desktop']:
		if  args[1]=='desktop':
			run_on_desktop()
		else:
			run_as_webserver()
	else :
		run_as_webserver()
