from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import hashtags
import win32com.client
import random
from urllib.request import urlretrieve
import cv2
import datetime

passwords = [ "", ""]
users = ["" ,""]

#nexadesor@vmailpro.net
passwords.reverse()
users.reverse()

scrollTimes = 2
time_betwin_act = 4
breackTime = (60*10, 60*20) # betwing two secends
breackCgance = 0.01 #float prsent
everyTimeUpload = 60 * 30 #secends
speed = 1.0 #lower faster
likesPerH = 30
uploadPerH = 1

accountsList = []
fullInArrow = 0


class account:
    def __init__(self, user, password):
        self.likes = 0
        self.startTime = time.time()
        self.upload = 0
        self.user = user
        self.password = password

    def PassHour(self):
        if (time.time() - self.startTime > 60*60):
            self.likes = 0
            self.upload = 0
            self.startTime = time.time()



useHashtag = False
savedImage = False
hashList = None

mobile_emulation = {
    "userAgent": "Mozilla/5.0 (Linux; Android 8.1.0; CUBOT_POWER) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Mobile Safari/537.36" }

chrome_options = Options()

chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome('C:/Users/User/Desktop/chromedriver/chromedriver.exe', chrome_options = chrome_options)

def myPrint(txt):
    print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " : "  + txt)


def getHashtags(hashtag, one=False):
    if not one:

        returnString = []


        ranadomHashtagList = hashtag

        if hashtag:
            returnString += (hashtag)
            while ranadomHashtagList == hashtag:
                ranadomHashtagList = random.choice(hashtags.allHashtags[2:])

        returnString += (hashtags.follow)
        returnString += (hashtags.general)
        if hashtag:
            returnString += (ranadomHashtagList)

        random.shuffle(returnString)
        return " ".join(returnString[:28])
    else:
        return random.choice(random.choice(hashtags.allHashtags[2:]))

def detect_faces():
    image  = cv2.imread('C:/Users/User/TAR.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=6,
        minSize=(30, 30)
        )

    myPrint("Found {0} Faces!".format(len(faces)))
    return len(faces)

def enterText(text, name):
    user_name_elem = driver.find_element_by_xpath("//input[@name='"+ name +"']")
    user_name_elem.clear()
    user_name_elem.send_keys(text)

def click(name):
    user_name_elem = driver.find_element_by_xpath("//button[@" + name + "']")
    user_name_elem.click()

def nameTE(name):
    return "//button[@" + name + "']"

def sl():
    time.sleep(time_betwin_act * speed)

def saveImage(imageXpath):
    global savedImage
    if not savedImage:
        urlretrieve(driver.find_element_by_xpath(imageXpath).get_attribute("src"), 'C:/Users/User/TAR.png')
        savedImage = True if detect_faces() == 0 else False

def randomChance(enterFloat):
    randomNum = random.uniform(0.0,1.0)
    return True if randomNum <= enterFloat else False

def logout():
    driver.get("https://www.instagram.com/accounts/logout/")
    time.sleep(2 * speed)
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div/div/div/p/button').click()
        time.sleep(2 * speed)
        driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/button[1]').click()
        driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/button[1]').click()
    except:
        pass
    time.sleep(3 * speed)

