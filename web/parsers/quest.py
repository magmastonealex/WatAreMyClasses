import datetime
from db import Database
class Quest:
	def __init__(self,db):
		self.db=db;
	def getSched(self,inp):
		ins=""
		inp=inp.split("Select Display Option")[1]
		almostclasses=inp.split("Class Nbr	Section	Component	Days & Times	Room	Instructor	Start/End Date")
		classes=[]
		skip=1
		for clas in almostclasses:
			if skip==1:
				skip=0
				continue
			prevclass=almostclasses[almostclasses.index(clas)-1]
			class_data={}
			class_data["name"]=prevclass.splitlines()[-6]
			scheditems=clas.splitlines()
			#print scheditems
			schedset=zip(*(iter(scheditems[1:]),) * 7)
			#print schedset
	
			scheddata=[]
			schedcur={}
			fst=1
			for it in schedset:
				if it[0]=="Exam Information":
					scheddata.append(schedcur)
					break
				if it[0] != " ":
					print "new cls + "+it[0]
					if fst != 1:
						scheddata.append(schedcur)
					else:
						fst=0
					schedcur={"cnum":it[0],"section":it[1],"type":it[2],"sched":[[it[3],it[4],it[5],it[6]]]}
				else:
					schedcur["sched"].append([it[3],it[4],it[5],it[6]])
			class_data["sched"]=scheddata
			classes.append(class_data)
			#print classes
		for clas in classes:
			name=clas["name"]
			for it in clas["sched"]:
				typ=it["type"]
				section=it["section"]
				for scheditem in it["sched"]:
					a,b=scheditem[3].split("-")
	
					if a.replace(" ","")==b.replace(" ",""):
						#one class
						start,end=scheditem[0][1:].split("-")
						
						if start.find("AM") != -1 or start.find("PM") != -1:
							if start.find("AM") != -1:
								start.replace("AM","").replace(" ","")
							elif start.find("PM") != -1:
								start.replace("PM","").replace(" ","")
								h,m=start.split(":")
								start=str(int(h)+12)+":"
	
							if end.find("AM") != -1:
								end.replace("AM","").replace(" ","")
							elif end.find("PM") != -1:
								end.replace("PM","").replace(" ","")
								h,m=end.split(":")
								end=str(int(h)+12)+":"+m
							timestamp="to_timestamp('"+a.replace(" ","")+" "+start.replace(" ","").replace("h","")+"', 'dd/mm/yyyy hh24:mi')"
							timestamp_end="to_timestamp('"+a.replace(" ","")+" "+end.replace(" ","").replace("h","")+"', 'dd/mm/yyyy hh24:mi')"
						else:
							timestamp="to_timestamp('"+a.replace(" ","")+" "+start.replace(" ","").replace("h","")+"', 'dd/mm/yyyy hh24:mi')"
							timestamp_end="to_timestamp('"+a.replace(" ","")+" "+end.replace(" ","").replace("h","")+"', 'dd/mm/yyyy hh24:mi')"
						self.db.run_sql("INSERT INTO timetable (uname,building,time,time_end,cls,sec,tpe,prof) VALUES('','"+scheditem[1]+"',"+timestamp+","+timestamp_end+",'"+name+"','"+section+"','"+typ+"','"+scheditem[2]+"');") #prof
					else:
						print typ+" "+name
						#start date is on Monday (of term!), end date is on Friday.
						if scheditem[0] != "TBA":
							dow,start,sep,end=scheditem[0].split(" ") # times.
							print dow
							days=[]
							for c in dow:
								if c.islower():
									days[-1]="Th"
								else:
									days.append(c)
							print days
							a,b=scheditem[3].split("-")
							class_times=[]
							a=a.replace(" ","")
							b=b.replace(" ","")
							termmonday=datetime.datetime.strptime(a,"%d/%m/%Y")
							termend=datetime.datetime.strptime(b,"%d/%m/%Y")
							for day in days:
								#find first
								dayclass=None
								setclass=None
								if day=="M":
									dayclass=termmonday
								elif day=="T":
									dayclass=termmonday+ datetime.timedelta(days=1)
								elif day=="W":
									dayclass=termmonday+ datetime.timedelta(days=2)
								elif day=="Th":
									dayclass=termmonday+ datetime.timedelta(days=3)						
								elif day=="F":
									dayclass=termmonday+ datetime.timedelta(days=4)
								#class_times.append(dayclass)
								setclass=dayclass
								while True:
									if setclass.month > termend.month or ( setclass.day > termend.day and setclass.month == termend.month):
										print "Finished"
										break
									class_times.append(setclass)
									setclass=setclass+ datetime.timedelta(days=7) # week from class
							if start.find("AM") != -1 or start.find("PM") != -1:
								if start.find("AM") != -1:
									start.replace("AM","").replace(" ","")
								elif start.find("PM") != -1:
									start.replace("PM","").replace(" ","")
									h,m=start.split(":")
									start=str(int(h)+12)+":"
		
								if end.find("AM") != -1:
									end.replace("AM","").replace(" ","")
								elif end.find("PM") != -1:
									end.replace("PM","").replace(" ","")
									h,m=end.split(":")
									end=str(int(h)+12)+":"+m
							for time in class_times:
								timestamp="to_timestamp('"+time.strftime("%d-%m-%Y")+" "+start.replace(" ","").replace("h","")+"', 'dd/mm/yyyy hh24:mi')"
								timestamp_end="to_timestamp('"+time.strftime("%d-%m-%Y")+" "+end.replace(" ","").replace("h","")+"', 'dd/mm/yyyy hh24:mi')"
								self.db.run_sql("INSERT INTO timetable (uname,building,time,time_end,cls,sec,tpe,prof) VALUES('','"+scheditem[1]+"',"+timestamp+","+timestamp_end+",'"+name+"','"+section+"','"+typ+"','"+scheditem[2]+"');") #prof

							#more work..
		return ins