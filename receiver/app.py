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
    print('before')
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    print('aft')
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

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

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

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

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

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


with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())


with open('log_conf.yaml','r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    

logger = logging.getLogger('basicLogger')


if __name__ == "__main__":
    app.run(port=8080)