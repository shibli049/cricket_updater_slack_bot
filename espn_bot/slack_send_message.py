import requests
import espn_update
import time,random
import json
import os
import mybot
import logging

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

default_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
default_payload ={'text':''}

def sendSlackMessage(msg,webhook_url = default_webhook_url, payload= default_payload):
    if(msg == None):
        return
    data = payload['text'] = msg
    response = requests.post(webhook_url,json=payload)
    logging.debug(response.text)


if __name__ == '__main__':

    last_update = None

    while(True):
        time.sleep(random.randint(30,70))
        logging.info(time.ctime())
        update,status,_ = espn_update.showScore()
        if(update != None and status != None):
            if(last_update == None):
                mybot.sendMessageToBotChannel(msg = "new: " + status)
                last_update = update
                logging.info("New: " + json.dumps( last_update ))
            else:
                # update = {'runs' : int(runs), 'wk': wickets-int(remaining_wickets), 'lead':lead}
                rundiff = abs( update['runs'] - last_update['runs'])
                wkdiff = abs( update['wk'] - last_update['wk'])
                leaddiff =  abs( update['lead'] - last_update['lead'])
                batting_team_diff = update['batting_team_id'] != last_update['batting_team_id']
                if('won by' in status or 'lost by' in status):
                    last_update = update
                    mybot.sendMessageToBotChannel(msg = "Final Result: " + status)
                    logging.info(">>>Final Update Available: " + json.dumps( last_update ))
                    break
                if('stump' in status):
                    last_update = update
                    mybot.sendMessageToBotChannel(msg = "Final update: " + status)
                    logging.info(">>>Day Final Update Available: " + json.dumps( last_update ))
                    sleep_time = 60*60
                    time.sleep(sleep_time)
                elif(rundiff == 50 or wkdiff == 1 or leaddiff == 20 or batting_team_diff ):
                   last_update = update
                   mybot.sendMessageToBotChannel(msg = "update: " + status)
                   logging.info(">>>Update Available: " + json.dumps( last_update ))
                else:
                    logging.info("No Update Available: " + json.dumps( update ))