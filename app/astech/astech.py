#!/usr/bin/python3
'''
Megamek server administration page.
This is ALPHA quality software (even after so much time),
so expect some bugs and glitches.
'''

# ----------------------------------------
# ------- IMPORT MODULES -----------------
# ----------------------------------------

# launching MegaMek from jar files
import subprocess

# using ENV from "podman run"
import os

# save and open files for MegaMek
import pathlib

# append date to filenames and
# wait between unsuccesfull login attempts
import time

# password hashing
import hashlib

# cookie secrets
import string
import random
random.seed()

# import bottle
from bottle import template, response, request, get, post, error, \
                   redirect, static_file, run, route


# ----------------------------------------
# ------- INITIAL CONFIGURATION ----------
# ----------------------------------------

# Bottle can run in debug mode
AST_DEBUG = os.environ.get("AST_DEBUG")
if AST_DEBUG:
  from bottle import debug

# MegaMek version
AST_MM_VERSION = os.environ.get("AST_MM_VERSION")

# get MegaMek port from ENV, or set it as 2346
AST_MM_PORT = os.environ.get("AST_MM_PORT")
if not AST_MM_PORT:
  AST_MM_PORT = 2346

# get user from ENV, or set it as 'kerensky'
AST_USER = os.environ.get("AST_USER")
if not AST_USER:
  AST_USER = 'kerensky'

# get password from ENV, or set it as 'sldf';
# TODO this ENV variable will still be plain text in container init/systemd unit file,
# it's just avoid keeping plain text password in containers memory all the time
PLAINPASS = os.environ.get("AST_PASS")
if PLAINPASS:
  AST_PASS = hashlib.sha512(PLAINPASS.encode()).hexdigest()
  del PLAINPASS
else:
  AST_PASS = hashlib.sha512('sldf'.encode()).hexdigest()

# set secrets for cookiess;
# restarting application will - almost certainly - force users to login again
SECRET1 = \
  ''.join(random.choices(string.ascii_letters + string.digits, k=34+random.randint(0,8)))
SECRET2 = \
  ''.join(random.choices(string.ascii_letters + string.digits, k=34+random.randint(0,8)))


# ----------------------------------------
# ------- HELPER FUNCTIONS ---------------
# ----------------------------------------

# convert megamek log files into lists
def getFile(filename):
  '''filename -> reversed list of last 81 lines'''
  # log file doesn't exist by default in MegaMek
  try:
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
    # in Bottle templates it is interpreted by SPACE character, which is
    # capable to break like if necessary (werid, but it works);
    # TODO it adds spaces into a log file view
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
# password encryption is nice, but useless without https;
# defaults are user: 'kerensky', password: 'sldf'
def crede(u, p):
  '''check credentials'''
  if u == AST_USER:
    if hashlib.sha512(p.encode()).hexdigest() == AST_PASS:
      time.sleep(random.randint(1,2))
      return True
    time.sleep(random.randint(1,2))
    return False
  time.sleep(random.randint(1,2))
  return False
# ----------------------------------------


# ----------------------------------------
# ------- MAIN LOGIC ---------------------
# ----------------------------------------

# MegaMek server stuff
class MegaTech:
  '''MegaMek server controls and status'''
  def __init__(self):

    self.version = AST_MM_VERSION     # megamek version
    self.port = AST_MM_PORT           # port number for MegaMek

    self.ison = False                 # MegaMek is off during __init__
    self.process = False              # to check if MegaMek is running

    # "shortcuts" for various directories
    self.mek_dir = f'./megamek-{self.version}'                 # MegaMek directory

    self.save_dir = f'{self.mek_dir}/savegames/'               # default save dir for megamek
    self.maps_dir = f'{self.mek_dir}/data/boards/astech/'      # astech will upload maps there
    self.unit_dir = f'{self.mek_dir}/data/mechfiles/astech/'   # and custom mechs there
    self.logs_dir = f'{self.mek_dir}/logs/'                    # gamelogs are there

  def start(self):
    '''starts MegaMek server'''
    # we don't want server duplicates
    if self.ison:
      return False

    # command to run MegaMek headless server
    command = f'/usr/bin/java -jar MegaMek.jar -dedicated -port {self.port}'

    # we're running server now
    self.process = subprocess.Popen(command.split(), cwd=self.mek_dir)
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
  username = request.get_cookie('administrator', secret=SECRET1)
  if username:
    # filetype define directory with files to download
    if filetype == 'map':
      rootdir = megatech.maps_dir
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
        redirect(request.get_cookie('curpage', secret=SECRET1))
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
  username = request.get_cookie('administrator', secret=SECRET1)

  if username:
    # redirect logged users to main page
    redirect('/')
    return True

  # cookie with information about bad password
  badPassword = request.get_cookie('badPassword', secret=SECRET2)
  return template('login',
                  badPassword=badPassword,
                  username=username,
                  AST_DEBUG=AST_DEBUG,
                  )
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
      response.set_cookie('administrator', username, secret=SECRET1)
      response.delete_cookie('badPassword')
      redirect('/')
    elif not crede(username, password):
      # bad password
      response.set_cookie('badPassword', 'nopass', max_age=5, secret=SECRET2)
      redirect('/login')
  else:
    # if login and/or password are not alpha, don't parse them
    # and redirect to login (just to be safe)
    response.set_cookie('badPassword', 'nopass', max_age=5, secret=SECRET2)
    redirect('/login')
# ----------------------------------------


# ----------------------------------------
# ------- MAIN PAGE ----------------------
# ----------------------------------------

