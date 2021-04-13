import connexion 
from connexion import NoContent
import json
import os
import requests
import yaml
import logging
import logging.config
import datetime
from pykafka import KafkaClient
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable, NoBrokersAvailableError

YAML = "twopape1965-ShiftCalendar-1.0.0-swagger.yaml"


def log_data(FILE_NAME, MAX_EVENTS, body, req_list):
    req_list.append(body)
    if len(req_list) > MAX_EVENTS:
        req_list.pop(0)
    with open(FILE_NAME, 'w') as file:
        for obj in req_list:
            json_str = json.dumps(obj)
            file.write(json_str + '\n')


def add_user(body):

    id = body['user_id']

    headers = {"Content-Type" : "application/json"}

    user = body

    # r = requests.post(app_config['eventstore1']['url'], json=body, headers=headers)
    # client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    # topic = client.topics[str.encode(app_config['events']['topic'])]

    msg = { "type" : "user",
            "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload" : user
            }
    
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f"Recieved event add user request with a unique id of {id}")

    logger.info(f"Returned event add user response (id: {id}) with status 201")
    
    return 201


def add_shift(body):

    id = body['shift_id']

    headers = {"Content-Type" : "application/json"}

    shift = body

    # r = requests.post(app_config['eventstore2']['url'], json=body, headers=headers)

    # client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    # topic = client.topics[str.encode(app_config['events']['topic'])]

    msg = { "type" : "shift",
            "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload" : shift
            }
    
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f"Recieved event add shift request with a unique id of {id}")

    logger.info(f"Returned event add shift response (id: {id}) with status 201")

    return 201


def add_income(body):

    id = body['income_id']

    headers = {"Content-Type" : "application/json"}

    income = body

    # r = requests.post(app_config['eventstore3']['url'], json=body, headers=headers)

    # client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    # topic = client.topics[str.encode(app_config['events']['topic'])]

    msg = { "type" : "income",
            "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload" : income
            }
    
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))



    logger.info(f"Recieved event add income request with a unique id of {id}")

    logger.info(f"Returned event add income response (id: {id}) with status 201")

    return 201


app = connexion.FlaskApp(__name__, specification_dir='')


app.add_api(YAML,strict_validation=True, validate_responses=True)


# with open('app_conf.yaml', 'r') as f:
#     app_config = yaml.safe_load(f.read())


# with open('log_conf.yaml','r') as f:
#     log_config = yaml.safe_load(f.read())
#     logging.config.dictConfig(log_config)
    

# logger = logging.getLogger('basicLogger')







if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

    # External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    
    
logger = logging.getLogger('basicLogger')


logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)


hostname = f"{app_config['events']['hostname']}:{app_config['events']['port']}"
max_tries = app_config['tries']['max_retries']
current_attempts=0
flag = False
while (current_attempts < max_tries) and (flag != True):
    logger.info(f"Attempting to connect to client attempt {current_attempts} of {app_config['tries']['max_retries']}")
    try:
        client = KafkaClient(hosts=hostname)
        flag = True
    except (SocketDisconnectedError, LeaderNotAvailable, NoBrokersAvailableError) as e:
        logger.error(f"attempted connection {current_attempts} of {app_config['tries']['max_retries']} failed retrying in {app_config['sleep']['time']} seconds.")
        time.sleep(5)
        current_attempts+=1
topic = client.topics[str.encode(app_config['events']['topic'])]
producer = topic.get_sync_producer()

if __name__ == "__main__":
    app.run(port=8080)