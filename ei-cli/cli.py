#!/usr/bin/env python3

"""Command Line Module for EI Data Pipeline Operations"""

from __future__ import print_function

import sys
import os

import argparse
import logging

logger = logging.getLogger(__name__)
cwd = os.getcwd()

def main():

  parser = argparse.ArgumentParser(description="EI Local Manager CLI Orchestrator (Version 1.0.0)")
  # parser.add_argument('-v', '--verbosity', type=int, dest='verbosity', help='verbosity range [0-6]', default=2, required=False)
  command_parser = parser.add_subparsers(help="options", dest='command')

  # User related CLIs
  user_parser = command_parser.add_parser('user', help='user operations (change-password)')
  user_command_parser = user_parser.add_subparsers(dest='user_command')

  user_change_pwd_parser = user_command_parser.add_parser('change-pwd', help='change user(s) password on the device(s)')
  user_change_pwd_parser.add_argument('-f', '--file', type=str, dest='inventory_file', help='device(s) inventory file (yaml)')

  # Agent related CLIs
  agent_parser = command_parser.add_parser('agent', help='agent operations (status, reset)')
  agent_command_parser = agent_parser.add_subparsers(dest='agent_command')

  agent_reset_parser = agent_command_parser.add_parser('reset', help='reset the agent(s)')
  agent_reset_parser.add_argument('-f', '--file', type=str, dest='inventory_file', help='device(s) inventory file (yaml)')

  agent_status_parser = agent_command_parser.add_parser('status', help='get status of the agent(s)')
  agent_status_parser.add_argument('-f', '--file', type=str, dest='inventory_file', help='device(s) inventory file (yaml)')

  # Pipeline related CLIs
  pipeline_parser = command_parser.add_parser('pipeline', help='pipeline operations (deploy, undeploy, status)')
  pipeline_command_parser = pipeline_parser.add_subparsers(dest='pipeline_command')

  pipeline_deploy_parser = pipeline_command_parser.add_parser('deploy', help='deploy data pipeline(s)')
  pipeline_deploy_parser.add_argument('-f', '--file', type=str, dest='inventory_file', help='pipeline(s) inventory file (yaml)')

  pipeline_undeploy_parser = pipeline_command_parser.add_parser('undeploy', help='un-deploy data pipeline(s)')
  pipeline_undeploy_parser.add_argument('-f', '--file', type=str, dest='inventory_file', help='pipeline(s) inventory file (yaml)')

  pipeline_status_parser = pipeline_command_parser.add_parser('status', help='get status of data pipeline(s)')
  pipeline_status_parser.add_argument('-f', '--file', type=str, dest='inventory_file', help='pipeline(s) inventory file (yaml)')

  args = parser.parse_args()
  logger.debug("EI CLI command running with args: %s", vars(args))

  if args.command == 'pipeline':
    if args.pipeline_command == 'deploy':
      on_pipeline_deploy(vars(args), pipeline_deploy_parser)
    elif args.pipeline_command == 'undeploy':
      on_pipeline_undeploy(vars(args), pipeline_undeploy_parser)
    elif args.pipeline_command == 'status':
      on_pipeline_status(vars(args), pipeline_status_parser)
    else:
      parser.print_help()
  elif args.command == 'agent':
    if args.agent_command == 'reset':
      on_agent_reset(vars(args), agent_reset_parser)
    elif args.agent_command == 'status':
      on_agent_status(vars(args), agent_status_parser)
    else:
      parser.print_help()
  elif args.command == 'user':
    if args.user_command == 'change-pwd':
      on_user_change_pwd(vars(args), user_change_pwd_parser)
    else:
      parser.print_help()
  else:
    parser.print_help()

def is_valid_string(string):
  return bool(string and string.strip())

def on_pipeline_deploy(args, parser):
  logger.debug("Calling on_pipeline_deploy()")
  inventory_file = args.get("inventory_file", "")
  if is_valid_string(inventory_file):
    logger.debug("Pipeline deployment selected", inventory_file)
  else:
    print("\nPlease provide a valid pipeline inventory file option\n")
    logger.error("Invalid : pipeline inventory file options :" + str(inventory_file))
    parser.print_help()

def on_pipeline_undeploy(args, parser):
  print("on_pipeline_undeploy", args)

def on_pipeline_status(args, parser):
  print("on_pipeline_status", args)

def on_agent_status(args, parser):
  print("on_agent_status", args)

def on_agent_reset(args, parser):
  print("on_agent_reset", args)

def on_user_change_pwd(args, parser):
  print("on_user_change_pwd", args)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='...')
    p.add_argument('--argument', required=False)
    p.add_argument('-a', required='--argument' in sys.argv) #only required if --argument is given
    p.add_argument('-b', required='--argument' in sys.argv) #only required if --argument is given
    args = p.parse_args()
    print(args)