def search(hashtag, index):
    driver.get("https://www.instagram.com/explore/tags/" + hashtag.replace("#", "") + "/")
    time.sleep(random.uniform(1.5, 3) * speed)

    # gathering photos
    pic_hrefs = []
    for i in range(1, scrollTimes):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1.5, 3) * speed)
            # get tags
            hrefs_in_view = driver.find_elements_by_tag_name('a')
            # finding relevant hrefs
            hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                             if '.com/p/' in elem.get_attribute('href')]
            # building list of unique photos
            [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            # print("Check: pic href length " + str(len(pic_hrefs)))
        except Exception:
            continue

    # Liking photos
    tempCounting = 0
    unique_photos = len(pic_hrefs)
    for pic_href in pic_hrefs:
        driver.get(pic_href)

        if (randomChance(breackCgance)):
            myPrint("start Sleeping")
            time.sleep(random.randrange(breackTime[0], breackTime[1]))
            myPrint("finish Sleeping")

        time.sleep(random.uniform(1.5, 3) * speed)
        try:
            if accountsList[index].likes >= likesPerH:
                return -1
            if tempCounting > likesPerH / 2:
                return

            time.sleep(random.uniform(1.5, 3) * speed)
            driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[2]/button').click()
            time.sleep(random.uniform(0.5, 2) * speed)

            #if blocked
            try:
                driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/button[1]").click()
                myPrint("account blocked")
                time.sleep(random.uniform(0.5, 2) * speed)
                accountsList[index].likes = likesPerH
                accountsList[index].upload = uploadPerH
                return -1
            except:
                pass

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(0.5, 2) * speed)
            driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
            time.sleep(random.uniform(0.5, 2) * speed)

            saveImage('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div/div[1]/img')
            time.sleep(random.uniform(0.5, 2) * speed)

            accountsList[index].likes += 1
            tempCounting += 1

            #for second in reversed(range(0, random.randint(18, 28))):
            #    print("#" + hashtag + ': unique photos left: ' + str(unique_photos)
             #                   + " | Sleeping " + str(second))
            #    time.sleep(1)
        except Exception as e:
            time.sleep(random.uniform(2, 3) * speed)
        unique_photos -= 1


def login(user, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2 * speed)

    enterText(user, "username")
    enterText(password, "password")
    click("type='submit")

    closePop()

def closePop():
    time.sleep(3 * speed)

    try:
        driver.find_element_by_xpath(nameTE("class='aOOlW   HoLwm ")).click()
    except:
        pass

    time.sleep(2 * speed)
    try:
        driver.find_element_by_xpath(nameTE("class='aOOlW   HoLwm ")).click()
    except:
        pass

def uploadImage():
    global savedImage

    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]').click()

    time.sleep(2 * speed)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.Sendkeys("TAR.png")
    shell.Sendkeys("~")
    time.sleep(4 * speed)

    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()
    sl()

    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/section[1]/div[1]/textarea').send_keys(getHashtags(getList(useHashtag)))
    sl()
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()
    sl()

    savedImage = False

    time.sleep(10 * speed)

def getList(OneHashtag):
    if (OneHashtag):
        for x in hashtags.allHashtags:
            if OneHashtag in x:
                return x
    else:
        return False


def main():
    global fullInArrow
    global useHashtag
    global savedImage
    global accountsList

    myPrint("start")

    for x in zip(users, passwords):
        accountsList.append(account(x[0], x[1]))


    tempHashtag = getHashtags(useHashtag, True)
    useHashtag = tempHashtag

    indexAc = 0
    while True:

        x = accountsList[indexAc]


        login(x.user, x.password)
        myPrint("login to " + x.user)

        tempHashtag = getHashtags(useHashtag, True)
        if not savedImage:
            useHashtag = tempHashtag

        x.PassHour()

        fullInArrow += 1 if search(tempHashtag, indexAc) == -1 else 0

        if (x.upload < uploadPerH):

            try:
                uploadImage()
                myPrint("upload")
                x.upload += 1
            except:
                driver.get('https://www.instagram.com')
                closePop()
                try:
                    uploadImage()
                    myPrint("upload")
                    x.upload += 1
                except:
                    myPrint("cant upload image")


        if fullInArrow >= len(accountsList):
            logout()

            accountsList.sort(key=lambda y: y.startTime)
            indexAc = 0

            sleepTime = 1 + 60*60 - (time.time() - accountsList[0].startTime)

            if (sleepTime < 0):
                myPrint("full use sleep time is negative! (" + str(sleepTime) + ")")
                continue

            myPrint("full use; sleep for " + str(int(sleepTime/60)) + " Minutes")
            time.sleep(sleepTime)

        else:
            indexAc = (indexAc + 1) % len(accountsList)
            logout()
            myPrint("logout from " + x.user)

        savedImage = False

        #TODO: like my oun image

if __name__ == '__main__':
    main()
