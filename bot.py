import os, logging, asyncio

from telegraph import upload_file

from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
aditya = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

moment_worker = []


#start
@aditya.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**π₯ Hello, I am Β»Β» Member Tagger\nπ Bot> For Β» Telegram Β» Groups\nπ· Feel Β» Free Β» to Β» Use Β» Me ....\nπ Click /help More Information.**",
                    buttons=(
                      [
                        Button.url('π₯ My β Owner π', 'https://t.me/adityahalder'),   
                      ],
                      [
                         Button.url('π’ Updates π’', 'https://t.me/adityaserver'), 
                         Button.url('π¬ Support π¬', 'https://t.me/adityadiscus'), 
                      ], 
                      [
                        Button.url('π Source Code π', 'https://github.com/mradityaxd/tagallbot'),   
                      ]
                   ), 
                    link_preview=False
                   )

#help
@aditya.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**π₯ Send Β» @all Your Text Β» To Tag\nπ Example Β» __@all Good Morning__\nπ· You Can Use ThisΒ» Command\nπ Via Reply On Any Message ....**"
  await event.reply(helptext,
                    buttons=(
                      [
                        Button.url('π₯ My β Owner π', 'https://t.me/adityahalder'),   
                      ],
                      [
                         Button.url('π’ Updates π’', 'https://t.me/adityaserver'), 
                         Button.url('π¬ Support π¬', 'https://t.me/adityadiscus'), 
                      ], 
                      [
                        Button.url('π Source Code π', 'https://github.com/mradityaxd/tagallbot'),   
                      ]
                   ), 
                    link_preview=False
                   )

#Wah bhaiya full ignorebazzi
#tag
@aditya.on(events.NewMessage(pattern="^/tagall|/call|/tall|/all|#all|@all?(.*)"))
async def mentionall(event):
  global moment_worker
  if event.is_private:
    return await event.respond("Use This In Channel or Group!")
  
  admins = []
  async for admin in aditya.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("Only Admin can use it.")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("I can't Mention Members for Old Post!")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Give me can an Argument. Ex: `/tag Hey, Where are you`")
  else:
    return await event.respond("Reply to Message or Give Some Text To Mention!")
    
  if mode == "text_on_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in aditya.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped!")
        return
      if usrnum == 5:
        await aditya.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    moment_worker.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in aditya.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped")
        return
      if usrnum == 5:
        await aditya.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


# Cancle 

@aditya.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in moment_worker:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      moment_worker.remove(event.chat_id)
    except:
      pass
    return await event.respond('**__Stoped__**\n\n**__Powered By:__ @AdityaServer**')




print("Started Successfully Join Support")
print("Β―\_(γ)_/Β― Need Help Join @AdityaDiscus")
aditya.run_until_disconnected()
