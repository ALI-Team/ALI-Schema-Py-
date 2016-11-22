#!/usr/bin/python

import argparse
import json
import os
import sys
import urllib2
import datetime
import calendar

def school_select():
	
	os.system('cls' if os.name=='nt' else 'clear')	

        schools = json.loads(urllib2.urlopen("http://beontime.se/app/schools.json").read())

        regions = []

        for school in schools:
                if not school["region"] in regions:
                        regions.append(school["region"])

        for region in regions:
		print("("+str(regions.index(region))+") "+region)
		
	while True:
		try:
			curr_region = int(raw_input("Select region ? "))
		except ValueError:
			continue
		if curr_region < 0 or curr_region > len(regions):
			continue
		else:
			break

	os.system('cls' if os.name=='nt' else 'clear')

	cities = []

	for school in schools:
		if school["region"] == regions[curr_region]:
			if not school["stad"] in cities:
				cities.append(school["stad"])
       
	for city in cities:
		print("("+str(cities.index(city))+") "+city)

	while True:
		try:
			curr_city = int(raw_input("Select city ? "))
		except ValueError:
			continue
		if curr_city < 0 or curr_city > len(cities):
			continue
		else:
			break
	
	os.system('cls' if os.name=='nt' else 'clear')

	school_list = []

	for school in schools:
		if school["stad"] == cities[curr_city]:
			if not school["namn"] in school_list:
				school_list.append(school["namn"])

	for school_i in school_list:
		print("("+str(school_list.index(school_i))+") "+school_i)

	while True:	
		try:
			curr_school = int(raw_input("Select school ? "))
		except ValueError:
			continue
		if curr_school < 0 or curr_school > len(school_list):
			continue
		else:
			break

	for school in schools:
		if school["namn"] == school_list[curr_school]:
			if not os.path.exists(os.environ['HOME']+'/.ali'):
    				os.makedirs(os.environ['HOME']+'/.ali')

			try:
        			f = open(os.environ['HOME']+'/.ali/schema.ali', 'r')
				settings = json.loads(f.read())
				f.close()
        			f = open(os.environ['HOME']+'/.ali/schema.ali', 'w')
				settings["school"] = school["id"]
				f.write(json.dumps(settings))
				f.close()
			except IOError:
        			f = open(os.environ['HOME']+'/.ali/schema.ali', 'w')
        			f.write(json.dumps({"school":school["id"], "class":""}))
        			f.close()
        sys.exit(0)

	return

def class_select():

	n_class = raw_input("Enter your class ? ")

	if not os.path.exists(os.environ['HOME']+'/.ali'):
        	os.makedirs(os.environ['HOME']+'/.ali')

        try:
                f = open(os.environ['HOME']+'/.ali/schema.ali', 'r')
                settings = json.loads(f.read())
                f.close()
                f = open(os.environ['HOME']+'/.ali/schema.ali', 'w')
		settings["class"] = n_class
                f.write(json.dumps(settings))
                f.close()
        except IOError:
                f = open(os.environ['HOME']+'/.ali/schema.ali', 'w')
                f.write(json.dumps({"school":"", "class":n_class}))
                f.close()	

	sys.exit(0)

	return

def check_positive(value):
	try:
		ival = int(value)
	except ValueError:
		print("Invalid week")
		sys.exit(1)
	if ival <= 0 or ival > 52:
		print("Invalid week")
		sys.exit(1)
	else:
		return ival
	return

def check_day(value):

	try:
		ival = int(value)
	except ValueError:
		print("Invalid day")
		sys.exit(1)
	if ival <= 0 or ival > 5:
		print("Invalid day")
		sys.exit(1)
	else:
		return ival

	return

parser = argparse.ArgumentParser(description='Show NovaSoftware schedule')
parser.add_argument('--school', help='Specify school', action='store_true')
parser.add_argument('--class', help='Specify class', action='store_true')
parser.add_argument('--week', help='Specify week', type=check_positive)
parser.add_argument('--day', help='Specify day', type=check_day)
args = parser.parse_args()

if args.school:
	school_select()

if getattr(args, "class"):
	class_select()

if not os.path.exists(os.environ['HOME']+'/.ali'):
    os.makedirs(os.environ['HOME']+'/.ali')

try:
	f = open(os.environ['HOME']+'/.ali/schema.ali', 'r')
except IOError:
	f = open(os.environ['HOME']+'/.ali/schema.ali', 'w')
	f.write(json.dumps({"school":"", "class":""}))
	f.close()
finally:	
	settings = json.loads(f.read())
	week = datetime.datetime.now().isocalendar()[1]
	day = datetime.datetime.today().weekday()+1

	if not settings["school"]:
		print("Please specify your school with --school")
		sys.exit(1)
	if not settings["class"]:
		print("Please specify your class with --class")
		sys.exit(1)

	if args.week:
		week = args.week

	if args.day:
		day = args.day
	
	try:
		schedule = json.loads(urllib2.urlopen("https://jobb.matstoms.se/ali/api/getjson.php?week="+str(week)+"&scid="+settings["school"]+"&clid="+settings["class"]+"&getweek=0&day="+str(int(day))).read())
	except ValueError:
		print("Error loading schedule. Please check class and/or school")
		sys.exit(1)

	os.system('cls' if os.name=='nt' else 'clear')	
	
	print(calendar.day_name[day-1])
	print("=====================================")
	
	for lesson in schedule["lessons"]:
		print(lesson["start"]+" - "+lesson["end"])
		print(lesson["info"])
		print("=====================================")
