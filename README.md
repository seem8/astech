# README #

This is a webapp to control and manage headless MegaMek (www.megamek.org) server.

It's intended to run on a Linux machine on any virtual, or psychical server.

It depends on Oracle Java JRE and Python 3.6.x.

![Alt text](https://lukaszposadowski.pl/wp-content/uploads/server_status.jpg "Optional title")

# HOW TO RUN #

1. Install Oracle Java JRE in /usr/java (RPM packages and installation script will do just that).

2. Run "python3.6 astech.py".

3. View "localhost:8080" in your browser.

# INSTALLATION #

1. Install Oracle Java JRE in /usr/java (RPM packages and installation script will do just that).

2. Install Python 3.6.x and make sure you can type "python3.6" in terminal to launch Python Shell.

3. (optional) Create user astech to "use" Astech and unpack astech-version.zip in his home directory.
   That user have to run both Java and Python.
   You may lock that user account with "usermod -L username".

4. (optional) If you want to run Astech at boot:
   - copy astech.service file to /etc/systemd/system:
   - change user line to username from #3, or to your username.

5. If you have firewall, open ports 3477 and 8080.

6. Run "systemctl start astech" as root, or with sudo.

7. Type your.domain:8080, or ip.ip.ip.ip:8080 in your browser.
