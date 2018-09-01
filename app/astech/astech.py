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

# file creating, uploading and listing directories
import os
import pathlib

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
    # we need just 300 last lines
    lastlog = mylines[len(mylines)-300 : len(mylines)]
    lastlog.reverse()

    # sometimes the word in file is too long to fit inside template div,
    # so I'm inserting '\n' all over the lines;
    # in tpl it is interpreted by SPACE character, which is capable to
    # break like if necessary (werid, but it works);
    # TODO it adds verid looking spaces into a log file view
    for line_number in range(len(lastlog)):
      line = list(lastlog[line_number])

      try:
        for column in (101, 152, 203, 254, 305, 356, 407, 458, 509):
          line.insert(column, '\n')
      except IndexError:
        pass

      lastlog[line_number] = ''.join(line)

    return lastlog
# ----------------------------------------

# get a string from localtime
def stringTime():
  '''returns string: year-month-day__hour-minute-second__'''
  t = time.localtime()
  return f'{t[0]}-{t[1]}-{t[2]}__{t[3]}-{t[4]}-{t[5]}__'
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
with open('config/astech.cookie', 'r+b') as secrets:
  cookies = pickle.load(secrets)
  secret1 = cookies['alpha']
  secret2 = cookies['beta']


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
    self.meks_dir = './megamek/installed'       # avaiable versions of Megamek
    self.archive_dir = './megamek/archives'     # downloaded versions of MegaMek

    self.install_dir = f'{self.meks_dir}/megamek-{self.version}'   # megamek directory
    self.save_dir = f'{self.install_dir}/savegames/'               # default save dir for megamek
    self.map_dir = f'{self.install_dir}/data/boards/astech/'       # astech will upload maps there
    self.unit_dir = f'{self.install_dir}/data/mechfiles/astech/'   # and custom mechs there
    self.logs_dir = f'{self.install_dir}/logs/'                    # gamelogs are there

  def start(self):
    '''starts MegaMek server'''
    # we don't want server duplicates
    if self.ison:
      return False

    javabin = '/usr/java/default/bin/java'

    # command to run MegaMek headless server
    command = f'{javabin} -jar MegaMek.jar -dedicated -port {str(self.port)}'

    # add password if present
    if self.game_password and self.game_password != '':
      command += f' -p {self.game_password}'

    # we're running server now
    self.process = subprocess.Popen(command.split(), cwd=self.install_dir)
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
    self.install_dir = f'{self.meks_dir}/megamek-{self.version}'   # megamek directory
    self.save_dir = f'{self.install_dir}/savegames/'               # default save dir for megamek
    self.map_dir = f'{self.install_dir}/data/boards/astech/'       # astech will upload maps there
    self.unit_dir = f'{self.install_dir}/data/mechfiles/astech/'   # and custom mechs there
    self.logs_dir = f'{self.install_dir}/logs/'                    # gamelogs are there


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


# download and remove user uploaded files
@route('/files/<operation>/<filetype>/<filename>')
def file_operations(operation, filetype, filename):
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
      # 404page leads to nothing, so it will return 404 error page
      redirect('/404page')
      return False

    if operation == 'download':
      # force download
      return static_file(filename, root=rootdir, download=filename)
    elif operation == 'remove':
      # remove the file
      try:
        os.remove(rootdir + filename)
        # os.remove is displaying blank page, so we have to
        # quickly return to maps, saves, or units page
        redirect(request.get_cookie('curpage', secret=secret1))
        return True
      except FileNotFoundError:
        redirect('/404page')
        return False
    else:
      redirect('/404page')
      return False

  elif not username:
    # if we're not logged, show login page
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

  if username:
    # redirect logged users to main page
    redirect('/')
    return True

  # cookie with information about bad password
  bad_password = request.get_cookie('badPassword', secret=secret2)
  return template('login', badPass=bad_password, username=username)
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
      # good password, give a cookie
      response.set_cookie('administrator', username, secret=secret1)
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
def index():
  # check if we are logged in
  username = request.get_cookie('administrator', secret=secret1)

  # check game password
  passwordnoalpha = request.get_cookie('passwordnoalpha', secret=secret2)
  passwordtoolong = request.get_cookie('passwordtoolong', secret=secret2)

  # checks if help messages will be displayed
  veteran = request.get_cookie('veteran', secret=secret1)

  # current page
  response.set_cookie('curpage', '/', secret=secret1)

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
    return template('administrator',
                    username = username,
                    veteran = veteran,
                    mtison = megatech.ison,
                    mtver = megatech.version,
                    mtname = megatech.name,
                    mtport = str(megatech.port),
                    mtdomain = megatech.domain,
                    logFile = getFile(megatech.logs_dir + 'megameklog.txt'),
                    mtpassword = megatech.game_password,
                    passwordnoalpha = passwordnoalpha,
                    passwordtoolong = passwordtoolong,
                    )

  elif not username:
    redirect('/login')

