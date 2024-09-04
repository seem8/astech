# README #

This is a webapp to control and manage headless MegaMek (www.megamek.org) server.

It's intended to run on a Linux machine with Java 17 and Python 3.6+. Tested up to Python 3.12.

# HOW TO RUN #

1. Install Java JDK 17 as /usr/bin/java. It can by a symlink to /etc/alternatives.

2. Unpack megamek-0.[version].[release].tar.gz as astech/megamek-version directory. In this example it will be megamek-0.49.19.1 (https://github.com/MegaMek/megamek/releases/download/v0.49.19.1/megamek-0.49.19.1.tar.gz). Read astech-version/PLACEHOLDER_FOR_ASTECH for more deailed instruction.

4. Run command AST_DEBUG=True AST_MM_VERSION=0.49.19.1 AST_MM_PORT=2346 AST_USER=username AST_PASS=password python3 astech.py

5. View "localhost:8080" in your browser. You can run it on a public IP and it will work, but without any https encryption, or anti-ddos protection.

ENV variables to use:
- AST_DEBUG=True|False ; run application in debug mode; optional ; default False
- AST_MM_PORT=[number] ; port number for joining MegaMek games ; optional ; default 2346
- AST_MM_VERSION=[A.B.C.D...] ; MegaMek version ; mandatory ; no default
- AST_USER=username ; optional ; default kerensky
- AST_PASS=password ; optional ; default sldf

# HOW TO RUN WITH SOME SECURITY #

Modify step 4 to AST_MM_VERSION=0.49.19.1 AST_MM_PORT=2346 AST_USER=otherusername AST_PASS=SeCuRePaSsWoRd python3 astech.py

You need:
- public IP address,
- some sort of http proxy, like Nginx,
- SSL certicate, possibly from Let's Encrypt.

Sample Nginx vhost configuration is included as app/nginx/sample.conf.

------------------------------------

# HOW IT LOOKS #
It is a little different now, but not much.

![login page](https://github.com/seem8/astech/blob/master/app/screenshots/astech_login.png "login page")
![index page](https://github.com/seem8/astech/blob/master/app/screenshots/astech_index.png "index page")
![files page](https://github.com/seem8/astech/blob/master/app/screenshots/astech_files_2.png "files page")
![options page](https://github.com/seem8/astech/blob/master/app/screenshots/astech_options.png "options page")

