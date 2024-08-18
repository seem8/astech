# README #

This is a webapp to control and manage headless MegaMek (www.megamek.org) server.

It's intended to run on a Linux machine Python 3.6+. Tested up to Python 3.9,
but it shoudl work with 3.11 without any problem.

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

1. Install Java JRE as /usr/bin/java. You should have either an executable of Java 11, Java 17, or a symlink to /etc/alternatives.

2. Change directory to config and run "python3 config_generator.py". It will create two files:
   - astech.crede with login and sha512sum of You password,
   - astech.cookie with two secrets for cookies.

3. Unpack megamek-0.[version].[release].tar.gz into astech/mek/installed/ directory. If You want different version, edit astech/config/astech.conf, or run config/generator.py in config directory.

4. Run "python3 astech.py".

5. View "localhost:8080" in your browser.

------------------------------------

# WHY ASTECH #
I'm playing MegaMek for year now. As much as I like miniatures and huge maps, custom hexed terrain and beer, some games are simply impractical on physical table. That's why I choose MegaMek for a lot of my games.

MegaMek has no dedicated server software, just a parameter to launch as a headless (it means without any window) server app. This is important, because it can be run on a Linux VPS server, without need for a graphical interface. It saves a ton or ram and removes any connectivity problems.

But I figured out, that some graphical interface would be great and that's why Astech is here. I created video tutorial for new users: https://youtu.be/r5_qf0LX8p4

# FOR WHO #
For anyone who wants to host a Megamek server on Linux. Aside from getting new version of MegaMek from time to time, there is no need of console work. Just wget desired MegaMek version, untar it to 'mek/installed' directory and Astech will take care of the rest without restart.

# TRY IT #
If you want to use Astech, I can provide link, login and password. Ask me here on GitHub, or at Battletech forum: http://bg.battletech.com/forums/index.php?topic=57664.0

