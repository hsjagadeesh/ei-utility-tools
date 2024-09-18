#!/usr/bin/env python3

"""Command Line Module for EI Local Manager Orchestration"""

import sys
import os

import argparse
import logging

logger = logging.getLogger(__name__)
cwd = os.getcwd()

def main():

  parser = argparse.ArgumentParser(description="EI Local Manager CLI Orchestrator (Version 1.0.0)")
  command_parser = parser.add_subparsers(help="options", dest='command')
  # CLI to initialize the ei-cli environment
  init_parser = command_parser.add_parser('init', help='initialize ei-cli environment')

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

  cli_args = parser.parse_args()
  logger.debug("EI CLI command running with args: %s", vars(cli_args))

  if cli_args.command == 'init':
    on_cli_init(vars(cli_args), init_parser)
  elif cli_args.command == 'pipeline':
    if cli_args.pipeline_command == 'deploy':
      on_pipeline_deploy(vars(cli_args), pipeline_deploy_parser)
    elif cli_args.pipeline_command == 'undeploy':
      on_pipeline_undeploy(vars(cli_args), pipeline_undeploy_parser)
    elif cli_args.pipeline_command == 'status':
      on_pipeline_status(vars(cli_args), pipeline_status_parser)
    else:
      parser.print_help()
  elif cli_args.command == 'agent':
    if cli_args.agent_command == 'reset':
      on_agent_reset(vars(cli_args), agent_reset_parser)
    elif cli_args.agent_command == 'status':
      on_agent_status(vars(cli_args), agent_status_parser)
    else:
      parser.print_help()
  elif cli_args.command == 'user':
    if cli_args.user_command == 'change-pwd':
      on_user_change_pwd(vars(cli_args), user_change_pwd_parser)
    else:
      parser.print_help()
  else:
    parser.print_help()

def is_valid_string(string):
  return bool(string and string.strip())

def on_cli_init(cli_args, parser):
  print("on_cli_init", cli_args)

def on_pipeline_deploy(cli_args, parser):
  logger.debug("Calling on_pipeline_deploy()")
  inventory_file = cli_args.get("inventory_file", "")
  if is_valid_string(inventory_file):
    logger.debug("Pipeline deployment selected", inventory_file)
  else:
    print("\nPlease provide a valid pipeline inventory file option\n")
    logger.error("Invalid : pipeline inventory file options :" + str(inventory_file))
    parser.print_help()

def on_pipeline_undeploy(cli_args, parser):
  print("on_pipeline_undeploy", cli_args)

def on_pipeline_status(cli_args, parser):
  print("on_pipeline_status", cli_args)

def on_agent_status(cli_args, parser):
  print("on_agent_status", cli_args)

def on_agent_reset(cli_args, parser):
  print("on_agent_reset", cli_args)

def on_user_change_pwd(cli_args, parser):
  print("on_user_change_pwd", cli_args)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='...')
    p.add_argument('--argument', required=False)
    p.add_argument('-a', required='--argument' in sys.argv)  # only required if --argument is given
    p.add_argument('-b', required='--argument' in sys.argv)  # only required if --argument is given
    print(p.parse_args())
