#!/usr/bin/python3
'''Megamek server administration page.
This is ALPHA quality software,
expect some bugs and glitches.
author: Łukasz Posadowski,  mail [at] lukaszposadowski.pl'''

# import subprocess, for launching jar files
import subprocess

# sleep may help with subprocess,
from time import sleep

# pickle is for the config files;
# maybe I will switch to sqlite
import pickle

# import bottle
# remember to comment out ', debug'  for production
from bottle import template, response, request, get, post, error, \
                   redirect, static_file, run, route, debug

# file uploading and listing directories
import os

# we have to append date to filenames 
import time 

# we're checking the password by making hash
# and comparing with a bytestring
import hashlib

# for downloading new versions of megamek
import urllib.request


# ----------------------------------------
# ------- HELPER FUNCTIONS ---------------
# ----------------------------------------

# convert megamek log files into lists
def getFile(filename):
  '''filename -> reversed list of last 81 lines'''
  try:
    # log file doesn't exist by default in MegaMek
    open(filename,'r').close()
  except FileNotFoundError:
    open(filename,'w').close()
  with open(filename,'r') as myfile:
    mylines = myfile.readlines()
    # we need just 81 last lines
    lastlog = mylines[len(mylines)-81 : len(mylines)]
    lastlog.reverse()
    
    # sometimes the word in file is too long to fit inside template div,
    # so I'm inserting '\n' all over the lines;
    # in tpl it is interpreted by SPACE character, which is capable to
    # break like if necessary (werid, but it works);
    # TODO it adds verid looking spaces into a log file view
    for i in range(len(lastlog)):
      t = list(lastlog[i])
      try:
        for ii in (50, 101, 152, 203, 254, 305, 356, 407, 458, 509):
          t.insert(ii, '\n')
      except IndexError:
        pass 
      lastlog[i] = ''.join(t)
        
    return lastlog
# ----------------------------------------

# get a string from localtime
def stringTime():
  '''returns string: year-month-day__hour-minute-second_'''
  t = time.localtime()
  strtime = str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + "__" + \
            str(t[3]) + "-" + str(t[4]) + "-" + str(t[5]) + "_"
  return strtime
# ----------------------------------------

# user name and password;
# password encryption is nice,
# but useless without https;
# defaults are 'somelogin' and 'somepassword'
def crede(u, p):
  '''check credentials'''
  credefile = open('config/astech.crede', 'r+b')
  # I really want to close that file
  credentials = pickle.load(credefile)
  credefile.close()
  if u == credentials['user']:
    if hashlib.sha512(p.encode()).hexdigest() == credentials['pass']:
      return True
    else:
      return False
  else:
    return False
# ----------------------------------------


# ----------------------------------------
# ------- SOME USEFULL VARIABLES ---------
# ----------------------------------------

# we need two separate secrets:
# 1: for cookies with ~1 day expiration time,
# 2: for 5 second cookies to display warnings on templates
# secrets are stored in astech.cookie config file
secretfile = open('config/astech.cookie', 'r+b')
cookies = pickle.load(secretfile)

secret1 = cookies['alpha']
secret2 = cookies['beta']

secretfile.close()


# ----------------------------------------
# ------- MAIN LOGIC ---------------------
# ----------------------------------------

