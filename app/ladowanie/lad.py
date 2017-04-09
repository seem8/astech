#!/home/lukasz/progi/python/astech/bin/python3

import os
from bottle import template, response, request, get, post, redirect, static_file, run, route, debug 

@get('/ladowacz')
def ladowywacz():
  return template('lad')

@post('/ladowacz')
def zaladowywacz():
  ladunek = request.files.get('lload')
  ladunek.save(os.path.curdir)

debug(True)
run(host='localhost', port=8080)

