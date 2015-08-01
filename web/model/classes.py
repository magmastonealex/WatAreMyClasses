"""
Model for a given class, storing time, date, instructor, class details, etc.
Returned by database.
Should probably be taken in by Database object during Quest import, but meh.
"""
class WaterlooClassTime:
	def __init__(self,ID,class_name,section,timestamp,timeend,instructor,Ctype,where):
		self.id=ID
		self.class_name=class_name
		self.section=section
		self.timestamp=timestamp
		self.timeend=timeend
		self.instructor=instructor
		self.type=Ctype
		self.where=where
