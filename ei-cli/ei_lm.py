from threading import Thread
import logging
import os

MAX_BATCH_SIZE = os.getenv("EI_CLI_BATCH_SIZE", 20)
DEPLOY = "deploy"
UN_DEPLOY = "undeploy"
STATUS = "status"
RESET = "reset"
CHANGE_PWD = "change-pwd"

DEVICE_IP = "DEVICE_IP"
PIPELINE_NAME = "PIPELINE_NAME"
DATA_SOURCE_FILE = "DATA_SOURCE_FILE"
DATA_TARGET_FILE = "DATA_TARGET_FILE"
DATA_LOGIC_FILE = "DATA_LOGIC_FILE"
DATA_VARIABLES_FILE = "DATA_VARIABLES_FILE"

PIPELINE_JSON = "PIPELINE_JSON"
RESPONSE = "RESPONSE"
PASSWORD = "PASSWORD"
OPERATION = "OPERATION"

logger = logging.getLogger(__name__)

class EiCliThread(Thread):

  def run(self):
    self.exc = None
    try:
      if hasattr(self, '_Thread__target'):
        # Thread uses name mangling prior to Python 3.
        self.ret = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
      else:
        self.ret = self._target(*self._args, **self._kwargs)
    except BaseException as e:
      self.exc = e

  def join(self):
    super(EiCliThread, self).join()
    if self.exc:
      raise RuntimeError('Exception in thread') from self.exc
    return self.ret

def run_in_batch(task_threads, max_thread_spawns_allowed=MAX_BATCH_SIZE):
  # calculate no of batches of threads to be spawned
  if len(task_threads) > max_thread_spawns_allowed:
    if len(task_threads) % max_thread_spawns_allowed:
      no_of_batches = int(len(task_threads) / max_thread_spawns_allowed) + 1
    else:
      no_of_batches = int(len(task_threads) / max_thread_spawns_allowed)
  else:
    no_of_batches = 1
  logger.debug("No of batches of threads to run {}".format(no_of_batches))
  i = 0
  for batch in range(no_of_batches):
    # for each batch, start the threads and wait for those to complete
    if i + max_thread_spawns_allowed <= len(task_threads):
      max_t = max_thread_spawns_allowed
    else:
      max_t = max_thread_spawns_allowed - (i + max_thread_spawns_allowed - len(task_threads))
    for j in range(i, i + max_t):
      task_threads[j].start()
    # Wait for all the threads in the batch to complete
    for k in range(i, i + max_t):
      task_threads[k].join()
    i = i + max_thread_spawns_allowed

def execute_pipelines(inventory_list, device_pwd=None, operation=None):
  pipeline_obj_list = []
  logger.debug("Number of objects inventory file " + str(len(inventory_list)))
  print(inventory_list)

  # Create pipeline object list from inventory list
  for inventory_obj in inventory_list:
    pipeline_obj = get_pipeline_obj(inventory_obj, operation)
    pipeline_obj[PASSWORD] = device_pwd
    pipeline_obj_list.append(pipeline_obj)

  # Create the pool threads for execution
  ei_cli_threads = []
  if len(pipeline_obj_list) > 0:
    for pipeline_obj in pipeline_obj_list:
      if pipeline_obj is not None:
        t = EiCliThread(target=execute_pipeline_obj, args=(operation, pipeline_obj))
        ei_cli_threads.append(t)
  # Start the thread execution in batches
  if len(ei_cli_threads) > 0:
    run_in_batch(ei_cli_threads, MAX_BATCH_SIZE)

def execute_pipeline_obj(operation=None, pipeline_obj=None):
  if operation is None:
    operation = pipeline_obj[OPERATION]
  # Check operation and perform the task
  if operation == DEPLOY:
    deploy_pipeline(pipeline_obj)
  elif operation == UN_DEPLOY:
    un_deploy_pipeline(pipeline_obj)
  elif operation == STATUS:
    get_pipeline_status(pipeline_obj)
  else:
    pass

def is_valid_string(string):
  return bool(string and string.strip())

