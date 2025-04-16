#!/usr/bin/env python3

# note the absolute home directory paths below /home/pi and update them before using!

from datetime import datetime, date, timedelta
import os, re, psutil, caldav

calendarurl="/caldav.php/username/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/"
caldav_url = 'https://calendar.server.url.com/'
username = 'obsstudio'
password = 'USE_SECURE_PASSWORD_HERE'

prestreamtime = timedelta(minutes=30)
poststreamtime = timedelta(minutes=15)
rightnow = datetime.now()
later = rightnow + prestreamtime
earlier = rightnow - poststreamtime

def checkprocessrunning(procname):
	isprocessrunning = False
	for proc in psutil.process_iter(['name']):
		# print(proc.info['name'])
		if procname == proc.info['name']:
			isprocessrunning = True
	return isprocessrunning

def checkprocessrunningwithopt(procname, optstr):
	isprocessrunning = False
	for proc in psutil.process_iter(['name']):
		# print(proc.info['name'])
		if procname == proc.info['name']:
			if optstr in proc.cmdline():
				isprocessrunning = True
	return isprocessrunning

def checkcmdrunning(procname):
	isprocessrunning = False
	for proc in psutil.process_iter(['name']):
		for item in proc.cmdline():
			# print(item)
			if procname == item:
				isprocessrunning = True
	return isprocessrunning

def checkcmdrunningwithopt(procname, optstr):
     isprocessrunning = False
     for proc in psutil.process_iter(['name']):
             for item in proc.cmdline():
                     if procname == item:
#                             print(proc.cmdline())
                             if optstr in proc.cmdline():
                                     isprocessrunning = True
     return isprocessrunning

print("Right Now: ", rightnow)
#print("Later (prestreamtime): " , later)
#print("Earlier (poststreamtime): ", earlier)

client = caldav.DAVClient(url=caldav_url, username=username, password=password)
my_principal = client.principal()
# calendars = my_principal.calendars()
# print(calendars)

mycalendar = caldav.Calendar(client=client, url=calendarurl)
#print(mycalendar)
events_fetched = mycalendar.date_search(start=earlier, end=later, expand=True)

#print(events_fetched)
#print(len(events_fetched))
if 0 == len(events_fetched):
	print("no streams currently scheduled")
	if checkprocessrunningwithopt('obs', '--startstreaming'): #checkprocessrunning('obs'):
		print("OBS is running and streaming but no event is scheduled, stopping the stream")
		os.system("sudo /usr/bin/pkill --signal SIGTERM obs")
	else:
		print("OBS is not running, so not doing anything")
else:
	try:
	#	print(events_fetched[0].data)
		firstEventData = events_fetched[0].data
	#	print('firstEventData is: ', firstEventData)
		f = re.compile(r"SUMMARY:")
		#print(f.match('SUMMARY: hey there').string[8:])
		eventname = re.search('^SUMMARY.*', firstEventData, re.MULTILINE).group(0)[8:]
		re.search('^SUMMARY.*', firstEventData, re.MULTILINE).group(0)[8:]
		prestream = mycalendar.date_search(start=rightnow, end=later, expand=True)
		poststream = mycalendar.date_search(start=earlier, end=rightnow, expand=True)
		if ( (len(prestream) > 0) and (0 == len(poststream)) ):
			print("currently pre-streaming event: ", eventname)
			if checkprocessrunning('obs'):
				print("OBS is running during pre-stream, not doing anything")
			else:
				print("OBS is not running during pre-stream, starting it")
				os.system("export DISPLAY=:0; export LIBVA_DRIVER_NAME=i965; /usr/bin/obs --startstreaming --disable-shutdown-check --profile 'default' &> /home/pi/obs-logfile.txt &")
		elif ( (len(poststream) > 0) and (0 == len(prestream)) ):
			print("currently post-streaming event: ", eventname)
			if checkprocessrunning('obs'):
				print("OBS is running during post-stream, not doing anything")
			else:
				print("OBS is not running during post-stream, starting it")
				os.system("export DISPLAY=:0; export LIBVA_DRIVER_NAME=i965; /usr/bin/obs --startstreaming --disable-shutdown-check --profile 'default' &> /home/pi/obs-logfile.txt &")
		else: # ( (len(poststream) > 0) and (len(prestream) > 0) ):
			print("currently streaming event: ", eventname)
			if checkprocessrunning('obs'):
				print("OBS is running, not doing anything")
			else:
				print("OBS is not running, starting it")
				os.system("export DISPLAY=:0; export LIBVA_DRIVER_NAME=i965; /usr/bin/obs --startstreaming --disable-shutdown-check --profile 'default' &> /home/pi/obs-logfile.txt &")
	except Exception as e:
		print("exception when accessing calendar, taking no action")
		print(str(e))
		pass