# MegaMek server status and controls
# we have a class for a little namespace home 
class MegaTech:
  '''MegaMek server controls and status'''
  def __init__(self):
    confile = open('config/astech.conf', 'r+b') # Astech configuration file
    self.asconfig = pickle.load(confile)        # restore dictionary from a file
    confile.close()
 
    # 4 vars are stored in astech.config file
    self.name = self.asconfig['name']         # name of the instance 
    self.version = self.asconfig['version']   # megamek version
    self.port = self.asconfig['port']         # port for megamek server
    # optional password to change game options
    self.game_password = self.asconfig['game_password']

    self.ison = False                         # megamek is off by default 
    self.process = False                      # to check if MegaMek is running
    self.domain = 'some.server.com'           # nice site name

    # "shortcuts" for various used directories
    self.meks_dir = 'megamek/installed'       # avaiable versions of Megamek
    self.archive_dir = 'megamek/archives'     # downloaded versions of MegaMek
    
    self.install_dir = self.meks_dir + '/megamek-' + self.version  # megamek directory
    self.save_dir = self.install_dir + '/savegames/'               # default save dir for megamek
    self.map_dir = self.install_dir + '/data/boards/astech/'       # astech will upload maps there
    self.unit_dir = self.install_dir + '/data/mechfiles/astech/'   # and custom mechs there
    self.logs_dir = self.install_dir + '/logs/'                    # gamelogs are there

  def start(self):
    '''starts MegaMek server'''
    # if game password is set, add it (with a space character at the end) to the lauch command
    if self.game_password != False:
      self.command = '/usr/java/default/bin/java -jar MegaMek.jar -dedicated -port ' + \
                     str(self.port) + ' -password ' + str(self.game_password) + ' '
    # if game password is not set, just run Megamek
    elif self.game_password == False:
      self.command = '/usr/java/default/bin/java -jar MegaMek.jar -dedicated -port ' + \
                     str(self.port)
    
    # start MegaMek dedicated server with parameters and in it's working directory
    self.process = subprocess.Popen(self.command.split(), cwd=self.install_dir) 
    
    # TODO testing parameters to load save games - not ready yet
    # dedicated servers parameters are as follows:
    # -port [port] -password [password] [savedgame]

    # we're sleeping, while waiting for Megamek to write a log file;
    # MegaMek is rarely slower than 1 second
    sleep(1)
    # we'll rely on this variable often
    self.ison = True

  def check(self):
    '''check if MegaMek is running'''
    try:
      # none means the process is running
      if self.process.poll() == None:
        return True 
      else:
        # any other result means it's not
        return False
    except AttributeError:
      # in case if the process wansn't initialised yet
      return False

  def stop(self):
    '''stops MegaMek server'''
    if self.ison == True:
      self.process.kill()
      self.ison = False

  def getConfig(self):
    '''creates dictionary from pickled astech config'''
    confile = open('config/astech.conf', 'r+b')
    # I really want to close that file
    self.asconfig = pickle.load(confile)
    confile.close()

    # updating variables from config file 
    self.name = self.asconfig['name']
    self.version = self.asconfig['version']
    self.port = self.asconfig['port']
    self.game_password = self.asconfig['game_password']
    
    # updating "shortcuts" for various used directories
    self.install_dir = self.meks_dir + '/megamek-' + self.version  # megamek directory
    self.save_dir = self.install_dir + '/savegames/'               # default save dir for megamek
    self.map_dir = self.install_dir + '/data/boards/astech/'       # astech will upload maps there
    self.unit_dir = self.install_dir + '/data/mechfiles/astech/'   # and custom mechs there
    self.logs_dir = self.install_dir + '/logs/'                    # gamelogs are there


  def writeConfig(self):
    '''pickles astech config into astech.conf file'''
    confile = open('config/astech.conf', 'w+b')

    # creating new config
    self.asconfig = { 'name': self.name, \
                      'version': self.version, \
                      'port': self.port, \
                      'game_password': self.game_password }

    pickle.dump(self.asconfig, confile, protocol=0)
    confile.close()

# sensors... engaged 
megatech = MegaTech()
# ----------------------------------------

# below is bottle.py related stuff, mainly routes for web browser

# ----------------------------------------
# ------- STATIC FILES -------------------
# ----------------------------------------

# site logo and other images
@route('/image/<filename>')
def image(filename):
  return static_file(filename, root='./static/', mimetype='image/png')

# style.css file for better looking page
@route('/style')
def style():
  return static_file('style.css', root='./static/')
# ----------------------------------------


# download static files
@route('/download/<filetype>/<filename>')
def downloadfile(filetype, filename):
  # check if we are logged in before download, to prevent link guessing
  username = request.get_cookie('administrator', secret=secret1)
  if username:
    # filetype define directory with files to download
    if filetype == 'map':
      rootdir = megatech.map_dir
    elif filetype == 'savegame':
      rootdir = megatech.save_dir
    elif filetype == 'unit':
     rootdir = megatech.unit_dir
    else:
      # er404 leads to nothing, so it will return 404 error page
      rootdir = 'er404'

    # force download
    return static_file(filename, root=rootdir, download=filename)

  elif not username:
    redirect('/login')
