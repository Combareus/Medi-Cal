"""
Classes for scheduling, employees (including surgeons, cleaner), patients
Progress: 
1/24/2024 - Classes for people created and initialized Lines: 180
1/30/2024 - Classes for schedule created, some validation done Lines: 309
2/06/2024 - Occupy and Conflict functions created Lines: 385]
"""

class Schedule():
	def __init__(self, year, month, day, hour, minute):
		"""
		Initializes class
		Attributes
			year (int)
			month (int)
			day (int)
			hour (int)
			minute (int)
		"""
		self._year = year
		self._month = month
		self._day = day
		self._hour = hour
		self._minute = minute

		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.minute = minute

	@property
	def year(self):
		"""Getter for year"""
		return self._year

	@property
	def month(self):
		"""Getter for month"""
		return self._month

	@property
	def day(self):
		"""Getter for day"""
		return self._day

	@property
	def hour(self):
		"""Getter for hour"""
		return self._hour

	@property
	def minute(self):
		"""Getter for minute"""
		return self._minute

	@year.setter
	def year(self, year):
		"""
		Setter for year
		Attributes
				self (schedule)
				year (int)
		"""
		while not year.isdigit():
			self.raiseerror()
		self._year = int(year)

	@month.setter
	def month(self, month):
		"""
		Setter for month
		Attributes
				self (schedule)
				month (int)
		"""
		while not month.isdigit() or month < 1 or month > 12:
			self.raiseerror()
		self._month = month

	@day.setter
	def day(self, day, month, year):
		"""
		Setter for day
		Attributes
				self (schedule)
				day (int)
				month (int)
				year (int)
		"""
		if not day.isdigit() or day < 1 or day > 31:
			self.raiseerror()
		elif month not in [1, 3, 5, 7, 8, 10, 12] and day == 31:
			self.raiseerror()
		elif month == 2 and day == 30:
			self.raiseerror()
		if day == 29 and month == 2:
			if year % 4 == 0:
				if year % 400 == 0:
					pass
				elif year % 100 == 0:
					self.raiseerror()
			else:
				self.raiseerror()
		self._day = day

	@hour.setter
	def hour(self, hour):
		"""
		Setter for hour
		Attributes
				self (schedule)
				hour (int)
		"""
		if not hour.isdigit() or hour < 0 or hour > 23:
			self.raiseerror()
		self._hour = hour

	@minute.setter
	def minute(self, minute):
		"""
		Setter for minute
		Attributes
				self (schedule)
				minute (int)
		"""
		if not minute.isdigit() or minute < 0 or minute > 59:
			self.raiseerror()
		self._minute = minute

	def raiseerror(self):
		"""
		Raises an error in case of an incorrect input
		"""
		#this is left purposely blank until the display is created
		return True


class Employee():
	def __init__(self, fullName, availability, assignments):
		"""
		Initializes class
		Attributes
			fullName (str): fullname of person
			Availability (2d lists with ints) - [[yearstart, month of start, day of start, hour of start, minute of start, yearend, monthend, dayend, hourend, minuteend], ...] - their availability based off of time of day, hours available, and day of week
			Assignments (2d lists with ints) - [[yearstart, month of start, day of start, hour of start, minute of start, yearend, monthend, dayend, hourend, minuteend], ...] - their assignments
		"""
		self._fullName = fullName
		self._availability = availability
		self._assignments = assignments

		self.fullName = fullName
		self.availability = availability
		self.assignments = assignments

	@property 
	def fullName(self):
		"""Getter for fullName"""
		return self._fullName

	@property 
	def availability(self):
		"""Getter for availability"""
		return self._availability

	@property 
	def assginments(self):
		"""Getter for availability"""
		return self._assignments

	@fullName.setter
	def fullName(self, n):
		"""
		Setter for fullName
		Attributes
				self (person)
				n (str) - name that needs validation
		"""
		while not (isinstance(n, str) and len(n) > 0):
				n = input("Invalid name, try again: ")
		self._fullName = n

	@availability.setter
	def availability(self, avail):
		"""
		Setter for availability
		Attributes
				self (person)
				avail (2d list)
		"""
		self._availability = avail

	@assignments.setter
	def assignments(self, assign):
		"""
		Setter for availability
		Attributes
				self (person)
				avail (2d list)
		"""
		self._assignments = assign
		
	def conflict(self, timestart, timeend):
		"""
		Determines if employee is available from timestart to timeend
		Attributes
			Self (person)
			timestart (1d list of ints: [year, month, day, hour, minute])
			timeend (1d list of ints: [year, month, day, hour, minute])

		Returns
			False - There is a conflict
			index - index of availability in self._availability 
		"""
		for x in self._availability:
			#if the day of the conflict is less than the day of we're checking, break (availability is ordered (i hope))
			if timestart[2] < x[2]:
				break
				
			#if the start of shift is less than the start of assignment
			if timestart[0] >= x[0] and timestart[1] >= x[1] and timestart[2] >= x[2] and timestart[3] >= x[3] and timestart[4] >= x[4]:

				#if the end of the assignment is less than the end of shift
				if timeend[0] <= x[5] and timeend[1] <= x[6] and timeend[2] <= x[7] and timeend[3] <= x[8] and timeend[4] <= x[9]:
					
					#we found an open slot
					return self._availability.index(x)
		return False
		
	def assign(self, timestart, timeend):
		"""
		Give assignment to person and change their availability and assignments
		Attributes
			Self (person)
			timestart (1d list of ints) - start of assignment
			timeend (1d list of ints) - end of assignment

		Returns
			True - Operation could be done
			False - Operation could not be done
		"""
		#store res of the conflict operation
		res = self.conflict(timestart, timeend)
		if res == -1:
			#Assignment could not be assigned
			return False
		else:
			#create a new timeslot for them
			temp = []
			for x in range(5):
				temp.append(timeend[x])
			for x in range(5, 10):
				temp.append(self._availability[res][x])
				#change the available timeslot so they are unavailable at that time
				self._availability[res][x] = timestart[x-5]
			#add temp to availability
			self._availability.insert(res+1, temp)
			
			return True

