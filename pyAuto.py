from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
import wikipedia
desired_caps = {
  "deviceName": "emulator-5554",
  "platformName": "android",
  "appPackage": "com.into.sketchit",
  "appActivity": ".LoginScreen",
  "noReset": True
}
responses = {'bilal':'legend','aq':'100iq','abhi':'legend','sk':'legend','divya':'mosi','xoya':'tharki','leo':'the boss'}
admins = ['abhi1002', 'bilaldra1']
score = {}
turns = {}

driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
prevMSG = ""
default_room = 'bot_room'
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def sendMsgToCurrentRoom(driver, message):
    msgTxtBox = driver.find_element_by_id("com.into.sketchit:id/chatEditText")
    msgTxtBox.send_keys(message)
    sendButton = driver.find_element_by_id("com.into.sketchit:id/buttonSendChat")
    sendButton.click()

def switchRoom(driver, roomName):
    # if(roomName[0] != '#'):
    #     el3 = driver.find_element_by_accessibility_id("minecraft")
    #     el3.click()
    # else: 
        roomObj = driver.find_element_by_xpath("//androidx.appcompat.app.ActionBar.b[@content-desc=\"" + roomName + "\"]/android.widget.TextView")
        roomObj.click()

def onStartUp(driver):
    el1 = driver.find_element_by_xpath("//android.widget.TextView[@content-desc=\"Chat\"]")
    el1.click()
    # el2 = driver.find_element_by_xpath("//androidx.appcompat.app.ActionBar.b[@content-desc=\"Z0MBIES\"]/android.widget.TextView")
    # el2.click()
    switchRoom(driver,default_room)


def getMessager_Name(driver):
    message_info = {'messager_name':'sibot001','message':'nothing ok?'}
    for i in ['15','14','13','12','11','10','9','8','7','6','5','4','3','2','1','0']:
        if(check_exists_by_xpath(driver,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.FrameLayout["+i+"]/android.widget.LinearLayout/android.widget.TextView") and check_exists_by_xpath(driver, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.FrameLayout["+i+"]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView")):
            try:
                messager_name = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.FrameLayout["+i+"]/android.widget.LinearLayout/android.widget.TextView").text
                message = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.FrameLayout["+i+"]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView").text
                message_info['messager_name'] = messager_name
                message_info ['message'] = message
            except Exception:
                message_info['messager_name'] = "nothing ok?"
                message_info ['message'] = "nothing ok?"
            break
    return message_info
 
def reply(driver, message_info):
    spam_limit = 5
    message = message_info['message']
    messager = message_info['messager_name']
    split_message = message.split()

    if(split_message[1] == "help"):
        sendMsgToCurrentRoom(driver,"TYPE \"sibot <your_message>\" to interact with me")
        sendMsgToCurrentRoom(driver,"TYPE \"sibot set <your_message> -> <reply_for_that_message>\" to feed into my responses")
        sendMsgToCurrentRoom(driver,"Added a dice game,  Commands 1) rolldice 2) resetdice 3) showscores")
        sendMsgToCurrentRoom(driver,"Added a rating command, TYPE sibot rate any_entity")
        return 0

    if(split_message[1] == "exit" and messager in admins):
        return 1

    if(message[-1] == '?'):
        sendMsgToCurrentRoom(driver,random.choice(['Yes','No','well actually yes, but no','well actually no, but yes']))
        return 0

    if(split_message[1] == "rate"):
        sendMsgToCurrentRoom(driver,str(random.choice(range(1,11))) + " / 10")

    if(split_message[1] == "rolldice"):
        die = random.choice(range(1,7))
        sendMsgToCurrentRoom(driver,"rolling.... its a " + str(die))
        if(messager in score.keys()):
            score[messager] = score[messager] + die
            turns[messager] = turns[messager] + 1
        else:
            score[messager] = die
            turns[messager] = 0
        sendMsgToCurrentRoom(driver,messager + " current score is " + str(score[messager]))
    if(split_message[1] == "resetdice" and messager in score.keys() ):
        score.clear()
        turns.clear()
        sendMsgToCurrentRoom(driver, " Scores resetted to zero ")
    if(split_message[1] == "showscore"):
        if(len(score) > 0):
            for i in score.keys():
                sendMsgToCurrentRoom(driver, i + " -> " + str(score[i]) + ", turns = " + str(turns[i]))
        else:
            sendMsgToCurrentRoom(driver,"1st play to display scores :3")


    if(split_message[1] == "spam"):
        cnt = 0
        msg = split_message[3]
        try:
            cnt = int(split_message[2])
        except Exception:
            cnt = 1
            msg = split_message[2]
        if(cnt > spam_limit):
            sendMsgToCurrentRoom(driver,"spam_limit is : " + str(spam_limit))
        else:
            msg = message.split(split_message[2])[1].strip()
            for i in range(0,cnt):
                sendMsgToCurrentRoom(driver,msg)


    if(split_message[1] == "set" and len(split_message) >= 5 ):
        intent = split_message[2].strip()
        response = message.split("->")[1].strip()
        if(intent == "spam_limit" and messager in admins):
            spam_limit = int(response)
        else:
            responses[intent] = response
        sendMsgToCurrentRoom(driver,"Response recorded")

    #switchRoom(driver,"bot_com")
    sendMsgToCurrentRoom(driver,messager + " said \"" + message.split('sibot')[1] + "\"")
    #switchRoom(driver,default_room)
    #sendMsgToCurrentRoom(driver,wikipedia.summary("hi"))
    return 0















 
onStartUp(driver)
spam_limit = 10
sendMsgToCurrentRoom(driver,"SI BOT Started")
sendMsgToCurrentRoom(driver,"type sibot help for more details")
exit = 0
while(exit != 1):
    message_info = getMessager_Name(driver)
    if(prevMSG != message_info['message'] and message_info['message'].split()[0] == 'sibot'):
        try:
            prevMSG = message_info['message']
            exit = reply(driver,message_info )
        except Exception:
            sendMsgToCurrentRoom(driver,"SRY CANT PROCESS A REPLY")
    elif(message_info['message'] in responses.keys()):
        sendMsgToCurrentRoom(driver,responses[message_info['message']])
    # elif(message _info['messager_name'] != 'SI_BOT001'):
    #     sendMsgToCurrentRoom(driver,"HI  " + message_info['messager_name'])

    #time.sleep(0.5)
sendMsgToCurrentRoom(driver,"exiting SI BOT.....")

#driver.quit()
print("YO")