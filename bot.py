from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import hashtags
import win32com.client
import random
from urllib.request import urlretrieve
import cv2
import datetime

CHROMEDRIVER_PATH = r"C:\Users\User\Desktop\Python\SeleniumScripts\chromedriver.exe"
scrollTimes = 1
time_betwin_act = 4
breackTime = (60*10, 60*20)  # betwing two secends
breackCgance = 0.01  # float prsent
everyTimeUpload = 60 * 30  # secends
speed = 1.0  # lower faster
likesPerH = 30
upload_per_h = 1


def read_users_data():
    """
    read user passwords and names    
    """
    f = open("passwords.txt", "r")
    lines = f.readlines()
    lines = list(map(lambda x: x.replace("\n", ""), lines))
    for user_name, password in zip(lines[::2], lines[1::2]):
        yield Account(user_name, password)


class Account:
    def __init__(self, user, password):
        self.likes = 0
        self.start_time = time.time()
        self.upload = 0
        self.user = user
        self.password = password

    def pass_hour(self):
        """
        if pass hour and can reset the timers
        """
        if time.time() - self.start_time > 60*60:
            self.likes = 0
            self.upload = 0
            self.start_time = time.time()


def log_print(txt):
    """
    print with time
    """
    print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " : " + txt)


def get_hashtags(hashtag, one=False):
    """
    get random hashtags
    """
    if not one:

        return_string = []
        ranadom_hashtag_list = hashtag

        if hashtag:
            return_string += hashtag
            while ranadom_hashtag_list == hashtag:
                ranadom_hashtag_list = random.choice(hashtags.all_hashtags[2:])

        return_string += hashtags.follow
        return_string += hashtags.general
        if hashtag:
            return_string += ranadom_hashtag_list

        random.shuffle(return_string)
        return " ".join(return_string[:28])
    else:
        return random.choice(random.choice(hashtags.all_hashtags[2:]))


def detect_faces():
    """
    check in downloaded image have a face    
    """
    image = cv2.imread('C:/Users/User/TAR.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=6,
        minSize=(30, 30)
        )

    log_print("Found {0} Faces!".format(len(faces)))
    return len(faces)


def enter_text(text, name, driver):
    """
    enter text to input    
    """
    user_name_elem = driver.find_element_by_xpath("//input[@name='" + name + "']")
    user_name_elem.clear()
    user_name_elem.send_keys(text)


def click(name, driver):
    """
    click on button
    """
    user_name_elem = driver.find_element_by_xpath("//button[@" + name + "']")
    user_name_elem.click()


def name_te(name):
    return "//button[@" + name + "']"


def sl():
    time.sleep(time_betwin_act * speed)


def save_image(image_xpath, driver):
    global savedImage
    if not savedImage:
        urlretrieve(driver.find_element_by_xpath(image_xpath).get_attribute("src"), 'C:/Users/User/TAR.png')
        savedImage = True if detect_faces() == 0 else False


def random_chance(enter_float):
    random_num = random.uniform(0.0, 1.0)
    return True if random_num <= enter_float else False


def logout(driver):
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


def search(hashtag, index, accounts_list, driver):
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
    temp_counting = 0
    unique_photos = len(pic_hrefs)
    for pic_href in pic_hrefs:
        driver.get(pic_href)

        if (random_chance(breackCgance)):
            log_print("start Sleeping")
            time.sleep(random.randrange(breackTime[0], breackTime[1]))
            log_print("finish Sleeping")

        time.sleep(random.uniform(1.5, 3) * speed)
        try:
            if accounts_list[index].likes >= likesPerH:
                return -1
            if temp_counting > likesPerH / 2:
                return

            ''

            time.sleep(random.uniform(1.5, 3) * speed)
            driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[2]/button').click()
            time.sleep(random.uniform(0.5, 2) * speed)

            # if blocked
            try:
                driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/button[1]").click()
                log_print("account blocked")
                time.sleep(random.uniform(0.5, 2) * speed)
                accounts_list[index].likes = likesPerH
                accounts_list[index].upload = upload_per_h
                return -1
            except:
                pass

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(0.5, 2) * speed)
            driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button').click()
            time.sleep(random.uniform(0.5, 2) * speed)

            save_image('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div/div[1]/img', driver)
            time.sleep(random.uniform(0.5, 2) * speed)

            accounts_list[index].likes += 1
            temp_counting += 1

        except:
            time.sleep(random.uniform(2, 3) * speed)
        unique_photos -= 1


def login(user, password, driver):
    """
    try to login
    """
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2 * speed)

    enter_text(user, "username", driver)
    enter_text(password, "password", driver)
    click("type='submit", driver)

    close_pop(driver)


def close_pop(driver):
    """
    try to close pop
    """
    time.sleep(3 * speed)

    try:
        driver.find_element_by_xpath(name_te("class='aOOlW   HoLwm ")).click()
    except:
        pass

    time.sleep(2 * speed)
    try:
        driver.find_element_by_xpath(name_te("class='aOOlW   HoLwm ")).click()
    except:
        pass


def upload_image(driver):
    global savedImage

    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]').click()

    time.sleep(2 * speed)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.Sendkeys("TAR.png")
    shell.Sendkeys("~")
    time.sleep(4 * speed)

    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()
    sl()

    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/section[1]/div[1]/textarea').send_keys(get_hashtags(get_list(True)))
    sl()
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()
    sl()

    savedImage = False

    time.sleep(10 * speed)


def get_list(one_hashtag):
    if one_hashtag:
        for x in hashtags.all_hashtags:
            if one_hashtag in x:
                return x
    else:
        return False


def main():
    accounts_list = list(read_users_data())
    
    full_in_arrow = 0
    use_hashtag = False
    saved_image = False
    
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 8.1.0; CUBOT_POWER) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Mobile Safari/537.36"}
    
    chrome_options = Options()
    
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
    
    log_print("start")

    temp_hashtag = get_hashtags(use_hashtag, True)
    use_hashtag = temp_hashtag

    index_ac = 0
    while True:

        x = accounts_list[index_ac]

        login(x.user, x.password, driver)
        log_print("login to " + x.user)

        temp_hashtag = get_hashtags(use_hashtag, True)
        if not saved_image:
            use_hashtag = temp_hashtag

        x.pass_hour()

        full_in_arrow += 1 if search(temp_hashtag, index_ac, accounts_list, driver) == -1 else 0

        if x.upload < upload_per_h:

            try:
                upload_image(driver)
                log_print("upload")
                x.upload += 1
            except:
                driver.get('https://www.instagram.com')
                close_pop(driver)
                try:
                    upload_image(driver)
                    log_print("upload")
                    x.upload += 1
                except:
                    log_print("cant upload image")

        if full_in_arrow >= len(accounts_list):
            logout(driver)

            accounts_list.sort(key=lambda y: y.startTime)
            index_ac = 0

            sleep_time = 1 + 60*60 - (time.time() - accounts_list[0].start_time)

            if sleep_time < 0:
                log_print("full use sleep time is negative! (" + str(sleep_time) + ")")
                continue

            log_print("full use; sleep for " + str(int(sleep_time / 60)) + " Minutes")
            time.sleep(sleep_time)

        else:
            index_ac = (index_ac + 1) % len(accounts_list)
            logout(driver)
            log_print("logout from " + x.user)

        saved_image = False

        # TODO: like my oun image


if __name__ == '__main__':
    main()
