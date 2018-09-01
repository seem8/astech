# README #

This is a webapp to control and manage headless MegaMek (www.megamek.org) server.

It's intended to run on a Linux machine with Oracle Java JRE and Python 3.6.

Some of the features are:
- start/stop MegaMek server,
- view MegaMek log file,
- switch between any number of MegaMek versions,
- upload custom units, maps and saved games.

# HOW IT LOOKS #

![login page](https://github.com/seem8/astech/blob/master/app/screenshots/astech_login.png "login page")
![index page](https://github.com/seem8/astech/blob/master/app/screenshots/astech_index.png "index page")
![files page](https://github.com/seem8/astech/blob/master/app/screenshots/astech_files_2.png "files page")
![options page](https://github.com/seem8/astech/blob/master/app/screenshots/astech_options.png "options page")

# HOW TO RUN #

1. Install Oracle Java JRE in /usr/java (RPM packages and installation script from www.java.com will do just that).

2. Unpack megamek-0.44.0.tar.gz into astech/mek/installed/ directory. If You want different version, edit astech/config/astech.conf, or run config/generator.py in config directory.

3. Run "python3.6 astech.py".

4. View "localhost:8080" in your browser.

5. Default username is 'someuser' with 'somepassword'.

------------------------------------

# WHY ASTECH #
I'm playing MegaMek for year now. As much as I like miniatures and huge maps, custom hexed terrain and beer, some games are simply impractical on physical table. That's why I choose MegaMek for a lot of my games.

MegaMek has no dedicated server software, just a parameter to launch as a headless (it means without any window) server app. This is important, because it can be run on a Linux VPS server, without need for a graphical interface. It saves a ton or ram and removes any connectivity problems.

But I figured out, that some graphical interface would be great and that's why Astech is here. I created video tutorial for new users: https://youtu.be/r5_qf0LX8p4

# FOR WHO #
For anyone who wants to host a Megamek server on Linux. Aside from getting new version of MegaMek from time to time, there is no need of console work. Just wget desired MegaMek version and untar it to 'installed' directory and Astech will take care of the rest without the need of restart.

# TRY IT #
If you want to use Astech, I can provide link, login and password. Ask me here on GitHub, or at Battletech forum: http://bg.battletech.com/forums/index.php?topic=57664.0
