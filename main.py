from telethon.sync import TelegramClient, events
from telethon import functions, types
import requests, json, os, time
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Replace with your API credentials
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
api_url = os.getenv("API_URL")
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")
si = ""

global_guide='(چند جواب متفاوت بده)'
guides={
    'ددد': 'دوباره نویسی کن',
    'ییی': 'معنی کن',
    'چچچ': 'مردم در پاسخ به این سوال عموما چه میگویند',
    'ففف': 'نوع هر کلمه را از لحاظ ساختار جمله در دستور زبان فارسی مشخص کن',
    'پپپ': 'جای خالی را پر کن',
    'ججج' : 'جمله بساز',
    'ششش' : 'با این کلمه/کلمات رباعی بساز',

}

guides_text=''
for g in guides.items():
    guides_text += ':\t'.join(g)
    guides_text += '\n'
guide = f"""راهنمای ربات ناشنوایار:
```{guides_text}
لطفاً در استفاده از ربات دقت کنید و از عبارت‌های مناسب استفاده کنید تا پاسخ‌های دقیق‌تری دریافت کنید.
برای کسب اطلاعات بیشتر، می‌توانید به وب‌سایت ناشنوایار مراجعه کنید.```
website: http://masoudsoft.ir
channel:  @masouds0ft
support: @fsdevel
"""
def event2resp(etext):
    
    # Add a guide to the input Text
    '''
    if "❌" in etext:
       etext = 'ددد: '+ etext
       etext = etext.replace('❌','')
    if 'یعنی چی' in  etext:
        etext = 'ییی: '+ etext
        etext = etext.replace('یعنی چی','')
    if 'یعنی' in  etext:
        etext = 'ییی: '+ etext
        etext = etext.replace('یعنی','')
    if etext.endswith('درسته؟'):
        etext = 'ددد: '+ etext
        etext = etext.replace('درسته؟','')
    if etext.endswith('درسته؟'):
        etext = 'ددد: '+ etext
        etext = etext.replace('درسته؟','')
    if etext.endswith('درسته'):
        etext = 'ددد: '+ etext
        etext = etext.replace('درسته','')
    if 'یعنی چه' in  etext:
        etext = 'ییی: '+ etext
        etext = etext.replace('یعنی چه','')
    if 'چی بگم' in  etext:
        etext = 'ججج: '+ etext
        etext = etext.replace('چی بگم','')
        
    '''
    if etext == '؟؟؟':
        return guide
    if len(etext)<4 or ':' not in etext: 
        return None
    
    cmd, text = etext.split(':')
    cmd = cmd.strip()
    text = text.strip()
    print('Command: ',cmd)
    print('Text: ',text)
    
    if cmd in guides:
        
        fullurl = f"{api_url}{global_guide}{guides[cmd]}: «{text}»"
        response = None
        while not response:
            try:
                response = requests.get(fullurl)
            except:
                print('retry')
                time.sleep(10)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response as JSON
            data = json.loads(response.text)
            return data["message"]
        else:
            # Handle the error
            print("Error: Could not retrieve data from API")
    
    return None

with TelegramClient('name', api_id, api_hash) as bot:

    @bot.on(events.NewMessage(chats=os.getenv("CHAT_ID").split(',')))
    async def handler(event):
        answer = event2resp(event.text)
        if answer:
            if event.reply_to:
                await bot.send_message(
                        entity=event.chat_id,
                        message=answer[:4000]+'\n✅',
                        reply_to = event.reply_to.reply_to_msg_id)
                

            else:
                await event.reply(answer[:4000]+'\n✅')
            
            if len(answer)>4000:
                time.sleep(5)
                await event.reply(answer[4000:8000]+'\n✅')
                
            print("\n-USER: ",event.text,"\n -BOT: ",answer)
        
    # Start the bot
    bot.run_until_disconnected()
    
print('Daefriend bot started.')