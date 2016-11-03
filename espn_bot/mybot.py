import os
from slackclient import SlackClient

BOT_NAME = 'mybot'

sc = SlackClient(os.environ.get('SLACK_TOKEN'))



def sendMessageToBotChannel(msg):
    if msg:
        sc.rtm_connect()
        sc.rtm_send_message(os.environ.get('BOT_CHANNEL_ID'), msg)


if __name__ == "__main__":
    sendMessageToBotChannel("Hello Channel!!")

    # api_call = slack_client.api_call("channels.list")
    # if api_call.get('ok'):
    #     # retrieve all users so we can find our bot
    #     # channels = api_call.get('channels')
    #     # for channel in channels:
    #     #     print("channel ID for '" + channel['name'] + "' is " + channel.get('id'))
    #         # if 'name' in user and user.get('name') == BOT_NAME:
    #         #     print("Bot ID for '" + user['name'] + "' is " + user.get('id'))

    # else:
    #     print("could not find bot user with the name " + BOT_NAME)
