#!/usr/bin/env python3

import os
import logging
import sys
import cli

def get_log_file():
  if os.getenv("EI_CLI_HOME") is None:
    print("EI_CLI_HOME env variable is not set")
    exit(0)
  _config_dir = os.getenv("EI_CLI_HOME", os.path.join(os.getenv("HOME"), ".ei"))
  return os.path.join(_config_dir, 'ei-cli.log')

def configure_logging(log_path=None, log_level=logging.DEBUG):
  if log_path is None:
    log_path = get_log_file()
  if not os.path.exists(os.path.dirname(log_path)):
    try:
      os.makedirs(os.path.dirname(log_path), exist_ok=True)
    except:
      print("[ERROR]: Failed to create log directory", log_path)
  elif (os.path.exists(log_path) and not os.access(log_path, os.W_OK)) or not os.access(os.path.dirname(log_path), os.W_OK):
    print("[WARNING]: log file at %s is not writeable and we cannot create it\n" % log_path, file=sys.stderr)
  else:
    logging.basicConfig(filename=log_path, level=log_level, format='%(asctime)s %(name)s %(message)s')
  os.environ['EI_LOG_PATH'] = log_path

# Configure the log setting
configure_logging(log_level=logging.DEBUG)
# Entry point for ei-cli
cli.main()