# main route - setting server password via html form
@post('/')
def index_set_password():
  username = request.get_cookie('administrator', secret=secret1)

  if username:
    game_pass = request.forms.get('mekpassword')

    if len(game_pass) > 0 and not game_pass.isalpha():
      # if mekpassword is not alpha, don't parse it;
      # will display warning message about using nonlatin characters, see administrator.tpl
      response.delete_cookie('passwordtoolong')
      response.set_cookie('passwordnoalpha', 'passwordnoalpha', max_age=5, secret=secret2)
      megatech.game_password = False

    elif len(game_pass) > 100:
      # it may be too much for MegaMek
      response.delete_cookie('passwordnoalpha')
      response.set_cookie('passwordtoolong', 'passwordtoolong', max_age=5, secret=secret2)
      megatech.game_password = False

    else:
      if game_pass == '':
        # empty password is no password
        megatech.game_password = False
      else:
        megatech.game_password = game_pass
      response.delete_cookie('passwordnoalpha')
      response.delete_cookie('passwordtoolong')


    # refreshing config file
    megatech.writeConfig()
    megatech.getConfig()

    redirect('/')

  elif not username:
    redirect('/login')
# ----------------------------------------

# ----------------------------------------
# ------- USER FILES PAGE ----------------
# ----------------------------------------

# files view and upload form 
@get('/gamefiles')
def list_user_files():
  username = request.get_cookie('administrator', secret=secret1)

  if username:
    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret=secret1)

    # current page for become_veteran and become_rookie functions
    response.set_cookie('curpage', '/gamefiles', secret=secret1)

    # create diretories, if they not exist
    pathlib.Path(megatech.map_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(megatech.unit_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(megatech.save_dir).mkdir(parents=True, exist_ok=True)

    # specify directories with user files
    map_list = os.listdir(megatech.map_dir)
    unit_list = os.listdir(megatech.unit_dir)
    save_list = os.listdir(megatech.save_dir)

    map_list.sort()
    unit_list.sort()
    save_list.sort()

    # cookies set when uploaded file is wrong
    wrongfile = request.get_cookie('wrongfile', secret=secret2)
    bigfile = request.get_cookie('bigfile', secret=secret2)
    nofile = request.get_cookie('nofile', secret=secret2)
    longname = request.get_cookie('longname', secret=secret2)

    # render web page with template
    return template('gamefiles',
                     username=username,
                     veteran=veteran,
                     map_list=map_list,
                     unit_list=unit_list,
                     save_list=save_list,
                     wrongfile=wrongfile,
                     bigfile=bigfile,
                     nofile=nofile,
                     longname=longname,
                     )

  elif not username:
    redirect('/login')
# ----------------------------------------


# checking and uploading files
@post('/gamefiles')
def upload_file():
  username = request.get_cookie('administrator', secret=secret1)
  if username:
    posted_file = request.files.get('posted_file')

    try:
      name, ext = os.path.splitext(posted_file.filename)
    except AttributeError:
      # in a case when no file was uploaded;
      # page template will show error message with this cookie
      response.set_cookie('nofile', 'nofile', max_age=5, secret=secret2)
      redirect(request.get_cookie('curpage', secret=secret1))
      return False

    if len(name) > 80:
      response.set_cookie('longname', 'longname', max_age=5, secret=secret2)
      redirect(request.get_cookie('curpage', secret=secret1))
      return False

    response.delete_cookie('nofile')
    # specify correct path to save uploaded file and filesize limit
    if ext == '.board':
      file_path = megatech.map_dir
      size_limit = 1500000
    elif ext == '.mtf':
      file_path = megatech.unit_dir
      size_limit = 1500000
    elif ext == '.gz':
      file_path = megatech.save_dir
      size_limit = 1500000
    else:
      # page template will show error message with this cookie
      response.set_cookie('wrongfile', 'wrongfile', max_age=5, secret=secret2)
      redirect(request.get_cookie('curpage', secret=secret1))
      return False

    # uploading and checking file in correct MegaMek directory
    posted_file.save(file_path, overwrite=True)
    filestats = os.stat(file_path + posted_file.filename)
    response.delete_cookie('wrongfile')

    # checking filesize and, if bigger than size limit, delete file
    if filestats.st_size > size_limit:
      # page template will show error message with this cookie
      response.set_cookie('bigfile', 'bigfile', max_age=5, secret=secret2)
      os.remove(file_path + posted_file.filename)
    else:
      response.delete_cookie('bigfile')

    # sometimes os.listdir isn't including new file right away
    time.sleep(1)
    redirect(request.get_cookie('curpage', secret=secret1))

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

    response.set_cookie('curpage', '/options', secret=secret1)

    # list of avaiable MegaMek versions
    versions = []
    # cutting 'megamek-(v)' prefix
    for i in os.listdir(megatech.meks_dir):
      if os.path.isdir(i):
        # skip "megamek-"
        versions.append(i[8:])
    versions.sort()

    # we are checking which version is currently selected
    selected = megatech.version

    return template('options',
                    username=username,
                    veteran=veteran,
                    versions=versions,
                    selected=selected,
                   )

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
  return template('error404')
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

