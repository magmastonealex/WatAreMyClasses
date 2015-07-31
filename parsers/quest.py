class Quest:
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
							timestamp="to_timestamp('"+a.replace(" ","")+" "+start.replace(" ","")+"', 'dd/mm/yyyy hh24:mi')"
							timestamp_end="to_timestamp('"+a.replace(" ","")+" "+end.replace(" ","")+"', 'dd/mm/yyyy hh24:mi')"
						else:
							timestamp="to_timestamp('"+a.replace(" ","")+" "+start.replace(" ","")+"', 'dd/mm/yyyy hh24:mi')"
							timestamp_end="to_timestamp('"+a.replace(" ","")+" "+end.replace(" ","")+"', 'dd/mm/yyyy hh24:mi')"
						ins=ins+"INSERT INTO timetable (uname,building,time,time_end,cls,sec,typ,prof) VALUES('','"+scheditem[1]+"',"+timestamp+","+timestamp_end+",'"+name+"','"+section+"','"+typ+"','"+scheditem[2]+"');" #prof
					else:
						pass
						#more work...
