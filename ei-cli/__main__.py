#!/usr/bin/env python3

import os
import logging
import sys
import cli

def get_config_dir():
  _config_dir = os.getenv("EI_CLI_HOME", os.path.join(os.getenv("HOME"), ".ei"))
  return _config_dir

def configure_logging(log_path, level):
  if not os.path.exists(os.path.dirname(log_path)):
    try:
      os.makedirs(os.path.dirname(log_path), exist_ok=True)
    except:
      print("[ERROR]: Failed to create log directory", log_path)
  elif (os.path.exists(log_path) and not os.access(log_path, os.W_OK)) or not os.access(os.path.dirname(log_path), os.W_OK):
    print("[WARNING]: log file at %s is not writeable and we cannot create it\n" % log_path, file=sys.stderr)
  else:
    logging.basicConfig(filename=log_path, level=level, format='%(asctime)s %(name)s %(message)s')
  os.environ['EI_LOG_PATH'] = log_path

def get_log_file():
  return os.path.join(get_config_dir(), 'ei.log')

configure_logging(get_log_file(), logging.DEBUG)

cli.main()
