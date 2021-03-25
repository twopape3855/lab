import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import json
from pykafka import KafkaClient
from flask_cors import CORS, cross_origin

def get_shift(index):
    """ Get shift Reading in History """
    hostname = f"{app_config['events']['hostname']}:{app_config['events']['port']}"
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                        consumer_timeout_ms=5000)
    logger.info(f"Retrieving shift at index {index}")
    count = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'shift':
                if count == int(index):
                    
                    return msg['payload'], 200
                count += 1
    except:
        logger.error("No more messages found")

    logger.error(f"Could not find msg at index {index}")
    return {"message": "Not Found"}, 404

def get_income(index):
    """ Get income Reading in History """
    hostname = f"{app_config['events']['hostname']}:{app_config['events']['port']}"
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                        consumer_timeout_ms=5000)
    logger.info(f"Retrieving income at index {index}")
    count = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'income':
                if count == int(index):
                    return msg, 200
                count += 1
    except:
        logger.error("No more messages found")

    logger.error(f"Could not find msg at index {index}")
    return {"message": "Not Found"}, 404



app = connexion.FlaskApp(__name__, specification_dir='')

CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'


app.add_api('openapi.yml', strict_validation=True, validate_responses=True)


with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())


with open('log_conf.yml','r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    

logger = logging.getLogger('basicLogger')

if __name__ == "__main__":
    app.run(port=8110)