# obs-automator

Automatically configure OBS Studio with an XML file (compatible with Vidiu Teradek and similar hardware encoders) and start/stop the stream.

Configure the file with the account username and paths for your Linux user account.

Consider leaving the user logged in with the screen locked so the DISPLAY will exist, or OBS will not launch.

Run the obs-automator.py script in a cron job, as often as every minute.

It will update your OBS settings files and launch the OBS Studio application, then shut it down when the event completes.

To create your own template files for the "service.ini" and "basic.json", once you've set up OBS With the scenes, sources, and other configurations as you want them, copy these files to the home folder (the original paths are in the obs-automator.py script).  Replace the video bit rate with VBITRATE and the audio bit rate with ABITRATE - these values will be replaced by the Python script when it runs.  Similarly, replace the rtsp URI/URL with RTMPURL and the stream key with RTMPSTREAM, again these will be replaced by the script from the values taken from the XML configuration file.
