import connexion 
from connexion import NoContent
import json
import os
from os import path
import requests
import yaml
import logging
import logging.config
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS, cross_origin

YAML = "twopape1965-ShiftCalendar-1.0.0-swagger.yaml"


def get_stats():
    logger.info('Request has begun.')
    if path.exists('data.json'):
        curr_stats = json.load(open('data.json', 'r'))
    else:
        return 404, "Stats not found"
    
    logger.debug(f'Contents of file are {curr_stats}')

    logger.info('Request finished')

    return curr_stats, 200

def populate_stats():
    logger.info("Start Periodic Processing")

    if path.exists('data.json'):
        curr_stats = json.load(open('data.json', 'r'))
    else:
        curr_stats = {'num_shifts':0, 'num_incomes': 0, 'max_income':0, 'timestamp':'2016-08-29T09:12:33Z'}

    curr_date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    r1 = requests.get(app_config['eventstore1']['url']+"/shifts?start_timestamp="+curr_stats['timestamp']+"&end_timestamp="+curr_date)

    r1_list = r1.json()

    r1_code = r1.ok

    if not r1_list:
        r1_count = 0
    else:
        r1_count = len(r1_list)

    shift_count = curr_stats['num_shifts'] + r1_count

    if r1_code == True:
        logger.info(f'Returned OK with {r1_count} events.')
    else:
        logger.error(f'Response code not OK.')

    r2 = requests.get(app_config['eventstore2']['url']"/incomes?start_timestamp="+curr_stats['timestamp']+"&end_timestamp="+curr_date)

    r2_list = r2.json()

    r2_code = r2.ok


    if not r2_list:
        r2_count = 0
    else:
        r2_count = len(r2_list)

    max_income = curr_stats['max_income']

    income_count = curr_stats['num_incomes'] + r2_count

    if r2_code == True:
        logger.info(f'Returned OK with {r2_count} events.')
    else:
        logger.error(f'Response code not OK.')

    if not r2_list:
        pass    
    else:
        for income in r2_list:
            if income['income_amount'] > max_income:
                max_income = income['income_amount']

    new_stats = {'num_shifts': shift_count, 'num_incomes': income_count, 'max_income': max_income, 'timestamp': curr_date}

    json.dump(new_stats, open('data.json', 'w'))

    logger.debug(f'data.json file updated with values: {new_stats}')

    logger.info('Periodic processing ended.')





def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()


# def log_data(FILE_NAME, MAX_EVENTS, body, req_list):
#     req_list.append(body)
#     if len(req_list) > MAX_EVENTS:
#         req_list.pop(0)
#     with open(FILE_NAME, 'w') as file:
#         for obj in req_list:
#             json_str = json.dumps(obj)
#             file.write(json_str + '\n')


# def add_user(body):

#     id = body['user_id']

#     headers = {"Content-Type" : "application/json"}

#     r = requests.post(app_config['eventstore1']['url'], json=body, headers=headers)
    
#     logger.info(f"Recieved event add user request with a unique id of {id}")

#     logger.info(f"Returned event add user response (id: {id}) with status {r.status_code}")
    
#     return NoContent, r.status_code


# def add_shift(body):

#     id = body['shift_id']

#     headers = {"Content-Type" : "application/json"}

#     r = requests.post(app_config['eventstore2']['url'], json=body, headers=headers)
    
#     logger.info(f"Recieved event add shift request with a unique id of {id}")

#     logger.info(f"Returned event add shift response (id: {id}) with status {r.status_code}")

#     return NoContent, r.status_code


# def add_income(body):

#     id = body['income_id']

#     headers = {"Content-Type" : "application/json"}

#     r = requests.post(app_config['eventstore3']['url'], json=body, headers=headers)
    
#     logger.info(f"Recieved event add income request with a unique id of {id}")

#     logger.info(f"Returned event add income response (id: {id}) with status {r.status_code}")

#     return NoContent, r.status_code


app = connexion.FlaskApp(__name__, specification_dir='')

CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'


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


if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)