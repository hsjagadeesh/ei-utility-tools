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

  parser = argparse.ArgumentParser(description="EI Data Pipeline Orchestrator")
  parser.add_argument('-v', '--verbosity', type=int, dest='verbosity', help='verbosity range [0-6]', default=2, required=False)

  command_parser = parser.add_subparsers(help="options", dest='command')
  pipeline_parser = command_parser.add_parser('pipeline', help='Pipeline Operations (deploy, undeploy, status)')
  pipeline_command_parser = pipeline_parser.add_subparsers(dest='pipeline_command')

  pipeline_deploy_parser = pipeline_command_parser.add_parser('deploy', help='Deploy single/multi data pipeline(s)')
  pipeline_deploy_parser.add_argument('-i', '--ip', type=str, dest='device_ip', help='ip address of the device (mandatory for single pipeline config option)')
  pipeline_deploy_parser.add_argument('-n', '--name', type=str, dest='pipeline_name', help='name of the data pipeline (mandatory for single pipeline config option)')
  pipeline_deploy_parser.add_argument('-c', '--config-file', type=str, dest='single_pipeline_config', help='single data pipeline config file path (json)')
  pipeline_deploy_parser.add_argument('-f', '--file', type=str, dest='multi_pipeline_config', help='multi data pipeline config file path (yaml)')

  pipeline_undeploy_parser = pipeline_command_parser.add_parser('undeploy', help='UnDeploy single/multi data pipeline(s)')
  pipeline_undeploy_parser.add_argument('-i', '--ip', type=str, dest='device_ip', help='ip address of the device (mandatory for single pipeline config option)')
  pipeline_undeploy_parser.add_argument('-n', '--name', type=str, dest='pipeline_name', help='name of the data pipeline (mandatory for single pipeline config option)')
  pipeline_undeploy_parser.add_argument('-c', '--config-file', type=str, dest='single_pipeline_config', help='single data pipeline config file path (json)')
  pipeline_undeploy_parser.add_argument('-p', '--pipeline-file', type=str, dest='multi_pipeline_config', help='multi data pipeline config file path (yaml)')

  pipeline_status_parser = pipeline_command_parser.add_parser('status', help='Get status for single/multi data pipeline(s)')
  pipeline_status_parser.add_argument('-i', '--ip', type=str, dest='device_ip', help='ip address of the device (mandatory for single pipeline config option)')
  pipeline_status_parser.add_argument('-n', '--name', type=str, dest='pipeline_name', help='name of the data pipeline (mandatory for single pipeline config option)')
  pipeline_status_parser.add_argument('-c', '--config-file', type=str, dest='single_pipeline_config', help='single data pipeline config file path (json)')
  pipeline_status_parser.add_argument('-p', '--pipeline-file', type=str, dest='multi_pipeline_config', help='multi data pipeline config file path (yaml)')

  args = parser.parse_args()
  logger.debug("Pipeline command running with args: %s", vars(args))

  if args.verbosity == 0:
    logging.basicConfig(level=logging.CRITICAL)
  elif args.verbosity == 1:
    logging.basicConfig(level=logging.WARNING)
  elif args.verbosity == 2:
    logging.basicConfig(level=logging.INFO)
  elif args.verbosity >= 3:
    logging.basicConfig(level=logging.DEBUG)

  if args.command == 'pipeline':
    if args.pipeline_command == 'deploy':
      on_deploy(vars(args), pipeline_deploy_parser)
    elif args.pipeline_command == 'undeploy':
      on_undeploy(vars(args), pipeline_undeploy_parser)
    elif args.pipeline_command == 'status':
      on_status(vars(args), pipeline_status_parser)
    elif args.pipeline_command == 'reset':
      on_reset(vars(args), pipeline_reset_parser)
    else:
      parser.print_help()
  else:
    parser.print_help()

def is_valid_string(string):
  return bool(string and string.strip())

def validate_args(args):
  is_single_dep = is_multiple_dep = False
  if is_valid_string(args["single_pipeline_config"]) and is_valid_string(args["multi_pipeline_config"]):
    print("\nPlease provide either single pipeline option or multiple pipeline option but not both\n")
    logger.error("Invalid : both single pipeline option and multiple pipeline option are given")
  elif not(is_valid_string(args["single_pipeline_config"])) and not(is_valid_string(args["multi_pipeline_config"])):
    print("\nPlease provide at least single pipeline option or multiple pipeline option\n")
    logger.error("Invalid : both single pipeline option and multiple pipeline option are not valid")
  elif is_valid_string(args["single_pipeline_config"]):
    if not is_valid_string(args["device_ip"]):
      print("\nPlease provide valid ip address\n")
      logger.error("Invalid Arg(s): device ip is null or empty")
    elif not (is_valid_string(args["pipeline_name"])):
      print("\nPlease provide valid pipeline name\n")
      logger.error("Invalid Arg(s): pipeline name is null or empty")
    else:
      args_str = str(args["device_ip"]) + " " + str(args["pipeline_name"]) + " " + str(args["single_pipeline_config"])
      logger.debug("Single pipeline deployment selected :" + args_str)
      print("\nSingle pipeline deployment selected", args["device_ip"], args["pipeline_name"], args["single_pipeline_config"])
      is_single_dep = True
  elif is_valid_string(args["multi_pipeline_config"]):
    logger.debug("Multi pipeline deployment selected :" + args["multi_pipeline_config"])
    print("\nMulti pipeline deployment selected", args["multi_pipeline_config"])
    is_multiple_dep = True
  else:
    logger.debug("Invalid pipeline deployment selected")
    is_single_dep = is_multiple_dep = False
  return is_single_dep, is_multiple_dep

def on_deploy(args, parser):
  logger.debug("Calling on_deploy()")
  is_single_dep, is_multiple_dep = validate_args(args)
  if is_single_dep:
      print("\nSingle pipeline deployment selected", args["device_ip"], args["pipeline_name"], args["single_pipeline_config"])
      # TODO
  elif is_multiple_dep:
    print("\nMulti pipeline deployment selected", args["multi_pipeline_config"])
    # TODO
  else:
    parser.print_help()

def on_undeploy(args, parser):
  print("on_undeploy ", args)

def on_status(args, parser):
  print("on_status ", args)

def on_reset(args, parser):
  print("on_reset ", args)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='...')
    p.add_argument('--argument', required=False)
    p.add_argument('-a', required='--argument' in sys.argv) #only required if --argument is given
    p.add_argument('-b', required='--argument' in sys.argv) #only required if --argument is given
    args = p.parse_args()
    print(args)