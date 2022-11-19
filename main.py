import datetime
import requests
import json
import os

from vkwave.bots import SimpleLongPollBot, SimpleBotEvent

TOKEN = os.environ['bot_token']
webhook_url = os.environ['webhook_url']
GROUP_ID = int(os.environ['group_id'])
BOT_DESTROY_MESSAGE = os.environ['bot_destroy_message']
STATUS_CHECK_RESPONSE = os.environ['bot_status_check_message']
SECONDS_AFTER_MEMBER_JOIN = int(os.environ['seconds_after_member_join'])
ACTIVE_STATUS_CHECK_COMMAND = os.environ['status_check_command']

bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)

@bot.message_handler()
async def echo(event: SimpleBotEvent) -> str:
    user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0]
    print("New message from " + user_data.first_name + " " + user_data.last_name + ": " + event.text)
    if len(event.text) > 0 and webhook_url is not None and len(webhook_url) > 0:
        send_webhook('Новое сообщение от ' + user_data.first_name + " " + user_data.last_name + ': ' + event.text)

    if ACTIVE_STATUS_CHECK_COMMAND in event.text:
        return STATUS_CHECK_RESPONSE

    for link in ["vk.com/", "https://", "http://", "vk.me/", "vk.cc/", "t.me/", ".com", ".net", ".ru"]:
        if link in event.text:
            print("Link detected! Check...")

            members = (await event.api_ctx.messages.get_conversation_members(
                peer_id=event.object.object.message.peer_id)).response
            member = None

            for mem in members.items:
                if mem.member_id == event.object.object.message.from_id:
                    member = mem

            join_date = datetime.datetime.fromtimestamp(member.join_date)

            delta_date = datetime.datetime.now() - join_date

            print("User added in group on last time: " + str(delta_date))

            if delta_date.total_seconds() < SECONDS_AFTER_MEMBER_JOIN:
                await event.api_ctx.messages.delete(
                    conversation_message_ids=event.object.object.message.conversation_message_id,
                    delete_for_all=True,
                    peer_id=event.object.object.message.peer_id)
                await event.api_ctx.messages.remove_chat_user(event.peer_id - 2000000000,
                                                              member_id=event.object.object.message.from_id)
                return BOT_DESTROY_MESSAGE
            else:
                print("All ok!")


def send_webhook(text):
    data = {'content': text}
    try:
        requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=1)
    except requests.exceptions.ReadTimeout:
        pass


print("Bot start...")
bot.run_forever()
