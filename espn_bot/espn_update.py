import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

# mbl_live_url1="http://m.espncricinfo.com/ci/engine/match/module/live.html?commTab=null;id=1050233;view=live"
mbl_live_url2="http://m.espncricinfo.com/ci/engine/match/module/scorecard_header.html?header=1;id=1050233;wrappertype=none"
mbl_live_url3="http://m.espncricinfo.com/ci/engine/match/module/live.html?id=1050233;view=live"


wickets = 10
def getScore(html):
    d = json.loads(html)
    live = d['live']
    curr_inn =live['innings']
    remaining_wickets = curr_inn['remaining_wickets']
    runs = curr_inn['runs']
    lead = int(curr_inn['lead'])*-1
    status = live['status']
    batting_team_id=curr_inn['batting_team_id']
    latest = "runs: " + runs + "/" + str(wickets-int(remaining_wickets)) + "\t trail by: " + str(lead)

    update = {'runs' : int(runs), 'wk': wickets-int(remaining_wickets), 'lead':lead, 'batting_team_id':batting_team_id}
    return update,status,live


def getPage(url = "http://www.espncricinfo.com/netstorage/1050233.json?xhr=1"):
    response = requests.get(url)
    html = response.text
    return html

def showScore():
    html = getPage()
    if(len(html) > 100):
        try:
            return getScore(html)
        except json.decoder.JSONDecodeError as err:
            logging.debug(html)
            logging.error("Error Retreiving Json Data")
            return None,None,[]
