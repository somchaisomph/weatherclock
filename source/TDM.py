import pycurl
import io
import json
import datetime

# --  *** important note ***
# -- This code works only in Thailand --

class Forecaster():
	def __init__(self):
		self._token_="get your own token"
		
	def daily_box_area(self,box,start,end, domain=2):
		# end - start <= 3 days.
		if not (0 <= domain <= 3) :
			print('Specified domain does not exist, available are 0,1,2,3.')
			return None
		if not start :
			_start_= str(datetime.date.today())	
		else:
			_start_ = start
			
		_url_="https://data.tmd.go.th/nwpapi/v1/forecast/area/box?\
domain=2&bottom-left=13.10,100.10&top-right=13.20,100.20&fields=tc_max,rh&starttime=2017-08-23T15:00:00'"

		
	def daily_place(self,province,amphoe,days=7):
		if not (0 < days <= 126) :
			print('Number of duration of forecast must be in range [1,126] days.')
			return None

		_fields_='tc_min,tc_max,rh,psfc,swdown,cond,rain'		
		#_buffer_ = io.BytesIO()
		_date_= str(datetime.date.today())
		_url_='https://data.tmd.go.th/nwpapi/v1/forecast/location/daily/place?\
province={}&amphoe={}&fields={}&date={}&duration={}'.format(province,amphoe,_fields_,_date_,days)
		print(_url_)
		_data_ = self.cURL(_url_)
		_res_ = []
		if _data_ == [] : return _res_
		for fc in _data_:
			obj={}
			obj['time'] = self.parse_date(fc['time'])
			obj['rh']= fc['data']['rh']
			obj['tc_max']= fc['data']['tc_max']
			obj['tc_min'] = fc['data']['tc_min']
			obj['psfc']=fc['data']['psfc']
			obj['swdown']=fc['data']['swdown']
			obj['rain']=fc['data']['rain']
			obj['cond']=fc['data']['cond']
			_res_.append(obj)
		return _res_

	def daily_lat_lon(self,lat='13.8174113',lon='100.6409061',days=7):
		if not (0 < days <= 126) :
			print('Number of duration of forecast must be in range [1,126] days.')
			return None
		
		_fields_='tc_min,tc_max,rh,psfc,swdown,cond,rain'		
		#_buffer_ = io.BytesIO()
		_date_= str(datetime.date.today())
		_url_='https://data.tmd.go.th/nwpapi/v1/forecast/location/daily/at?\
lat={}&lon={}&fields={}&date={}&duration={}'.format(lat,lon,_fields_,_date_,days)
		#print(_url_)
		_data_ = self.cURL(_url_)
		_res_ = []
		if _data_ == [] : return _res_
		for fc in _data_:
			obj={}
			obj['time'] = self.parse_date(fc['time'])
			obj['data'] = {}
			obj['data']['rh']= fc['data']['rh']
			obj['data']['tc_max']= fc['data']['tc_max']
			obj['data']['tc_min'] = fc['data']['tc_min']
			obj['data']['psfc']=fc['data']['psfc']
			obj['data']['swdown']=fc['data']['swdown']
			obj['data']['rain']=fc['data']['rain']
			obj['data']['cond']=fc['data']['cond']
			_res_.append(obj)
		return _res_
		
	def hourly_lat_lon(self,lat='13.82',lon='100.64',steps=1):
		if not (0 < steps <= 48) :
			print('Number of duration must be in range [1,48] hours.')
			return None
		
		_fields_='tc,rh,cond,rain,ws10m'		
		_now_= datetime.datetime.now()
		_date_ ="{}-{:02d}-{:02d}".format(_now_.year,_now_.month,_now_.day)
		_hr_ = _now_.hour
		_url_='https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at?\
lat={}&lon={}&fields={}&date={}&hour={}&duration={}'.format(lat,lon,_fields_,_date_,_hr_,steps)
		#print(_url_)

		_data_ = self.cURL(_url_)
		_res_ = []
		if _data_ == [] : return []
		for fc in _data_:
			rec={}
			rec['time'] = self.parse_date(fc['time'])
			rec['data'] = {}
			rec['data']['rh']= fc['data']['rh']
			rec['data']['tc']= fc['data']['tc']
			rec['data']['ws10m']= fc['data']['ws10m']
			rec['data']['rain']=fc['data']['rain']
			rec['data']['cond']=fc['data']['cond']
			_res_.append(rec)
		return _res_	
		
	def parse_date(self,ds):
		_date , _time = ds.split("T")
		y,mt,d = _date.split('-')
		_hms,_ = _time.split("+")
		h,m,s = _hms.split(":")
		return (y,mt,d,h,m,s)
		
	def wm2_uvi(self,wm2):
		return wm2/25.0
		
	def cURL(self,url):
		_buffer_ = io.BytesIO()
		c = pycurl.Curl()
		c.setopt(pycurl.WRITEDATA, _buffer_)
		c.setopt(pycurl.URL,url)
		c.setopt(pycurl.HTTPHEADER, ['authorization: Bearer {}'.format(self._token_),'Accept: application/json'])
		c.perform()
		c.close()
		_json_ = json.loads(_buffer_.getvalue())
		try:
			_data_ = _json_['WeatherForecasts'][0]["forecasts"]
		except:
			_data_ = []
		return _data_

	
			
	
