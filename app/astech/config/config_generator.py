#!/usr/bin/python3
'''
config generator app for Astech
'''

# we are dumping dictiorany to a file
import pickle

# we will hash the password
import hashlib

# we need a little random string for signed cookies
import string
import random
random.seed()

# ---------------------------------------
# dumb initial configutarion 
conf =   {
         'name': '',
         'version': '',
         'port': 2346,
         'game_password': False,
         }
crede =  {
         'user': '',
         'pass': '',
         }
secret = {
         'alpha': '',
         'beta': '',
         }
bottle = {
         'port': '8080',
         'debug': 'n',
         'domain': 'some.server.com',
         }
# ---------------------------------------
# now we are making real one
name = input('Server name: ')
version = input('MegaMek version: ')
port = input('MegaMek port: ')
user = input('Astech username: ')
password = input('Astech password: ')
server_domain = input('Server web address: ')
server_port = input('Bottle port: ')
server_debug = input('Use Bottle debug mode? [y/n] ')

# we have all the data we need
print('--- saving configuration ---')

# ---------------------------------------
conf['name'] = name
conf['version'] = version
conf['port'] = int(port)

crede['user'] = user
crede['pass'] = hashlib.sha512(password.encode()).hexdigest()

bottle['domain'] = server_domain
bottle['port'] = server_port
bottle['debug'] = server_debug

# dumping name, version and port
with open('astech.conf', 'w+b') as confile:
  pickle.dump(conf, confile, protocol=0)

# dumping user and password
with open('astech.crede', 'w+b') as credefile:
  pickle.dump(crede, credefile, protocol=0)

# dumping bottle config
with open('astech.bottle', 'w+b') as bottlefile:
  pickle.dump(bottle, bottlefile, protocol=0)

# generating random strings for signed cookiess
secret['alpha'] = ''.join(random.choices(string.ascii_letters + string.digits,
                                   k=34+random.randint(0,8)))
secret['beta'] = ''.join(random.choices(string.ascii_letters + string.digits,
                                   k=34+random.randint(0,8)))

# dumping cookie confing file
with open('astech.cookie', 'w+b') as cookiefile:
  pickle.dump(secret, cookiefile, protocol=0)
# ---------------------------------------
# ok
print('--- config is ready. ---')

