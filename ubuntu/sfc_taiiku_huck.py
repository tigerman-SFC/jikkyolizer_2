# -*- coding: utf-8 -*-
from pyvirtualdisplay import Display
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
import lxml.html
import requests
import time
from datetime import datetime
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HuckSfcTaiiku:
    def __init__(self, login, password, dating, period, sports, teacher):
        self.x_window = 1200
        self.y_window = 1600
        self.login = login
        self.password = password
        self.dating = dating
        self.period = period
        self.sports = sports
        self.teacher = teacher

    def set_up(self):
        self.display = Display(visible=0, size=(self.x_window, self.y_window))
        self.display.start()
        self.browser = webdriver.Firefox()   #実験では、34秒のタイム。
        self.end_of_function_print(sys._getframe().f_code.co_name)


    def browser_get(self):
        self.browser.get('https://wellness.sfc.keio.ac.jp/v3/')   #実験では、17秒のタイム
        try:
            element = WebDriverWait(self.browser, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bottom"))
            )
        except:
            self.print_function_error(sys._getframe().f_code.co_name + '0')
            sys.exit()
        try:
            element1 = WebDriverWait(self.browser, 100).until(
                EC.visibility_of_element_located((By.NAME, "login"))
            )
            element1 = self.browser.find_element_by_name("login")
            element1.send_keys(self.login)
            element2 = self.browser.find_element_by_name("password")
            element2.send_keys(self.password)
            element3 = self.browser.find_element_by_name("submit")
            element3.click()
        except:
            self.print_function_error(sys._getframe().f_code.co_name + '1')
            sys.exit()
        self.end_of_function_print(sys._getframe().f_code.co_name)

    def to_page_make_reservation(self):
        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "Make Reservation"))
            )
            element.click()
        except:
            self.print_function_error(sys._getframe().f_code.co_name)
            sys.exit()
        self.end_of_function_print(sys._getframe().f_code.co_name)
    
    def to_page_all_two_week(self):
        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "Show all the available classes for the next two weeks."))   #2週間全ての講義を取得
            )
            element.click()
        except:
            self.print_function_error(sys._getframe().f_code.co_name)
            sys.exit()
        self.end_of_function_print(sys._getframe().f_code.co_name)

    def click_target_content(self):
        y_scroll = 0
        flag_y_scroll = 0
        for number_of_title in range(2,300):
            try:
                print (str(number_of_title))
                sports = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[3]/table[2]/tbody/tr["+str(number_of_title)+"]/td[3]"))
                )
                dating = browser.find_element_by_xpath("/html/body/div/div[3]/table[2]/tbody/tr["+str(number_of_title)+"]/td[1]")
                period = browser.find_element_by_xpath("/html/body/div/div[3]/table[2]/tbody/tr["+str(number_of_title)+"]/td[2]")
                print (dating.text)
                flag_y_scroll = 0
                if (sports.text == self.sports) and (dating.text == self.dating) and (period.text == self.period):
                    self.browser.find_element_by_xpath('/html/body/div/div[3]/table[2]/tbody/tr['+str(number_of_title)+']/td[6]/following-sibling::td').click()
                    now_string = self.get_now_string()
                    print ("Clicked!" + now_string)
                    self.end_of_function_print(sys._getframe().f_code.co_name + '1')
                    return 1
            except:
                if flag_y_scroll == 0:
                    y_scroll += self.y_window
                    self.browser.execute_script("window.scrollTo(0, " + str(y_scroll) + ");")
                    flag_y_scroll = 1
                else:
                    #print '/html/body/div/div[3]/table[2]/tbody/tr[' + str(number_of_title) + ']/td[3]'   #後にこの行全てをコメントアウト
                    now_string = self.get_now_string()
                    print ("Nothing!" + now_string)
                    self.end_of_function_print(sys._getframe().f_code.co_name + '0')
                    return 0


    def push_button_reservation(self):
        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[3]/form/p/input[1]"))
            )
            self.browser.save_screenshot('testshot30.png')
            element.click()
        except:
            self.print_function_error(sys._getframe().f_code.co_name)
            sys.exit()
        self.end_of_function_print(sys._getframe().f_code.co_name)          

    def push_button_kakutei(self):
        try:
            time.sleep(2)
            element = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[3]/form/p/input[1]"))
            )
            element.click()
            time.sleep(2)
            self.check_kakutei()
        except:
            self.print_function_error(sys._getframe().f_code.co_name)
            sys.exit()
        self.end_of_function_print(sys._getframe().f_code.co_name)     

    def check_kakutei(self):
        try:
            element1 = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[2]/ul/li[2]/a"))
            )
            element1.click()

            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "bottom"))
            )
            for reserve_num in range(2,20):
                dating = browser.find_element_by_xpath('/html/body/div/div[3]/form/table/tbody/tr[ ' + str(reserve_num) + ']/td[1]')
                period = browser.find_element_by_xpath('/html/body/div/div[3]/form/table/tbody/tr[ ' + str(reserve_num) + ']/td[2]')
                sports = browser.find_element_by_xpath('/html/body/div/div[3]/form/table/tbody/tr[ ' + str(reserve_num) + ']/td[3]')
                if (sports.text == self.sports) and (dating.text == self.dating) and (period.text == self.period):
                    print ('Mission Complete!')
                    sys.exit()
        except:
            self.print_function_error(sys._getframe().f_code.co_name)
            sys.exit()
        self.end_of_function_print(sys._getframe().f_code.co_name)  

    def get_now_string(self):
        now_string = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return now_string

    def end_of_function_print(self, func_name):
        now_string = self.get_now_string()
        output_string = func_name + '-Completed! ' + now_string
        print (output_string)

    def print_function_error(self, func_name):
        now_string = self.get_now_string()
        output_string = func_name + '-Failed! ' + now_string
        print (output_string)

    def display_now_html(self):
        root = lxml.html.fromstring(self.browser.page_source)
        print (root.text_content())

    

if __name__ == "__main__":
    args = sys.argv 
    date_string = ' ' + args[1]
    control_window = HuckSfcTaiiku('s15108yi', 'Yoshi852046!', 'date_string', 'args[2]', 'args[3]', 'args[4]')
    control_window.set_up()   #仮想ディスプレイの起動、firefoxの起動。
    while True:
        control_window.browser_get()   #体育システムのトップページへと移動する。
        control_window.to_page_make_reservation()   #予約ページへと遷移。
        control_window.to_page_all_two_week()   #2週間分の講義を全て表示。
        reservation_flag = control_window.click_target_content()   #対象の講義をクリック。
        if reservation_flag == 1:
            control_window.push_button_reservation()   #予約ボタンをクリック。
        else:
            pass
        control_window.push_button_kakutei()
        control_window.display_now_html()
        time.sleep(5)