# ----------------------------------------
  

# remove static files
@route('/remove/<filetype>/<filename>')
def removefile(filetype, filename):
  # check if we are logged in before download, to prevent link guessing
  username = request.get_cookie('administrator', secret=secret1)
  if username:
    # filetype define directory with files to delete 
    if filetype == 'map':
      rootdir = megatech.map_dir
    elif filetype == 'savegame':
      rootdir = megatech.save_dir
    elif filetype == 'unit':
      rootdir = megatech.unit_dir
    else:
      # er404 leads to nothing, so it will return 404 error page
      rootdir = 'er404'
    
    # remove the file
    try:
      os.remove(rootdir + filename)
      # os.remove is displaying blank page, so we have to
      # quickly return to maps, saves, or units page
      redirect(request.get_cookie('curpage', secret=secret1))
    except FileNotFoundError:
      redirect('/404page')

  elif not username:
    redirect('/login')
# ----------------------------------------


# ----------------------------------------
# ------- LOGIN PAGE ---------------------
# ----------------------------------------

# a little login template
@get('/login')
def login():
  # username variable is required for header template
  username = request.get_cookie('administrator', secret=secret1)
  # cookie with information about bad password
  bad_password = request.get_cookie('badPassword', secret=secret2)
  return template('login', badPass=bad_password, \
                           username=username )
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
      response.set_cookie('administrator', username, max_age=87654, secret=secret1)
      response.delete_cookie('badPassword')
      redirect('/')
    elif not crede(username, password):
      # bad password
      response.set_cookie('badPassword', 'nopass', max_age=5, secret=secret2)
      redirect('/login')
  else:
    # if login and/or password are not alpha, don't parse them
    # and redirect to login (just to be safe)
    response.set_cookie('badPassword', 'nopass', max_age=5, secret=secret2)
    redirect('/login')
# ----------------------------------------


# ----------------------------------------
# ------- MAIN PAGE ----------------------
# ----------------------------------------

# main route
@get('/')
def administrator():
  # check if we are logged in
  username = request.get_cookie('administrator', secret=secret1)
  # check if game password are latin characters only
  noalpha = request.get_cookie('noalpha', secret=secret2)

  # checks if help messages will be displayed
  veteran = request.get_cookie('veteran', secret=secret1)

  # current page for become_veteran and become_rookie functions
  response.set_cookie('curpage', '/', max_age=321, secret=secret1)

  # update data from config file
  megatech.getConfig()

  if username:
    # password and login cookie are checked by now
    response.delete_cookie('badPassword')
    
    # check if MegaMek is on and correct megatech.ison
    if megatech.check():
      megatech.ison = True
    elif not megatech.check():
      megatech.ison = False

    # render template
    return template('administrator', \
                    username = username, \
                    veteran = veteran, \
                    mtison = megatech.ison, \
                    mtver = megatech.version, \
                    mtname = megatech.name, \
                    mtport = str(megatech.port), \
                    mtdomain = megatech.domain, \
                    logFile = getFile(megatech.logs_dir + 'megameklog.txt'), \
                    mtpassword = megatech.game_password, \
                    noalpha = noalpha )

  elif not username:
    redirect('/login')

# main route - setting server password via html form
@post('/')
def setMekPassword():
  username = request.get_cookie('administrator', secret=secret1)
  
  if username:
    game_pass = request.forms.get('mekpassword')
    # check if password isn't something like '/mmstop'
    if game_pass.isalpha():
      megatech.game_password = game_pass
    elif game_pass == '':
      # empty password is no password
      megatech.game_password = False
    else:
      # if mekpassword is not alpha, don't parse it;
      # will display warning message about using nonlatin characters, see administrator.tpl
      response.set_cookie('noalpha', 'noalpha', max_age=5, secret=secret2)
      game_pass = False
      megatech.game_password = False
    
    # refreshing config file
    megatech.writeConfig()
    megatech.getConfig()

    redirect('/')

  elif not username:
    redirect('/login')
