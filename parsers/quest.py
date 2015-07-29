import re
def uw_waterloo_quest_schedule(input):
	arr_days={'m':"MO",'t':"TU","w":"WE","h":"TH","f":"FR","s":"SA","u":"SU"}
	arr_num_days={'m':1,"t":2,"w":3,"h":4,"f":5,'s':6,"u":7}

	code=""
	name=""
	section=""
	typ=""
	days=""
	time_start=""
	time_end=""
	location=""
	prof=""
	date_start=""
	date_end=""

	ical_array=[]
	js_array=[]
	pos=0
	total_length=len(input)
	swap=True

	while pos < total_length and pos >=0:
		found=False
		ampm=False

		if re.match('/(AM)|(PM)/', ) != None:
			pass