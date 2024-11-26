#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   csdn_auto_publisher.py
@Time    :   2024-11-26 21:21:24
@Author  :   Ez
@Version :   1.0
@Desc    :   None


pyperclip==1.9.0 
selenium==4.26.1 

'''

import os 
import time
import sys
import pyperclip 
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait 


login_url = 'https://passport.csdn.net/login'
pub_url   = 'https://editor.csdn.net/md/'  
 
options = webdriver.chrome.options.Options()
options.page_load_strategy = 'normal'  
driver = webdriver.Chrome(options=options)

# 使用账号密码登录 
def login(username, password):

    driver.get(login_url)
    time.sleep(1)  # 等待2秒

    # pw_button = driver.find_element(By.XPATH, '//span[@class="tabs-active"]') # 无效
    pw_button = driver.find_element(By.XPATH, '//div[@class="login-box-tabs-items"]//span[contains(text(),"密码登录")]') 
    pw_button.click()
    time.sleep(1) 
 
    name_field = driver.find_element(By.XPATH, '//input[@autocomplete="username"]')  
    name_field.clear() 
    name_field.send_keys(username)
    # time.sleep(1)
    pw_field = driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]')  
    pw_field.clear() 
    pw_field.send_keys(password)
    # time.sleep(1) 
    service_btn = driver.find_element(By.XPATH, '//i[@class="icon icon-nocheck"]')
    service_btn.click() 
    # time.sleep(1) 
    login_btn = driver.find_element(By.XPATH, '//button[@class="base-button"]')   
    login_btn.click() 
    time.sleep(5)
 

def csdn_publisher(driver, article): 
 
    driver.switch_to.new_window('tab')  
 
    driver.get(pub_url)
    time.sleep(2)  # 等待2秒
 
    title = driver.find_element(By.XPATH, '//div[contains(@class,"article-bar")]//input[contains(@placeholder,"请输入文章标题")]')
    title.clear() 
    title.send_keys(article.title)
    time.sleep(1)  # 等待3秒
 
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL  
    back_ctrl = Keys.BACKSPACE if sys.platform == 'darwin' else Keys.BACKSPACE  
    
    action_chains = webdriver.ActionChains(driver)
    content = driver.find_element(By.XPATH, '//div[@class="editor"]//div[@class="cledit-section"]')
    content.click()  
    time.sleep(1)
    
    # 清除原来的内容 
    action_chains.key_down(cmd_ctrl).send_keys('a').key_up(cmd_ctrl).perform()
    time.sleep(1) 
    action_chains.key_down(back_ctrl).perform()
    time.sleep(1)  

    content = driver.find_element(By.XPATH, '//div[@class="editor"]//div[@class="cledit-section"]')
    content.click()  
    time.sleep(1)  

    pyperclip.copy(article.content)
    time.sleep(1) 
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(1)  # 等待3秒
 

    # 发布文章
    send_button = driver.find_element(By.XPATH, '//button[contains(@class, "btn-publish") and contains(text(),"发布文章")]')
    send_button.click()
    time.sleep(2)

    # 文章标签
    if len(article.tags) > 0:
        add_tag = driver.find_element(By.XPATH,
                                        '//div[@class="mark_selection"]//button[@class="tag__btn-tag" and contains(text(),"添加文章标签")]')
        add_tag.click()
        time.sleep(1)
        tag_input = driver.find_element(By.XPATH, '//div[@class="mark_selection_box"]//input[contains(@placeholder,"请输入文字搜索")]')
        for tag in article.tags:
            tag_input.send_keys(tag)
            time.sleep(2)
            tag_input.send_keys(Keys.ENTER)
            time.sleep(1)

        # 关闭按钮
        close_button = driver.find_element(By.XPATH, '//div[@class="mark_selection_box"]//button[@title="关闭"]')
        close_button.click()
        time.sleep(1)

    # 文章封面
    if len(article.cover_img_path) > 0:
        file_input = driver.find_element(By.XPATH, "//input[@class='el-upload__input' and @type='file']")
        # 文件上传不支持远程文件上传，所以需要把图片下载到本地
        file_input.send_keys( article.cover_img_path)
        time.sleep(2)

    # 摘要 
    if len(article.summary) > 0:
        summary_input = driver.find_element(By.XPATH, '//div[@class="desc-box"]//textarea[contains(@placeholder,"摘要：会在推荐、列表等场景外露")]')
        summary_input.send_keys(article.summary)
        time.sleep(2)

    # 分类专栏 
    if len(article.categories) > 0:
        # 先点击新建分类专栏
        add_category = driver.find_element(By.XPATH, '//div[@id="tagList"]//button[@class="tag__btn-tag" and contains(text(),"新建分类专栏")]')
        add_category.click()
        time.sleep(1)
        for category in article.categories:
            category_input = driver.find_element(By.XPATH, f'//input[@type="checkbox" and @value="{category}"]/..')
            if category_input == None:continue 
            category_input.click()
            time.sleep(1)
        # 点击关闭按钮
        close_button = driver.find_element(By.XPATH, '//div[@class="tag__options-content"]//button[@class="modal__close-button button" and @title="关闭"]')
        close_button.click()
        time.sleep(1)

    # 可见范围
    visibility = '粉丝可见'
    
    visibility_input = driver.find_element(By.XPATH,f'//div[@class="switch-box"]//label[contains(text(),"{visibility}")]')
    parent_element = visibility_input.find_element(By.XPATH, '..')
    parent_element.click()

    if len(article.pub_date.strip()) == 0:    # 立即发布  
        publish_button = driver.find_element(By.XPATH, '//div[@class="modal__inner-2"]//button[contains(text(),"发布文章")]')
        publish_button.click()
        time.sleep(6)
        return 1


    # 定时发布 
    scheduled_btn = driver.find_element(By.XPATH, '//div[@class="modal__inner-2"]//button[contains(text(),"定时")]') 
    scheduled_btn.click()
    time.sleep(1) 

    # 选择时间 
    date_picker = driver.find_element(By.XPATH, '//input[@placeholder="选择日期"]')    
    date_picker.find_element(By.XPATH, '..').click()

    date = driver.find_element(By.XPATH, f'//div[@class="el-picker-panel__body-wrapper"]//td[contains(@class, "available")]//span[text()={article.pub_date}]')   
    date.find_element(By.XPATH, '..').click()

    time.sleep(1) 
    time_picker = driver.find_element(By.XPATH, '//input[@placeholder="选择时间"]')   
    time_picker.find_element(By.XPATH, '..').click()
    time.sleep(1) 
     
    time_btn = driver.find_element(By.XPATH, f"//div[@class='el-scrollbar']//div[text()='{article.pub_time}']")   
    time_btn.click()  
    time.sleep(1) 
    scheduled_btn2 = driver.find_element(By.XPATH, '//div[@class="el-dialog__footer"]//button[contains(text(),"定时发布")]') 
    scheduled_btn2.click()  
     
    time.sleep(6)
    return 1


class Article(object):
    def __init__(self, file_path) -> None:
        # self.title = ''
        self.file_path = file_path 

        all_content = open(self.file_path).read().strip()

        self.title = all_content.split('\n')[0].strip()
        self.content = all_content[len(self.title):].strip() 
        if self.title.startswith('# '):self.title = self.title[2:].strip() 
        self.summary = ''

        self.tags = []  
        self.cover_img_path = ''
        self.categories = [] 

        self.pub_date = '' # 定时发布日  如，1,2 需在未来一周之内
        self.pub_time = '08:15' # 定时发布时间，遵守发布时的显示样式
 

# 测试发布整个文件夹
def test_dir_pub():
 
    src_dir = '' 
    save_dir = os.path.join(src_dir, 'pub')
    if not os.path.isdir(save_dir):os.makedirs(save_dir) 
    
    for file_name in os.listdir(src_dir):
        file_path = os.path.join(src_dir, file_name) 
        done_path = os.path.join(save_dir, file_name) 

        try:
            article = Article(file_path) 
            article.tags = ['python'] 
            article.categories = ['Python'] 
            # article.categories = ['Python'] 
            print(article.title) 
            # print(article.content) 
            ret = csdn_publisher(driver, article)
            if ret ==None:continue
            if ret == 1:
                shutil.move(file_path, done_path )  
        
        except Exception as err:
            print('xx ', err) 

    driver.quit() 
    pass 

# 简单发布一个文件
def test_simple_pub():
    file_path = '/Users/xx/Documents/xxx/tool.md' 
    article = Article(file_path) 
    article.tags = ['python'] 
    article.cover_img_path = '/Users/xx/Pictures/logo.png'
    article.categories = ['Python'] 
    # article.categories = ['Python'] 
    print('-- title : ', article.title) 
    # print(article.content) 
    ret = csdn_publisher(driver, article)
    # if ret ==None:continue

# 定时发布文件
def test_scheduled_pub():
    file_path = '/Users/xx/Documents/xxx/tool.md' 
    article = Article(file_path) 
    article.tags = ['python']  
    article.categories = ['Python'] 
    article.pub_date = '29'
    article.pub_time = '08:15'  
    print('-- title : ', article.title)  
    ret = csdn_publisher(driver, article)


import shutil
if __name__ == '__main__':
    
    # paths = sys.argv[1:]
    # print('-- ', paths) 
    # handle_paths(paths) 
    username = ''
    password = '' 
    login(username, password)
    # test_simple_pub()
    test_scheduled_pub() 

    driver.quit()  