# ----------------------------------------


# TODO - saves, maps and unit uploads are very similar.
#        Maybe there is an *elegant* way to write one 
#        function and template for all three.

# ----------------------------------------
# ------- MAPS PAGE ----------------------
# ----------------------------------------

# map files upload form
@get('/maps')
def upload_map():
  username = request.get_cookie('administrator', secret=secret1)

  # cookies set when uploaded file is wrong
  # wrong extension
  wrongboard = request.get_cookie('wrongboard', secret=secret2)
  # over 1.5M size
  bigboard = request.get_cookie('bigboard', secret=secret2)
  # no file selected
  noboard = request.get_cookie('noboard', secret=secret2)
  
  if username:
    # current page for become_veteran and become_rookie functions
    response.set_cookie('curpage', '/maps', max_age=321, secret=secret1)

    # create directory for maps, if not already present 
    if not os.path.isdir(megatech.map_dir):
      os.mkdir(megatech.map_dir)

    # list of current map files, by alphabet
    mapfiles = os.listdir(megatech.map_dir)
    mapfiles.sort()

    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret=secret1)

    # render web page with template
    return template('maps', username=username, \
                            veteran=veteran, \
                            mapfiles=mapfiles, \
                            wrongboard=wrongboard, \
                            bigboard=bigboard, \
                            noboard=noboard)

  elif not username:
    redirect('/login')
# ----------------------------------------

# checking and uploading files to ./data/maps/astech dir
@post('/maps')
def do_upload_map():
  username = request.get_cookie('administrator', secret=secret1)
  if username:
    map_file = request.files.get('map_file')
    try:
      name, ext = os.path.splitext(map_file.filename)
      goodboard = True
    except AttributeError:
      # in the case when no file is choosen;
      # page template will show error message with this cookie
      response.set_cookie('noboard', 'noboard', max_age=5, secret=secret2)
      goodboard = False

    if goodboard:
      response.delete_cookie('noboard')
      if ext not in ('.board'):
        # page template will show error message with this cookie
        response.set_cookie('wrongboard', 'wrongboard', max_age=5, secret=secret2)
      else:
        # create directory for maps, if not already present 
        if not os.path.isdir(megatech.map_dir):
          os.mkdir(megatech.map_dir)

        # uploading file to astech directory
        map_file.save(megatech.map_dir, overwrite=True)
        filestats = os.stat(megatech.map_dir + map_file.filename)
        response.delete_cookie('wrongboard')

        # checking filesize and, if bigger than 1.5M, delete file
        if filestats.st_size > 1500000:
          # page template will show error message with this cookie
          response.set_cookie('bigboard', 'bigboard', max_age=5, secret=secret2)
          os.remove(megatech.map_dir + map_file.filename)
        elif filestats.st_size <= 1500000:
         response.delete_cookie('bigboard')

    sleep(1)
    redirect('/maps')

  elif not username:
    redirect('/login')
# ----------------------------------------


# ----------------------------------------
# ------- SAVEGAMES PAGE -----------------
# ----------------------------------------

# savegame upload form
@get('/saves')
def upload_save():
  username = request.get_cookie('administrator', secret=secret1)
  
  # cookies set when uploaded file is wrong
  # wrong extension
  wrongsave = request.get_cookie('wrongsave', secret=secret2)
  # file over 1M size
  bigsave = request.get_cookie('bigsave', secret=secret2)
  # no file selected
  nosave = request.get_cookie('nosave', secret=secret2)

  if username:
    # current page for become_veteran and become_rookie functions
    response.set_cookie('curpage', '/saves', max_age=321, secret=secret1)

    # create directory for saves if not already present 
    if not os.path.isdir(megatech.save_dir):
      os.mkdir(megatech.save_dir)

    # list of saves, by alphabet (and by date, since datastamp
    # is at the beggining of each file
    savegames = os.listdir(megatech.save_dir)
    savegames.sort()
  
    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret=secret1)

    # render web page with template
    return template('saves', username=username, \
                             veteran=veteran, \
                             savegames=savegames, \
                             wrongsave=wrongsave, \
                             bigsave=bigsave, \
                             nosave=nosave )

  elif not username:
    redirect('/login')