def get_pipeline_obj(inventory_obj, operation=None):
  pipeline_obj = {}
  if operation is None:
    return pipeline_obj

  device_ip = inventory_obj.get(DEVICE_IP, None)
  pipeline_name = inventory_obj.get(PIPELINE_NAME, None)

  # For any operation, device ip and pipeline name are mandatory
  if not is_valid_string(device_ip):
    logger.error("Invalid device ip given in inventory file for inventory obj " + inventory_obj)
    print("Invalid device ip given in inventory file.")
    exit(0)
  if not is_valid_string(pipeline_name):
    print("Invalid pipeline name given in inventory file.")
    logger.error("Invalid pipeline name given in inventory file for inventory obj " + inventory_obj)
    exit(0)

  # This field will contain the response of the api call and will get updated during api call execution
  pipeline_obj[RESPONSE] = "NA"
  pipeline_obj[OPERATION] = operation
  pipeline_obj[DEVICE_IP] = device_ip
  pipeline_obj[PIPELINE_NAME] = pipeline_name

  # If the operation is un-deploy or get status, then only device ip and pipeline name is needed
  if operation == STATUS or operation == UN_DEPLOY:
    return pipeline_obj

  if operation == DEPLOY:
    data_source_file = inventory_obj.get(DATA_SOURCE_FILE, None)
    data_target_file = inventory_obj.get(DATA_TARGET_FILE, None)

    # For deploy, data_source_file and data_target_file are mandatory
    if not is_valid_string(data_source_file):
      print("Invalid data source file name given in inventory file.")
      logger.error("Invalid data source file name given in inventory file for inventory obj " + inventory_obj)
      exit(0)
    if not is_valid_string(data_target_file):
      print("Invalid pipeline name given in inventory file.")
      logger.error("Invalid pipeline name given in inventory file for inventory obj " + inventory_obj)
      exit(0)

    # For deploy, data logic and data variables are not mandatory
    data_logic_file = inventory_obj.get(DATA_LOGIC_FILE, None)
    data_vars_file = inventory_obj.get(DATA_VARIABLES_FILE, None)

    # Get the pipeline json obj
    pipeline_json = get_pipeline_json(data_source_file, data_target_file, data_logic_file, data_vars_file)
    pipeline_obj[PIPELINE_JSON] = pipeline_json

  return pipeline_obj

def get_pipeline_json(data_source_json, data_target_json, data_logic_json=None, data_vars=None):
  pipeline_json = {}
  # TODO Combine the files and apply template variables
  return pipeline_json

def un_deploy_pipeline(pipeline_obj):
  device_ip = pipeline_obj[DEVICE_IP]
  pipeline_name = pipeline_obj[PIPELINE_NAME]
  logger.debug("Started un-deploying pipeline " + pipeline_name + " on device " + device_ip)
  print("Started un-deploying pipeline", pipeline_name, "on device", device_ip)
  # TODO Send http delete request to the device. URL: /api/v1/edge-intelligence/pipelines/{pipelineId}

  # Set the response from the api call to pipeline object
  status = pipeline_obj[RESPONSE] = "Success"
  print("Finished un-deploying pipeline", pipeline_name, "on device", device_ip, "Status:", status)
  logger.debug("Finished un-deploying pipeline " + pipeline_name + " on device " + device_ip + "Status: " + status)
  pass

def get_pipeline_status(pipeline_obj):
  device_ip = pipeline_obj[DEVICE_IP]
  pipeline_name = pipeline_obj[PIPELINE_NAME]
  logger.debug("Started getting pipeline status for " + pipeline_name + " on device " + device_ip)
  print("Started getting pipeline status for", pipeline_name, "on device", device_ip)
  # TODO Send http get status request to the device. URL: /api/v1/edge-intelligence/pipelines/{pipelineId}/status

  # Set the response from the api call to pipeline object
  status = pipeline_obj[RESPONSE] = "Success"
  print("Finished getting pipeline status for", pipeline_name, "on device", device_ip, "Status:", status)
  logger.debug("Finished getting pipeline status for " + pipeline_name + " on device " + device_ip + "Status: " + status)
  pass

def deploy_pipeline(pipeline_obj):
  device_ip = pipeline_obj[DEVICE_IP]
  pipeline_name = pipeline_obj[PIPELINE_NAME]
  logger.debug("Started deploying pipeline " + pipeline_name + " on device " + device_ip)
  print("Started deploying pipeline", pipeline_name, "on device", device_ip)
  # TODO Send http post request to the device. URL: /edge-intelligence/pipelines

  # Set the response from the api call to pipeline object
  status = pipeline_obj[RESPONSE] = "Success"
  print("Finished deploying pipeline", pipeline_name, "on device", device_ip, "Status:", status)
  logger.debug("Finished deploying pipeline " + pipeline_name + " on device " + device_ip + "Status: " + status)
  pass
