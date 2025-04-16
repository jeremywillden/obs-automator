# obs-automator

Configure the file with the account username and paths for your Linux user account.

Consider leaving the user logged in with the screen locked so the DISPLAY will exist, or OBS will not launch.

Run the obs-automator.py script in a cron job, as often as every minute.

It will update your OBS settings files and launch the OBS Studio application, then shut it down when the event completes.
