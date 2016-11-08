import requests
import json
import logging

import gzip

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


def getPage(url = "http://www.espncricinfo.com/netstorage/1063053.json?xhr=1"):
    # headers = {'accept-encoding': 'gzip,deflate'}
    # , headers=headers
    response = requests.get(url)
    html = response.text
    # jsondata = response.json
    logging.debug(html)
    # logging.info(jsondata)
    # logging.info(len(html))
    return html,len(html)

def showScore():
    html,_ = getPage()
    if(len(html) > 100):
        try:
            return getScore(html)
        except (json.decoder.JSONDecodeError ,KeyError) as err:
            logging.debug(html)
            logging.error("Error Retreiving Json Data: {0}".format(err))
            return None,None,[]


if __name__ == '__main__':
    import time
    import random
    total_time = 0
    s_time = 0
    f_time = 0
    repeat = 10
    s_count = 0
    f_count = 0
    for i in range(repeat):
        start = time.time()
        html,len_html = getPage()
        done = time.time()
        elapsed = done - start
        total_time += elapsed
        logging.info("len_html:"  + str(len_html))
        if(len_html < 300):
            f_time += elapsed
            f_count += 1
        else:
            s_time += elapsed
            s_count += 1
        print(elapsed)
        # sleep_time = random.randint(60,120)
        # print("sleeping for " + str(sleep_time))
        # time.sleep(sleep_time)

    print("t: " , total_time/repeat)
    if(s_count > 0):
        print("s:" , s_time/s_count)

    if(f_count > 0):
        print("f:" , f_time/f_count)