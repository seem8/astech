#!/home/lukasz/progi/python/botle/bin/python3
'''Megamek server administration page.
This is ALPHA quality software,
expect some bugs and glitches.
author: Łukasz Posadowski,  mail [at] lukaszposadowski.pl'''

# import subprocess, for launching jar files
import subprocess

# sleep may help with subprocess
from time import sleep

# import bottle
# remember to delete debug for production
from bottle import template, response, request, get, post, error, \
                   redirect, static_file, run, route, debug

# file uploading and listing directories
# I'll try to use pathlib.Path over os.path, when possible.
import os
from pathlib import Path

# we have to append date to filenames 
import time 


# ----------------------------------------
# ------- HELPER FUNCTIONS ---------------
# ----------------------------------------

# megamek log files into lists
# TODO rewrite with WITH
def getFile(filename):
  '''filename -> list of last 22 lines'''
  try:
    logfile = open(filename,'r')
  except(FileNotFoundError):
    # when filename does not exist
    create_file = open(filename,'x').close()
    logfile = open(filename,'r')
  logfilelines = logfile.readlines()
  logfile.close()
  # we need only couple of last lines from the file
  lastlog = logfilelines[len(logfilelines)-22 : len(logfilelines)]
  lastlog.reverse()
  return lastlog 

# get a string from localtime
def stringTime():
  '''returns string: year-month-day__hour-minute-second_'''
  t = time.localtime()
  strtime = str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + "__" + \
            str(t[3]) + "-" + str(t[4]) + "-" + str(t[5]) + "_"
  return strtime

# login and password (without encryption)
# TODO looks secure so far... but have to be updated for
# database and encryption
def crede(l, p):
 if l == 'brathac' and p == 'deathabovefrom':
   return True
 else:
   return False


# ----------------------------------------
# ------- MAIN LOGIC ---------------------
# ----------------------------------------

# MegaMek server status and controls
# we have a class for a little namespace home 
class MegaTech:
  '''MegaMek server controls and status'''
  def __init__(self):
    self.ison = False                               # megamek is off by default 
    self.version = '0.43.2'                         # megamek version
    self.port = 3477                                # port for megamek server
    self.domain = 'mek.solaris7.pl'                 # nice site name
    self.from_save = False                          # check if savegame is loaded
    self.password = False                           # optional password to change game options 
    self.save_dir = Path('./savegames/')            # default save dir for megamek
    self.map_dir = Path('./data/boards/astech/' )   # astech will upload maps there
    self.unit_dir = Path('./data/mechfiles/astech') # and custom mechs there

    # command to lauch MegaMek server with provided port
    self.command = '/usr/java/default/bin/java -jar MegaMek.jar -dedicated -port ' + str(self.port)
  
  def start(self):
    '''starts MegaMek server'''
    # if password is set, add it to the lauch command
    if self.password != False:
      self.command += ' -password ' + self.password + ' '
    self.process = subprocess.Popen(self.command.split()) 
    # TODO testing parameters to load save games - not ready yet
    # dedicated servers parameters are as follows:
    # -port [port] -password [password] [savedgame]
    sleep(2)
    self.ison = True
  
  def stop(self):
    '''stops MegaMek server'''
    if self.ison == True:
      self.process.kill()
      self.ison = False
  
  def restart(self):
    '''quick restart with start and stop functions'''
    self.stop()
    sleep(1)
    self.start()

megatech = MegaTech()
# ----------------------------------------

# below is bottle.py related stuff

# ----------------------------------------
# ------- STATIC FILES -------------------
# ----------------------------------------

# site logo (thanks ManganMan) and other images
@route('/image/<filename>')
def image(filename):
  return static_file(filename, root='./img/', mimetype='image/png')
# ----------------------------------------

# ----------------------------------------
# ------- LOGIN PAGE ---------------------
# ----------------------------------------

# a little login template
@get('/login')
def login():
  # username variable is required for header template
  username = request.get_cookie('administrator', secret='comstarwygra')
  # cookie with information about bad password
  bad_password = request.get_cookie('badPassword', secret='comstarprzegra')
  return template('login', badPass=bad_password, \
                           username=username)
# ----------------------------------------

# check credentials and redirect to other routes
@post('/login')
def check_login():
  # check if username and password isn't something like '/mmstop'
  if request.forms.get('username').isalpha() and request.forms.get('password').isalpha():
    username = request.forms.get('username')
    password = request.forms.get('password')

    # now check actual credentials from the form
    if crede(username, password):
      # good password
      # signed cookie for a period of time in seconds (about a day)
      response.set_cookie('administrator', username, max_age=87654, secret='comstarwygra')
      response.delete_cookie('badPassword')
      redirect('/')
    elif not crede(username,password):
      # bad password
      response.set_cookie('badPassword', 'nopass', max_age=21, secret='comstarprzegra')
      redirect('/login')
  else:
    # if login and/or password are not alpha, don't parse them
    # and redirect to login (just to be safe)
    response.set_cookie('badPassword', 'nopass', max_age=21, secret='comstarprzegra')
    redirect('/login')
