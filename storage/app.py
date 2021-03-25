import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import mysql.connector

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from users import User
from shifts import Shift
from incomes import Income
import datetime
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread


YAML = "twopape1965-ShiftCalendar-1.0.0-swagger.yaml"
DB_ENGINE = create_engine("mysql+pymysql://events:password@acit3855-sba-microservices-vm-cameron-woolfries.eastus2.cloudapp.azure.com:3306/events")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def add_user(body):
    """ Receives a user info to add to the users table """

    id = body['user_id']

    logger.info(f"Connecting to DB. Hostname:acit3855-sba-microservices-vm-cameron-woolfries.eastus2.cloudapp.azure.com, Port:3306.")

    session = DB_SESSION()

    user = User(body['user_id'],
                       body['user_name'],
                       body['password'])

    session.add(user)

    session.commit()
    
    session.close()

    logger.debug(f"Stored event add user request with a unique id of {id}.")

    return NoContent, 201


def add_shift(body):
    """ Receives a shift and adds it to the shift table"""

    id = body['shift_id']

    logger.info(f"Connecting to DB. Hostname:acit3855-sba-microservices-vm-cameron-woolfries.eastus2.cloudapp.azure.com, Port:3306.")

    session = DB_SESSION()

    shift = Shift(body['shift_id'],
                   body['shift_name'],
                   body['start_time'],
                   body['end_time'],
                   body['user_id'])

    session.add(shift)

    session.commit()
    
    session.close()

    logger.debug(f"Stored event add user request with a unique id of {id}.")

    return NoContent, 201

    return NoContent, 200


def add_income(body):
    """ Recieves an income object and shift it in the incomes table"""

    id = body['income_id']

    logger.info(f"Connecting to DB. Hostname:acit3855-sba-microservices-vm-cameron-woolfries.eastus2.cloudapp.azure.com, Port:3306.")

    session = DB_SESSION()

    income = Income(body['income_id'],
                   body['income_amount'],
                   body['shift_id'])

    session.add(income)

    session.commit()
        
    session.close()

    logger.debug(f"Stored event add income request with a unique id of {id}.")

    return NoContent, 201

    return NoContent, 200


def get_shifts(timestamp):
    """Gets new shifts after the timestamp"""

    logger.info(f"Connecting to DB. Hostname:acit3855-sba-microservices-vm-cameron-woolfries.eastus2.cloudapp.azure.com, Port:3306.")

    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)

    shifts = session.query(Shift).filter(Shift.date_created >= timestamp_datetime)

    results_list = []
    
    for shift in shifts:
        results_list.append(shift.to_dict())

    session.close()

    logger.info("Query for shifts after %s returns %d results" %(timestamp, len(results_list)))

    return results_list, 200


def get_incomes(timestamp):
    """Gets new incomes after the timestamp"""

    logger.info(f"Connecting to DB. Hostname:acit3855-sba-microservices-vm-cameron-woolfries.eastus2.cloudapp.azure.com, Port:3306.")

    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)

    incomes = session.query(Income).filter(Income.date_created >= timestamp_datetime)

    results_list = []
    
    for income in incomes:
        results_list.append(income.to_dict())

    session.close()

    logger.info("Query for incomes after %s returns %d results" %(timestamp, len(results_list)))

    return results_list, 200


def process_messages():
    """Process event messages"""
    hostname = f"{app_config['events']['hostname']}:{app_config['events']['port']}"
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config['events']['topic'])]
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                                reset_offset_on_start=False,
                                                auto_offset_reset=OffsetType.LATEST)

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info(f"Message: {msg}")

        payload = msg["payload"]

        if msg['type'] == "user":
            add_user(payload)
        elif msg['type'] == "shift":
            add_shift(payload)
        elif msg['type'] == "income":
            add_income(payload)
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api(YAML, strict_validation=True, validate_responses=True)


with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())


with open('log_conf.yaml','r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    

logger = logging.getLogger('basicLogger')


if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)