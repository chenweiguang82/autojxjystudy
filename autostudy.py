# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
import time, sys

class Course(object):
    def __init__(self,driver,link_text,xpath,course_class_name):
        self.study = driver.find_elements_by_link_text(link_text)
        self.embed = driver.find_elements_by_xpath(xpath)
        self.total_course=driver.find_element_by_class_name(course_class_name).text.split('\n')
        
    def print_current_status(self):
        print('当前课程学习情况:')
        print('==============')
        for i in range(self.get_courses_num()):
            print('%s\t\t%d%%\n' %(self.total_course[i+1].split()[0],self.get_percent()[i]))
        
    def get_percent(self):
        return [int(x.get_attribute('src').split('=')[1]) for x in self.embed]
    
    def get_courses_num(self):
        return len(self.study)
    
    def is_finished(self):
        return sum([x < 100 for x in self.get_percent()]) == 0
    
    def unfinished_courses_num(self):
        tmp = []
        tmp1 = self.get_percent()
        for x in range(len(tmp1)):
            if (tmp1[x] < 100):
                tmp.append(x)
        return tmp
    
    def do_study(self):
        if self.is_finished():
            print('课程已学完')
        else:
            for x in self.unfinished_courses_num():
                self.study[x].click()
                print('准备学习课程:%s\n' %(self.total_course[x+1].split()[0]))
                break

def AutoAnswer(driver):
        message=driver.find_element_by_class_name('ui_main')
        if message.text == '':
            return False
        else:
            tmp=message.text.split('\n')[0]
            question=eval(tmp.split('：')[1].split('=')[0])
            
            for x in message.text.split('\n')[1:4]:
                if question == int(x.split()[1]):
                    answer = x.split()[0]
                    break
            option=driver.find_element_by_id('radio_'+answer)
            option.click()
            time.sleep(1)
            button=driver.find_element_by_id('but_Question')
            button.click()
            return True

def CountDown(Seconds):
    for i in range(Seconds):
        sys.stdout.write('\r%3d' %(Seconds-i))
        time.sleep(1)
    print('')

###############
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
#driver.get('http://szpx.haacee.org.cn')
driver.get('http://zjpx.hnhhlearning.com/')
CountDown(10)
print('已登录网站：%s' %(driver.title))
print('请在30秒钟之内登录')
CountDown(30)
#登录
#之后运行下面的

courses = Course(driver,'进入学习','//embed','homelinetable-dashed-bom')
courses.print_current_status()
#embed=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div/table/tbody/tr[2]/td[3]/embed')
while courses.is_finished != False:
    courses.do_study()
    CountDown(10)
    
    chapter = Course(driver,'进入学习','//embed','xktable')
    chapter.print_current_status()
    while chapter.is_finished != False:
        chapter.do_study()
        CountDown(10)
    
        chapter_windows = driver.current_window_handle
        all_handles = driver.window_handles    
        for handle in all_handles:
            if handle != chapter_windows:
                driver.switch_to_window(handle)
             
        video=driver.find_element_by_id('p2ps_video')
        video.click()
        progress=driver.find_element_by_id('div_ProgressBar_value')
        while True:
            prog=int(progress.text.split('%')[0])
            if prog != 100:
                if AutoAnswer(driver):
                    print('\n已自动答题')
                    time.sleep(10)
                else:
                    sys.stdout.write('\r正在学习中...%3d%%\r' %(prog))
                    time.sleep(60)
            else:
                break
        driver.close()
        driver.switch_to_window(chapter_windows)
        driver.refresh()
        time.sleep(10)
        chapter = Course(driver,'进入学习','//embed','xktable')
    
    driver.back()
    driver.refresh()
    time.sleep(10)
    courses = Course(driver,'学习','//embed','homelinetable-dashed-bom')
    
print('你的课程已经全部完成')


#driver.quit()
