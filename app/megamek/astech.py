#!/usr/bin/python3
'''Megamek server administration page.
This is ALPHA quality software,
expect some bugs and glitches.
author: Łukasz Posadowski,  mail [at] lukaszposadowski.pl'''

# import subprocess, for launching jar files
import subprocess

# sleep may help with subprocess,
from time import sleep

# import bottle
# remember to delete debug for production
from bottle import template, response, request, get, post, error, \
                   redirect, static_file, run, route, debug

# file uploading and listing directories
# I'll try to use pathlib.Path over os.path, when possible.
import os
# from pathlib import Path

# we have to append date to filenames 
import time 


# ----------------------------------------
# ------- HELPER FUNCTIONS ---------------
# ----------------------------------------

# megamek log files into lists
def getFile(filename):
  '''filename -> list of last 81 lines'''
  with open(filename,'r') as myfile:
    mylines = myfile.readlines()
    # we need just 81 last lines
    lastlog = mylines[len(mylines)-81 : len(mylines)]
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
 if l == 'somelogin' and p == 'somepassword':
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
    self.ison = False                          # megamek is off by default 
    self.version = '0.43.2'                    # megamek version
    self.port = 3477                           # port for megamek server
    self.domain = 'some.server.com'            # nice site name
    self.password = False                      # optional password to change game options 
    self.save_dir = './savegames/'             # default save dir for megamek
    self.map_dir = './data/boards/astech/'     # astech will upload maps there
    self.unit_dir = './data/mechfiles/astech/' # and custom mechs there

  def start(self):
    '''starts MegaMek server'''
    # if password is set, add it to the lauch command
    if self.password != False:
      self.command = '/usr/java/default/bin/java -jar MegaMek.jar -dedicated -port ' + \
                     str(self.port) + ' -password ' + str(self.password) + ' '
    elif self.password == False:
      self.command = '/usr/java/default/bin/java -jar MegaMek.jar -dedicated -port ' + str(self.port)
    
    # start MegaMek dedicated server with parameters
    self.process = subprocess.Popen(self.command.split()) 
    
    # TODO testing parameters to load save games - not ready yet
    # dedicated servers parameters are as follows:
    # -port [port] -password [password] [savedgame]

    # we're sleeping, while wainting for Megamek to write to a log file
    sleep(1)

    self.ison = True
  
  def stop(self):
    '''stops MegaMek server'''
    if self.ison == True:
      self.process.kill()
      # self.password = False
      self.ison = False
  
megatech = MegaTech()
# ----------------------------------------


# below is bottle.py related stuff

# ----------------------------------------
# ------- STATIC FILES -------------------
# ----------------------------------------

# site logo and other images
@route('/image/<filename>')
def image(filename):
  return static_file(filename, root='./img/', mimetype='image/png')


# download static files
@route('/download/<filetype>/<filename>')
def downloadfile(filetype, filename):
  # check if we are logged in before download, to prevent link guessing
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  if username:
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
  

# remove static files
@route('/remove/<filetype>/<filename>')
def removefile(filetype, filename):
  # check if we are logged in before download, to prevent link guessing
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  if username:
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
    os.remove(rootdir + filename)
    # and quickly return to the maps/saves/units/ page
    redirect(request.get_cookie('curpage', secret='sseeccrreett11'))
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
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  # cookie with information about bad password
  bad_password = request.get_cookie('badPassword', secret='sseeccrreett22')
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
      response.set_cookie('administrator', username, max_age=87654, secret='sseeccrreett11')
      response.delete_cookie('badPassword')
      redirect('/')
    elif not crede(username,password):
      # bad password
      response.set_cookie('badPassword', 'nopass', max_age=21, secret='sseeccrreett22')
      redirect('/login')
  else:
    # if login and/or password are not alpha, don't parse them
    # and redirect to login (just to be safe)
    response.set_cookie('badPassword', 'nopass', max_age=21, secret='sseeccrreett22')
    redirect('/login')