# main route
@get('/')
def index():
  # check if we are logged in
  username = request.get_cookie('administrator', secret=SECRET1)

  # checks if help messages will be displayed
  veteran = request.get_cookie('veteran', secret=SECRET1)

  # current page
  response.set_cookie('curpage', '/', secret=SECRET1)

  if username:
    # password and login cookie are checked by now
    response.delete_cookie('badPassword')

    # check if MegaMek is on and correct megatech.ison
    if megatech.check():
      megatech.ison = True
    elif not megatech.check():
      megatech.ison = False

    # render template
    return template('index',
                    username = username,
                    veteran = veteran,
                    mtison = megatech.ison,
                    mtver = megatech.version,
                    mtport = megatech.port,
                    logFile = getFile(megatech.logs_dir + 'megamek.log'),
                    AST_DEBUG=AST_DEBUG,
                    )

  elif not username:
    redirect('/login')
# ----------------------------------------


# ----------------------------------------
# ------- USER FILES PAGE ----------------
# ----------------------------------------

# files view and upload form 
@get('/gamefiles')
def list_user_files():
  username = request.get_cookie('administrator', secret=SECRET1)

  if username:
    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret=SECRET1)

    # current page for become_veteran and become_rookie functions
    response.set_cookie('curpage', '/gamefiles', secret=SECRET1)

    # create diretories, if they not exist
    pathlib.Path(megatech.maps_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(megatech.unit_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(megatech.save_dir).mkdir(parents=True, exist_ok=True)

    # specify directories with user files
    map_list = os.listdir(megatech.maps_dir)
    unit_list = os.listdir(megatech.unit_dir)
    save_list = os.listdir(megatech.save_dir)

    map_list.sort()
    unit_list.sort()
    save_list.sort()

    # cookies set when uploaded file is wrong
    wrongfile = request.get_cookie('wrongfile', secret=SECRET2)
    bigfile = request.get_cookie('bigfile', secret=SECRET2)
    nofile = request.get_cookie('nofile', secret=SECRET2)
    longname = request.get_cookie('longname', secret=SECRET2)

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
                     AST_DEBUG=AST_DEBUG,
                     )

  elif not username:
    redirect('/login')
# ----------------------------------------


# checking and uploading files
@post('/gamefiles')
def upload_file():
  username = request.get_cookie('administrator', secret=SECRET1)
  if username:
    posted_file = request.files.get('posted_file')

    try:
      name, ext = os.path.splitext(posted_file.filename)
    except AttributeError:
      # in a case when no file was uploaded;
      # page template will show error message with this cookie
      response.set_cookie('nofile', 'nofile', max_age=5, secret=SECRET2)
      redirect(request.get_cookie('curpage', secret=SECRET1))
      return False

    if len(name) > 80:
      response.set_cookie('longname', 'longname', max_age=5, secret=SECRET2)
      redirect(request.get_cookie('curpage', secret=SECRET1))
      return False

    response.delete_cookie('nofile')
    # specify correct path to save uploaded file and filesize limit
    if ext == '.board':
      file_path = megatech.maps_dir
      size_limit = 1500000
    elif ext == '.mtf':
      file_path = megatech.unit_dir
      size_limit = 1500000
    elif ext == '.gz':
      file_path = megatech.save_dir
      size_limit = 1500000
    else:
      # page template will show error message with this cookie
      response.set_cookie('wrongfile', 'wrongfile', max_age=5, secret=SECRET2)
      redirect(request.get_cookie('curpage', secret=SECRET1))
      return False

    # uploading and checking file in correct MegaMek directory
    posted_file.save(file_path, overwrite=True)
    filestats = os.stat(file_path + posted_file.filename)
    response.delete_cookie('wrongfile')

    # checking filesize and, if bigger than size limit, delete file
    if filestats.st_size > size_limit:
      # page template will show error message with this cookie
      response.set_cookie('bigfile', 'bigfile', max_age=5, secret=SECRET2)
      os.remove(file_path + posted_file.filename)
    else:
      response.delete_cookie('bigfile')

    # sometimes os.listdir isn't including new file right away
    time.sleep(1)
    redirect(request.get_cookie('curpage', secret=SECRET1))

  elif not username:
    redirect('/login')
# ----------------------------------------


# ----------------------------------------
# ----------- OPTIONS PAGE ---------------
# ----------------------------------------

@route('/options')
def options():
  username = request.get_cookie('administrator', secret=SECRET1)

  if username:
    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret=SECRET1)

    response.set_cookie('curpage', '/options', secret=SECRET1)

    return template('options',
                    username=username,
                    veteran=veteran,
                    AST_DEBUG=AST_DEBUG,
                   )

  elif not username:
    redirect('/login')

# ----------------------------------------
# Little routes that call functions.

# turn on MegaMek server via MegaTech class
@route('/mmturnon')
def mmturnon():
  if request.get_cookie('administrator', secret=SECRET1):
    megatech.start()
    time.sleep(4)
  redirect('/')
# ----------------------------------------


# turn off MegaMek server via MegaTech class
@route('/mmturnoff')
def mmturnoff():
  if request.get_cookie('administrator', secret=SECRET1):
    megatech.stop()
    time.sleep(2)
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
  if request.get_cookie('administrator', secret=SECRET1):
    response.set_cookie('veteran', 'veteran', secret=SECRET1)
  # curpage cookie is storing current page (route)
  redirect(request.get_cookie('curpage', secret=SECRET1))
# ----------------------------------------


# delete veteran cookie to show tutorial messages 
@route('/green')
def becomeGreen():
  if request.get_cookie('administrator', secret=SECRET1):
    response.delete_cookie('veteran')
  # curpage cookie is storing current page (route)
  redirect(request.get_cookie('curpage', secret=SECRET1))
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

# main loop
if AST_DEBUG:
  debug(True)
  run(host='0.0.0.0', port=8080, reloader=True)
else:
  run(host='127.0.0.1', port=8080)