# ----------------------------------------

# checking and uploading files to savegames dir
@post('/saves')
def do_upload_save():
  username = request.get_cookie('administrator', secret=secret1)
  if username:
    save_file = request.files.get('saved_game')

    try:
      name, ext = os.path.splitext(save_file.filename)
      goodsave = True
    except AttributeError:
      # in the case when no file is choosen;
      # page template will show error message with this cookie
      response.set_cookie('nosave', 'nosave', max_age=5, secret=secret2)
      goodsave = False

    if goodsave:
      response.delete_cookie('nosave')
      if ext not in ('.gz'):
        # page template will show error message with this cookie
        response.set_cookie('wrongsave', 'save', max_age=5, secret=secret2)
      else:
        # create directory for saves if not already present 
        if not os.path.isdir(megatech.save_dir):
          os.mkdir(megatech.save_dir)
        # add current time to file name, to avoid
        # incidental overwrites
        save_file.filename = stringTime() + save_file.filename

        # uploading file to astech directory
        save_file.save(megatech.save_dir, overwrite=True)
        filestats = os.stat(megatech.save_dir + save_file.filename)
        response.delete_cookie('wrongsave')

        # checking filesize and, if bigger than 1M, delete file
        if filestats.st_size > 1000000:
          # page template will show error message with this cookie
          response.set_cookie('bigsave', 'bigsave', max_age=5, secret=secret2)
          os.remove(megatech.save_dir + save_file.filename)
        elif filestats.st_size <= 1000000:
         response.delete_cookie('bigsave')

    sleep(1)
    redirect('/saves')

  elif not username:
    redirect('/login')
# ----------------------------------------

# ----------------------------------------
# ------- CUSTOM UNITS PAGE --------------
# ----------------------------------------

# listing custom units and upload form handling
@get('/units')
def upload_units():
  username = request.get_cookie('administrator', secret=secret1)
  
  # cookies set when uploaded file is wrong
  # wrong extension
  wrongunit = request.get_cookie('wrongunit', secret=secret2)
  # file over 1M size
  bigunit = request.get_cookie('bigunit', secret=secret2)
  # no file selected
  nounit = request.get_cookie('nounit', secret=secret2)

  
  if username:
    # current page for become_veteran and become_rookie functions
    response.set_cookie('curpage', '/units', max_age=321, secret=secret1)
    
    # create directory for units if not already present 
    if not os.path.isdir(megatech.unit_dir):
      os.mkdir(megatech.unit_dir)

    # prepare list conatining every file in astech unit directory
    unitfiles = os.listdir(megatech.unit_dir)
    unitfiles.sort()

    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret=secret1)

    # render web page with template
    return template('units', username=username, \
                             veteran=veteran, \
                             unitfiles=unitfiles, \
                             wrongunit=wrongunit, \
                             bigunit=bigunit, \
                             nounit=nounit )

  elif not username:
    redirect('/login')
# ----------------------------------------

# uploading and checking custom units files
@post('/units')
def do_upload_units():
  username = request.get_cookie('administrator', secret=secret1)
  if username:
    unit_file = request.files.get('unit_file')

    try:
      name, ext = os.path.splitext(unit_file.filename)
      goodunit = True
    except AttributeError:
      # in the case when no file is choosen;
      # page template will show error message with this cookie
      response.set_cookie('nounit', 'nounit', max_age=5, secret=secret2)
      goodunit = False

    if goodunit:
      response.delete_cookie('nounit')
      if ext not in ('.mtf'):
        # page template will show error message with this cookie
        response.set_cookie('wrongunit', 'wrongunit', max_age=5, secret=secret2)
      else:
        # create directory for units if not already present 
        if not os.path.isdir(megatech.unit_dir):
          os.mkdir(megatech.unit_dir)

        # uploading file to astech directory
        unit_file.save(megatech.unit_dir, overwrite=True)
        filestats = os.stat(megatech.unit_dir + unit_file.filename)
        response.delete_cookie('wrongunit')

        # checking filesize and, if bigger than 1M, delete file
        if filestats.st_size > 1000000:
          # page template will show error message with this cookie
          response.set_cookie('bigunit', 'bigunit', max_age=5, secret=secret2)
          os.remove(megatech.unit_dir + unit_file.filename)

    sleep(1)
    redirect('/units')

  elif not username:
    redirect('/login')