# ----------------------------------------


# ----------------------------------------
# ------- MAIN PAGE ----------------------
# ----------------------------------------

# main route
@get('/')
def administrator():
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  noalpha = request.get_cookie('noalpha', secret='sseeccrreett22')

  # checks if help messages will be displayed
  veteran = request.get_cookie('veteran', secret='sseeccrreett11')

  # current page for become_veteran and become_rookie functions
  response.set_cookie('curpage', '/', max_age=1234, secret='sseeccrreett11')

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
                                     noalpha = noalpha )

  elif not username:
    redirect('/login')

# main route - setting server password via html form
@post('/')
def setMekPassword():
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  
  if username:
    # check if username and password isn't something like '/mmrestart'
    game_pass = request.forms.get('mekpassword')
    if game_pass.isalpha():
      megatech.password = game_pass
      redirect('/')
    else:
      # if mekpassword is not alpha, don't parse it
      response.set_cookie('noalpha', 'noalpha', max_age=21, secret='sseeccrreett22')
      game_pass = False
      megatech.password = False
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
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  wrongboard = request.get_cookie('wrongboard', secret='sseeccrreett22')
  bigboard = request.get_cookie('bigboard', secret='sseeccrreett22')
  
  if username:
    # current page for become_veteran and become_rookie functions
    response.set_cookie('curpage', '/maps', max_age=321, secret='sseeccrreett11')

    # create directory for maps, if not already present 
    if not os.path.isdir(megatech.map_dir):
      os.mkdir(megatech.map_dir)

    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret='sseeccrreett11')

    return template('maps', username=username, \
                            veteran=veteran, \
                            mapfiles=os.listdir(megatech.map_dir), \
                            wrongboard=wrongboard, \
                            bigboard=bigboard)
  elif not username:
    redirect('/login')
# ----------------------------------------

# checking and uploading files to ./data/maps/astech dir
@post('/maps')
def do_upload_map():
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  if username:
    map_file = request.files.get('map_file')
    name, ext = os.path.splitext(map_file.filename)
    if ext not in ('.board'):
      # page template will show error message with this cookie
      response.set_cookie('wrongboard', 'wrongboard', max_age=21, secret='sseeccrreett22')
    else:
      # create directory for maps, if not already present 
      if not os.path.isdir(megatech.map_dir):
        os.mkdir(megatech.map_dir)

      # uploading file to astech directory
      map_file.save(megatech.map_dir, overwrite=True)
      filestats = os.stat(megatech.map_dir + map_file.filename)
      response.delete_cookie('wrongboard')

      # checking filesize and, if bigger than 1M, delete file
      if filestats.st_size > 1000000:
        # page template will show error message with this cookie
        response.set_cookie('bigboard', 'bigboard', max_age=21, secret='sseeccrreett22')
        os.remove(megatech.map_dir + map_file.filename)
      elif filestats.st_size <= 1000000:
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
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  wrongsave = request.get_cookie('wrongsave', secret='sseeccrreett22')
  bigsave = request.get_cookie('bigsave', secret='sseeccrreett22')

  if username:
    # current page for become_veteran and become_rookie functions
    response.set_cookie('curpage', '/saves', max_age=321, secret='sseeccrreett11')

    # create directory for saves if not already present 
    if not os.path.isdir(megatech.save_dir):
      os.mkdir(megatech.save_dir)
  
    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret='sseeccrreett11')

    return template('saves', username=username, \
                             veteran=veteran, \
                             # TODO create dir if not exist
                             savegames=os.listdir(megatech.save_dir), \
                             wrongsave=wrongsave, \
                             bigsave=bigsave, )

  elif not username:
    redirect('/login')
# ----------------------------------------

