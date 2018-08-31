# README #

This is a webapp to control and manage headless MegaMek (www.megamek.org) server.

It's intended to run on a Linux machine on any virtual, or psychical server.

It depends on Oracle Java JRE and Python 3.6.

![Alt text](https://lukaszposadowski.pl/wp-content/uploads/server_status.jpg "Optional title")

# HOW TO RUN #

1. Install Oracle Java JRE in /usr/java (RPM packages and installation script from www.java.com will do just that).

2. Unpack megamek-0.44.0.tar.gz into astech/mek/installed/ directory. If You want different version, edit astech/config/astech.conf, or run config_generator.py in config directory.

3. Run "python3.6 astech.py".

4. View "localhost:8080" in your browser.

5. Default username is 'someuser' with 'somepassword'.

------------------------------------

More info in the wiki: https://github.com/seem8/astech/wiki