# ----------------------------------------

# ----------------------------------------
# ----------- OPTIONS PAGE ---------------
# ----------------------------------------

@route('/options')
def options():
  username = request.get_cookie('administrator', secret=secret1)

  if username:
    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret=secret1)

    response.set_cookie('curpage', '/options', max_age=321, secret=secret1)
  
    username = request.get_cookie('administrator', secret=secret1)
    
    # list of avaiable MegaMek versions
    versions = []
    # cutting 'megamek-(v)' prefix
    for i in os.listdir(megatech.meks_dir):
      # skip "megamek-"
      versions.append(i[8:])
    versions.sort()

    # we are checking which version is currently selected
    selected = megatech.version
   
    return template('options', username=username, \
                               veteran=veteran, \
                               versions=versions, \
                               selected=selected) 
  
  elif not username:
    redirect('/login')

# ----------------------------------------
# Little routes that call functions.

# turn on MegaMek server via MegaTech class
@route('/mmturnon')
def mmturnon():
  if request.get_cookie('administrator', secret=secret1):
    print(megatech.version)
    megatech.start()
  redirect('/')
# ----------------------------------------


# turn off MegaMek server via MegaTech class
@route('/mmturnoff')
def mmturnoff():
  if request.get_cookie('administrator', secret=secret1):
    megatech.stop()
  redirect('/')
# ----------------------------------------


# logout from astech
@route('/logout')
def logoff():
  response.delete_cookie('administrator')
  redirect('/login')
# ----------------------------------------


# set vetran cookie to hide tutorial messages
@route('/veteran')
def becomeVeteran():
  if request.get_cookie('administrator', secret=secret1):
    response.set_cookie('veteran', 'veteran', secret=secret1)
  # curpage cookie is storing current page (route)
  redirect(request.get_cookie('curpage', secret=secret1))
# ----------------------------------------


# delete veteran cookie to show tutorial messages 
@route('/green')
def becomeGreen():
  if request.get_cookie('administrator', secret=secret1):
    response.delete_cookie('veteran')
  # curpage cookie is storing current page (route)
  redirect(request.get_cookie('curpage', secret=secret1))
# ----------------------------------------

# change MegaMek version
@route('/ver/<vernumber>')
def changeVer(vernumber):
  '''Changes version info in MegaTech instance
  and installs version of MegaMek'''
  megatech.version = vernumber
  
  # stop current MegaMek instance 
  megatech.stop()

  # updating astech.conf file
  megatech.writeConfig()
  megatech.getConfig()

  # curpage cookie is storing current page (route)
  redirect(request.get_cookie('curpage', secret=secret1))
# ----------------------------------------

# 404 error page
@error(404)
def route404(error):
  '''Page not found page.'''
  username = request.get_cookie('administrator', secret=secret1)

  if username:
    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret=secret1)

    response.set_cookie('curpage', '404', max_age=1234, secret=secret1)
  
    username = request.get_cookie('administrator', secret=secret1)
    return template('error404', username=username, \
                                veteran=veteran)
  elif not username:
    redirect('/login')
# ----------------------------------------



# ----------------------------------------
# ----- ALL SYSTEMS... NOMINAL -----------
# ----------------------------------------
# main debug loop
# remember to add debug import from bottle
debug(True)
run(host='localhost', port=8080, reloader=True)

# main production loop
# remember to delete debug import from bottle
#run(host='0.0.0.0', port=8080)

