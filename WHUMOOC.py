# coding=UTF-8

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from config import *

chrome_options = Options()
chrome_options.add_argument("--mute-audio")  # 静音
driver = webdriver.Chrome(
    executable_path=CHROMEDRIVER,  options=chrome_options
)

def play(video_id):
    play = driver.find_element_by_xpath(
        "//*[@class='vjs-big-play-button']")
    play.click()
    driver.switch_to.default_content()
    driver.switch_to.frame("iframe")
    while(True):
        try:
            finished = len(driver.find_elements_by_xpath(
                "//*[@class='ans-attach-ct ans-job-finished']"))
            if finished > video_id:
                break
        except:
            pass
        time.sleep(5)

def watch():
    try:
        driver.switch_to.frame("iframe")
        iframes = driver.find_elements_by_xpath(
            "//iframe[@class='ans-attach-online ans-insertvideo-online']")
    except:
        driver.switch_to.default_content()
        return
    
    video_num = len(iframes)

    for i in range(video_num):
        driver.switch_to.frame(iframes[i])
        play(i)

    driver.switch_to.default_content()


def main():
    driver.get('http://www.mooc.whu.edu.cn/portal')
    time.sleep(1)

    login = driver.find_element_by_class_name('loginSub')
    login.click()
    time.sleep(1)

    uname = driver.find_element_by_xpath(
        "//form[@id='casLoginForm']/*/input[@id='username']")
    uname.click()
    uname.send_keys(UNAME)

    passwd = driver.find_element_by_xpath(
        "//form[@id='casLoginForm']/*/input[@id='password']")
    passwd.click()
    passwd.send_keys(PASSWD)

    submit = driver.find_element_by_xpath(
        "//form[@id='casLoginForm']/*/button[@class='auth_login_btn primary full_width']")
    submit.click()
    time.sleep(10)

    driver.switch_to.frame("frame_content")
    course = driver.find_element_by_xpath("//li[@cname='%s']" % LESSON)
    course.click()

    time.sleep(1)
    driver.switch_to_window(driver.window_handles[1])

    lesson = driver.find_element_by_xpath("//div[@class='leveltwo']/h3/a")

    while(True):
        lesson.click()
        time.sleep(2)
        watch()
        try:
            lesson = driver.find_element_by_xpath(
                "//div[@class='orientationright ']")
        except:
            break
    driver.quit()


if __name__ == '__main__':
    main()