class Surgeon(Employee):
	def __init__(self, fullName, availability, assignments, qualifications, exp):
		"""
		Initializes class
		Attributes
			fullName (str): fullname of person
			availability (2d list of ints): availability of surgeon
			Qualifications (list of strings): list of genre of surgeries surgeon can perform
			exp (str): Senior or Junior ("Sr" or "Jr")
		"""
		super().__init__(fullName, availability, assignments)
		self._qualifications = qualifications
		self._exp = exp

		self.qualifications = qualifications
		self.exp = exp

	@property
	def qualifications(self):
		"""Getter for qualifications"""
		return self._qualifications

	@property
	def exp(self):
		"""Getter for exp"""
		return self._exp

	@qualifications.setter
	def qualifications(self, quals):
		"""
		Setter for qualifications
		Attributes
			self (Surgeon)
			qual (list)
		"""
		self._qualifications = quals

	@exp.setter
	def exp(self, title):
		"""
		Setter for exp
		Attributes
			self (surgeon)
			title (str)
		"""
		while title != "Jr" and title != "Sr":
			title = input("Invalid experience level, type Sr or Jr")
		self.exp = title

	def qualcheck(self, type, title):
		if title == "Sr":
			if self._exp == "Jr":
				return False
		if type not in self._qualifications:
			return False
		return True

		
	def assignsurgeon(self, type, title, timestart, timeend):
		"""
		Give assignment to surgeon and change their availability and assignments
		Note: This is DIFFERENT than assigning a regular employee
		Attributes
			Self (surgeon)
			type - Surgery type
			title - title required (jr or sr)
			timestart (1d list of ints) - start of assignment
			timeend (1d list of ints) - end of assignment

		Returns
			True - Operation could be done
			False - Operation could not be done
		"""
		#if the surgeon does not have the necessary credentials
		if self.qualcheck(self, type, title) == False:
			return False
		else:
			#otherwise assign - this doesnt necessarily return True, if there is a conflict it will return False in self.conflict()
			self.assign(self, timestart, timeend)
			return True

class Cleaner(Employee):
	def __init__(self, fullName, availability, assignments):
		"""
		Initializes class
		Attributes
			fullName (str): fullname of person
			Availability (2d lists with ints) - [[day of week, start of availability, hours available], ...] - their availability based off of time of day, hours available, and day of week

		"""
		super().__init__(fullName, availability, assignments)

class Patient():
	def __init__(self, fullName, conditionType, severity):
		"""
		Initializes class
		Attributes
			fullName (str): fullname of person
			conditionType (str): type of surgery needed
			severity (int): severity on a scale of 1 to 100
		"""
		self._fullName = fullName
		self._conditionType = conditionType
		self._severity = severity

		self.fullName = fullName
		self.conditionType = conditionType
		self.severity = severity

	
	@property 
	def fullName(self):
		"""Getter for fullName"""
		return self._fullName

	@property
	def conditionType(self):
		"""Getter for conditionType"""
		return self._conditionType

	@property
	def severity(self):
		"""Getter for severity"""
		return self._severity

	@fullName.setter
	def fullName(self, n):
		"""
		Setter for fullName
		Attributes
			self (person)
			n (str) - name that needs validation
		"""
		while not (isinstance(n, str) and len(n) > 0):
				n = input("Invalid name, try again: ")
		self._fullName = n

	@conditionType.setter
	def conditionType(self, type):
		"""
		Setter for conditionType
		Attributes
			self (patient)
			type (str)
	"""
		self._conditionType = type

	@severity.setter
	def severity(self, n):
		"""
		Setter for severity
		Attributes
			self (patient)
			n (int)
		"""
		self._severity = n