# ----------------------------------------

# TODO - saves, maps and unit uploads are very similar.
#        Maybe there is a way to write one 
#        function and template for all three.

# ----------------------------------------
# ------- SAVEGAMES PAGE -----------------
# ----------------------------------------

# savegame upload form
@get('/saves')
def upload_save():
  username = request.get_cookie('administrator', secret='comstarwygra')

  # current page for become_veteran and become_rookie functions
  response.set_cookie('curpage', '/saves', max_age=321, secret='comstarwygra')
  
  # checks if help messages will be displayed
  veteran = request.get_cookie('veteran', secret='comstarwygra')
  if username:
    return template('saves', username=username, \
                             veteran=veteran, \
                             # TODO create dir if not exist
                             savegames=os.listdir(megatech.save_dir)) #, \
                             # removeSave=os.remove('.savegames/'+item))
  # an idea to remove saved games:
  # saves = os.listdir(./savegames')
  # os.remove('.savegames/saves[index])
  elif not username:
    redirect('/login')
# ----------------------------------------

# checking and uploading files to savegames dir
@post('/saves')
def do_upload_save():
  username = request.get_cookie('administrator', secret='comstarwygra')
  if username:
    save_file = request.files.get('saved_game')

    # check if file extension is .gz
    name, ext = os.path.splitext(save_file.filename)
    if ext not in ('.gz'):
      # TODO nice info about wrong file extension
      print('WRONG FILE EXTENSION :(')
    else:
      # TODO check if directory is present, create if nessesary;
      # add current time to file name, to avoid
      # incidental overwrites
      save_file.filename = stringTime() + save_file.filename
      save_file.save(str(megatech.save_dir), overwrite=True)

      # checking filesize and, if bigger than 1M, delete file
      filestats = os.stat(str(megatech.save_dir) + '/' + save_file.filename)
      if filestats.st_size > 1000000000:
        # TODO nice info about too big file
        print('FILE IS TOO BIG. :(')
        os.remove(megatech.save_dir + save_file.filename)

    sleep(1)
    redirect('/saves')
  elif not username:
    redirect('/login')
# ----------------------------------------

# ----------------------------------------
# ------- MAPS PAGE ----------------------
# ----------------------------------------

# map files upload form
@get('/maps')
def upload_map():
  username = request.get_cookie('administrator', secret='comstarwygra')

  # current page for become_veteran and become_rookie functions
  response.set_cookie('curpage', '/maps', max_age=321, secret='comstarwygra')

  # checks if help messages will be displayed
  veteran = request.get_cookie('veteran', secret='comstarwygra')
  if username:
    return template('maps', username=username, \
                            veteran=veteran, \
                            # TODO create dir if not exist
                            mapfiles=os.listdir(megatech.map_dir))
  elif not username:
    redirect('/login')
# ----------------------------------------

# checking and uploading files to savegames dir
@post('/maps')
def do_upload_map():
  username = request.get_cookie('administrator', secret='comstarwygra')
  if username:
    map_file = request.files.get('map_file')
    name, ext = os.path.splitext(map_file.filename)
    if ext not in ('.board'):
      # TODO nice info about wrong file extension
      print('WRONG FILE EXTENSION :(')
    else:
      # TODO check if directory is present, create if nessesary;
      # add current time to file name, to avoid
      # incidental overwrites
      map_file.save(str(megatech.map_dir), overwrite=True)
      filestats = os.stat(str(megatech.map_dir) + '/' + map_file.filename)

      # checking filesize and, if bigger than 1M, delete file
      if filestats.st_size > 1000000000:
        # TODO nice info about too big file
        print('FILE IS TOO BIG. :(')
        os.remove(megatech.map_dir + map_file.filename)
    sleep(1)
    redirect('/maps')
  elif not username:
    redirect('/login')
# ----------------------------------------

# ----------------------------------------
# ------- CUSTOM UNITS PAGE --------------
# ----------------------------------------

# listing custom units and upload form handling
@get('/units')
def upload_units():
  username = request.get_cookie('administrator', secret='comstarwygra')

  # current page for become_veteran and become_rookie functions
  response.set_cookie('curpage', '/units', max_age=321, secret='comstarwygra')

  # checks if help messages will be displayed
  veteran = request.get_cookie('veteran', secret='comstarwygra')
  if username:
    return template('units', username=username, \
                             veteran=veteran, \
                             # TODO create dir if not exist
                             unitfiles=os.listdir(megatech.unit_dir))
  elif not username:
    redirect('/login')
# ----------------------------------------


