#!/usr/bin/env python3

import requests
from shutil import copyfile
import os

# customize your file paths here for your user account
streamURLfilePath = '/home/pi/stream.url'
basicIniTemplateFile = '/home/pi/basic.ini.template'
serviceJsonTemplateFile = '/home/pi/service.json.template'
basicIniFile = '/home/pi/basic.ini'
serviceJsonFile = '/home/pi/service.json'
streamURLfile = '/home/pi/stream.url'
liveServiceJsonFile = '/home/pi/.config/obs-studio/basic/profiles/default/service.json'
liveBasicIniFile = '/home/pi/.config/obs-studio/basic/profiles/default/basic.ini'
obsLogFile = '/home/pi/obs-logfile.txt'

# Replace the following with the Webcast URL for your Teradek-compatible XML configuration file
x = requests.get('https://webcast.example.com/2368').text
# The example files below are templates, though the test-off file should work as-is
#x = requests.get('https://raw.githubusercontent.com/jeremywillden/obs-automator/main/test-on.xml').text
#x = requests.get('https://raw.githubusercontent.com/jeremywillden/obs-automator/main/test-off.xml').text

streamstarting = False
streamending = False

# There's certainly a better way to extract these values, using standard XML libraries is risky,
# as many of them do not check for intentional attack data structures
# (they can eat Gigs of RAM with a few lines of code) - this method is robust enough for this application
_,videobitrate = x.split("<video>")
videobitrate,_ = videobitrate.split("</video>")
_,videobitrate = videobitrate.split("<custom_bitrate>")
videobitrate,_ = videobitrate.split("</custom_bitrate>")
_,audiobitrate = x.split("<audio>")
audiobitrate,_ = audiobitrate.split("</audio>")
_,audiobitrate = audiobitrate.split("<custom_bitrate>")
audiobitrate,_ = audiobitrate.split("</custom_bitrate>")
_,url = x.split("<url>")
url,_ = url.split("</url>")
_,streamkey = x.split("<stream>")
streamkey,_ = streamkey.split("</stream>")

try:
	with open(streamURLfilePath, 'r') as streamurlfilereader:
		currentstreamurl = streamurlfilereader.read()
except:
	currentstreamurl = "RTMPURL"
	pass
if("RTMPURL" == url):
	url = ""
if("RTMPURL" == currentstreamurl):
	currentstreamurl = ""
print("currentstreamurl is " + currentstreamurl)
if(url.startswith("rtmp:")):
	serveractive = True
	print("serveractive is True")
else:
	serveractive = False
	print("serveractive is False")
	url = "" # this is the value when no stream is active
if(currentstreamurl.startswith("rtmp:")):
	streamactive = True
	print("streamactive is True")
else:
	streamactive = False
	print("streamactive is False")
	currentstreamurl = "" # this is the value when no stream is active

if("" == url):
	if(streamactive):
		print("stopping stream and exiting")
		streamending = True
	else:
		print("no stream scheduled, no stream running, exiting")
else:
	if(streamactive):
		print("stream URL has not changed, not taking any action")
	else:
		streamstarting = True
		print("stream URL has just changed for a new event, creating files and starting stream")
		currentstreamurl = url
		print("stream url: " + url)
		print("stream key: " + streamkey)
		print("video bitrate: " + videobitrate)
		videokbitrate = str(int(int(videobitrate) / 1000))
		print("video kbitrate: " + videokbitrate)
		print("audio bitrate: " + audiobitrate)
		audiokbitrate = str(int(int(audiobitrate) / 1000))
		print("audio kbitrate: " + audiokbitrate)
		#print(b)

		with open(basicIniTemplateFile, 'r') as basicfilereader:
			basicfiledata = basicfilereader.read()
		with open(serviceJsonTemplateFile, 'r') as servicefilereader:
			servicefiledata = servicefilereader.read()

		#print("BASIC FILE:")
		#print(basicfiledata)
		#print("SERVICE FILE:")
		#print(servicefiledata)

		basicfiledata = basicfiledata.replace("VBITRATE", videokbitrate)
		basicfiledata = basicfiledata.replace("ABITRATE", audiokbitrate)
		with open(basicIniFile, 'w+') as writer:
			writer.seek(0)
			writer.writelines(basicfiledata)
			writer.truncate()

		servicefiledata = servicefiledata.replace("RTMPURL", currentstreamurl)
		servicefiledata = servicefiledata.replace("RTMPSTREAM", streamkey)
		with open(serviceJsonFile, 'w+') as writer:
			writer.seek(0)
			writer.writelines(servicefiledata)
			writer.truncate()

if(streamstarting or streamending):
	print("writing to stream.url file the value: " + url)
	with open(streamURLfile, 'w+') as streamurlfilewriter:
		streamurlfilewriter.seek(0)
		streamurlfilewriter.write(url)

	copyfile(serviceJsonFile, liveServiceJsonFile)
	copyfile(basicIniFile, liveBasicIniFile)

if(streamstarting):
	os.system("export DISPLAY=:0; /usr/bin/obs --startstreaming --profile 'default' &> " + obsLogFile + " &")
if(streamending):
	os.system("pkill obs")