# checking and uploading files to savegames dir
@post('/saves')
def do_upload_save():
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  if username:
    save_file = request.files.get('saved_game')

    # check if file extension is .gz
    name, ext = os.path.splitext(save_file.filename)
    if ext not in ('.gz'):
      # page template will show error message with this cookie
      response.set_cookie('wrongsave', 'save', max_age=21, secret='sseeccrreett22')
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
        response.set_cookie('bigsave', 'bigsave', max_age=21, secret='sseeccrreett22')
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
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  wrongunit = request.get_cookie('wrongunit', secret='sseeccrreett22')
  bigunit = request.get_cookie('bigunit', secret='sseeccrreett22')
  
  if username:
    # current page for become_veteran and become_rookie functions
    response.set_cookie('curpage', '/units', max_age=321, secret='sseeccrreett11')

    # create directory for units if not already present 
    if not os.path.isdir(megatech.unit_dir):
      os.mkdir(megatech.unit_dir)

    # prepare list conatining every file in astech unit directory
    unitfiles = os.listdir(megatech.unit_dir)
    unitfiles.sort()

    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret='sseeccrreett11')
    return template('units', username=username, \
                             veteran=veteran, \
                             unitfiles=unitfiles, \
                             wrongunit=wrongunit, \
                             bigunit=bigunit )
  elif not username:
    redirect('/login')
# ----------------------------------------

# uploading and checking custom units files
@post('/units')
def do_upload_units():
  username = request.get_cookie('administrator', secret='sseeccrreett11')
  if username:
    unit_file = request.files.get('unit_file')
    name, ext = os.path.splitext(unit_file.filename)
    if ext not in ('.mtf'):
      # page template will show error message with this cookie
      response.set_cookie('wrongunit', 'wrongunit', max_age=21, secret='sseeccrreett22')
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
        response.set_cookie('bigunit', 'bigunit', max_age=21, secret='sseeccrreett22')
        os.remove(megatech.unit_dir + unit_file.filename)

    sleep(1)
    redirect('/units')
  elif not username:
    redirect('/login')
# ----------------------------------------


# Little routes that call functions.

# turn on MegaMek server via MegaTech class
@route('/mmturnon')
def mmturnon():
  if request.get_cookie('administrator', secret='sseeccrreett11'):
    megatech.start()
  redirect('/')
# ----------------------------------------


# turn off MegaMek server via MegaTech class
@route('/mmturnoff')
def mmturnoff():
  if request.get_cookie('administrator', secret='sseeccrreett11'):
    megatech.stop()
  redirect('/')
# ----------------------------------------


# logout from astech
@route('/logout')
def logoff():
  response.delete_cookie('administrator')
  redirect('/')
# ----------------------------------------


# set vetran cookie to hide tutorial messages
@route('/veteran')
def become_veteran():
  if request.get_cookie('administrator', secret='sseeccrreett11'):
    response.set_cookie('veteran', 'veteran', secret='sseeccrreett11')
  # curpage cookie is storing current page (route)
  redirect(request.get_cookie('curpage', secret='sseeccrreett11'))
# ----------------------------------------


# delete veteran cookie to show tutorial messages 
@route('/green')
def become_green():
  if request.get_cookie('administrator', secret='sseeccrreett11'):
    response.delete_cookie('veteran')
  # curpage cookie is storing current page (route)
  redirect(request.get_cookie('curpage', secret='sseeccrreett11'))
# ----------------------------------------


# 404 error page
@error(404)
def route404(error):
  username = request.get_cookie('administrator', secret='sseeccrreett11')

  if username:
    # checks if help messages will be displayed
    veteran = request.get_cookie('veteran', secret='sseeccrreett11')

    response.set_cookie('curpage', '404', max_age=1234, secret='sseeccrreett11')
  
    username = request.get_cookie('administrator', secret='sseeccrreett11')
    return template('error404', username=username, \
                                veteran=veteran)
  elif not username:
    redirect('/login')
# ----------------------------------------


# ----------------------------------------
# main debug loop
# remember to add debug import from bottle
debug(True)
run(host='localhost', port=8080, reloader=True)

# main production loop
# remember to delete debug import from bottle
#run(host='0.0.0.0', port=8080)

