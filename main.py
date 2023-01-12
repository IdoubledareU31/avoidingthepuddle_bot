from telebot.async_telebot import AsyncTeleBot 
import pytube
import time
import asyncio

# Let's start working with PyTelegramBotAPI

with open ("token.txt", "r") as f:
    token = f.read()
    
bot = AsyncTeleBot(token)

latest_video_url=""
mychat_id=0

# pytube was updated with the following: "https://github.com/pishiko/pytube/tree/fix-channel"
# otherwise the url won't be accepted (and still it does not allow for original youtube urls;
# use the scheme as follows


# check if the current video is the latest video
# add the information about the latest video to the txt file
async def new_video_check():
    global latest_video_url
    # Cheking if there are any new videos on @Avoidingthepuddle channel on youtube
    c = pytube.Channel("https://www.youtube.com/user/AvoidingthePuddle")
    # latest_video_url = c.video_urls
    # print ("this is the list of urls: ", latest_video_url)
    latest_video_url = c.video_urls[:1][0]
    print (latest_video_url)
    link=latest_video_url
    with open("latest_video.txt", "r") as f:
        latest_vid = f.read()
    if link == latest_vid:
        print ("There are no new videos")
        return False
    else:
        print ("New video found")
        with open ("latest_video.txt", "w") as f:
            f.write(link)
        print ("Link updated")
        return True

#let's create how bot will send a message

@bot.message_handler(commands=["status", "start"])
async def send_status(message):
    global mychat_id
    with open ("users.txt", "r") as f:
        users = f.read()
        print (f.read())
        print (str(message.chat.id))
        f.close()
    if str(message.chat.id) not in users:
        with open ("users.txt", "a") as file:
           file.write(str(message.chat.id)+", ")
    await bot.send_message(message.chat.id, "The bot is alive! Here's the latest video from Aris:\n{}".format(latest_video_url))


async def cheking_yutube():
    task1 = asyncio.create_task(mypolling())
    #result1 = await task2
    while True:
        with open ("users.txt", "r") as f:
            list_of_users = f.read().split(", ")[:-1]
        print (list_of_users)
        task2 = asyncio.create_task(new_video_check())
        result = await task2
        print (result)
        if result:
            for user_id in list_of_users:
                await bot.send_message(int(user_id), "NEW VIDEO:\n{}".format(latest_video_url))
        else:
            print("There's no new video")
           #  for user_id in list_of_users:
           #      await bot.send_message(user_id, "There's no new video")
        await asyncio.sleep(2500)

async def mypolling():
    await bot.polling(non_stop=True, request_timeout=300)


asyncio.run (cheking_yutube())