# uploading and checking custom units files
@post('/units')
def do_upload_units():
  username = request.get_cookie('administrator', secret='comstarwygra')
  if username:
    unit_file = request.files.get('unit_file')
    name, ext = os.path.splitext(unit_file.filename)
    if ext not in ('.mtf'):
      # TODO nice info about wrong file extension
      print('WRONG FILE EXTENSION :(')
    else:
      # TODO check if directory is present, create if nessesary;
      # add current time to file name, to avoid
      # incidental overwrites
      unit_file.save(str(megatech.unit_dir), overwrite=True)
      filestats = os.stat(str(megatech.unit_dir) + '/' + unit_file.filename)

      # checking filesize and, if bigger than 1M, delete file
      if filestats.st_size > 1000000000:
        # TODO nice info about too big file
        print('FILE IS TOO BIG. :(')
        os.remove(megatech.unit_dir + unit_file.filename)
    sleep(1)
    redirect('/units')
  elif not username:
    redirect('/login')
# ----------------------------------------

# ----------------------------------------
# ------- TUTORIAL PAGE ------------------
# ----------------------------------------

# tutorial
@route('/firststrike')
def tutorial():
  username = request.get_cookie('administrator', secret='comstarwygra')
  
  # current page for become_veteran and become_rookie functions
  response.set_cookie('curpage', '/firststrike', max_age=321, secret='comstarwygra')
  
  # checks if help messages will be displayed
  veteran = request.get_cookie('veteran', secret='comstarwygra')
  if username:
    return template('first_strike', username=username, \
                                    veteran=veteran)
  elif not username:
    redirect('/login')
# ----------------------------------------

# ----------------------------------------
# ------- MAIN PAGE ----------------------
# ----------------------------------------

# main route
@get('/')
def administrator():
  username = request.get_cookie('administrator', secret='comstarwygra')

  # checks if help messages will be displayed
  veteran = request.get_cookie('veteran', secret='comstarwygra')

  # current page for become_veteran and become_rookie functions
  response.set_cookie('curpage', '/', max_age=1234, secret='comstarwygra')

  if username:
    response.delete_cookie('badPassword')
    return template('administrator', username = username, \
                                     veteran = veteran, \
                                     mtison = megatech.ison, \
                                     mtver = megatech.version, \
                                     mtport = str(megatech.port), \
                                     mtdomain = megatech.domain, \
                                     getLogFile = getFile('logs/megameklog.txt'), \
                                     mtpassword = megatech.password, \
                                     mtfromSave = megatech.from_save)

  elif not username:
    redirect('/login')

# main route - setting server password via html form
@post('/')
def setMekPassword():
  username = request.get_cookie('administrator', secret='comstarwygra')
  
  if username:
    # check if username and password isn't something like '/mmrestart'
    if request.forms.get('mekpassword').isalpha():
      megatech.password = request.forms.get('mekpassword')
      redirect('/')
    else:
      # if mekpassword is not alpha, don't parse it
      # and redirect to login (just to be safe)
      response.set_cookie('noalpha', 'noalpha', max_age=21, secret='comstarprzegra')
  elif not username:
    redirect('/login')
# ----------------------------------------

# A little functions doing bigger functions.
@route('/mmturnon')
def mmturnon():
  if request.get_cookie('administrator', secret='comstarwygra'):
    megatech.start()
  redirect('/')

@route('/mmturnoff')
def mmturnoff():
  if request.get_cookie('administrator', secret='comstarwygra'):
    megatech.stop()
  redirect('/')

# it's not used anywhere now
#@route('/mmrestart')
#def mmrestart():
#  if request.get_cookie('administrator', secret='comstarwygra'):
#    megatech.restart()
#  redirect('/')

@route('/logout')
def logoff():
  response.delete_cookie('administrator')
  redirect('/')

# set vetran cookie to hide tutorial messages
@route('/veteran')
def become_veteran():
  if request.get_cookie('administrator', secret='comstarwygra'):
    response.set_cookie('veteran', 'veteran', secret='comstarwygra')
  # curpage cookie is storing current page (route)
  redirect(request.get_cookie('curpage', secret='comstarwygra'))

# delete veteran cookie to show tutorial messages again 
@route('/green')
def become_green():
  if request.get_cookie('administrator', secret='comstarwygra'):
    response.delete_cookie('veteran')
  # curpage cookie is storing current page (route)
  redirect(request.get_cookie('curpage', secret='comstarwygra'))

# finally - 404
@error(404)
def route404(error):
  username = request.get_cookie('administrator', secret='comstarwygra')
  return template('error404', username=username)

# ----------------------------------------
# main debug run
# remember to add debug import from bottle
debug(True)
run(host='localhost', port=8080, reloader=True)

# main production run
# remember to delete debug import from bottle
#run(host='0.0.0.0', port=8080)

