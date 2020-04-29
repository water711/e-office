# -*- coding : utf-8 -*-

import time
import config.ElePath as ElePath
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class OaTest(object):

    base_url = "http://192.168.1.2:38010"
    index_url = base_url + "/eoffice10/client/app/web/#/portal/view/1"
    flow_step = []

    def __init__(self, flow_id, user):
        self.flow_id = flow_id   # 流程ID
        self.user = user      # 轮流存放流程每个节点办理人
        self.flow_url = ''    # 创建流程后的流程URL链接
        self.flow_step = []   # 记录流程经过的节点
        self.flow_step.append(user)
        self.step = 1         # 记录流程经过的节点数量

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def login(self, user):
        self.driver.get(OaTest.base_url)

        # 输入用户名
        f_name = WebDriverWait(self.driver, 999).until(
            lambda driver: driver.find_element_by_xpath(ElePath.name_xpath))
        f_name.clear()
        f_name.send_keys(self.user)

        # 提交
        f_submit = self.driver.find_element_by_xpath(ElePath.submit_xpath)
        f_submit.click()

        # 等待打开首页
        WebDriverWait(self.driver, 999).until(
            lambda driver: driver.find_element_by_class_name('username'))

    def create_flow(self):
        '''
            创建流程，填写表单
        '''
        # 使用流程ID，拼接该流程url地址，从浏览器打开
        flow_url = OaTest.base_url + '/eoffice10/client/app/web/#/flow-handle/' + \
            str(self.flow_id) + '//'
        self.driver.get(flow_url)

        # 等待创建流程页面加载完成
        WebDriverWait(self.driver, 999).until(
            lambda driver: driver.find_element_by_class_name('eui-content'))

        # 获取必填表单控件
        control_list = self.get_control()

        # 填写表单内容
        self.write_content(control_list)

        # 提交表单并判断是否成功
        self.submit_flow()

        # 获取流程下一个审批人
        self.get_next_user()

        # 获取该流程URL地址
        self.get_flow_url()

    def get_control(self):
        '''
            从文件获取表单必填控件信息
        '''
        control_list = []
        file_name = 'control_id/' + str(self.flow_id) + '.txt'
        with open(file_name, 'r') as f:
            while 1:
                line = f.readline().strip('\n')
                if not line:
                    break
                s = line.split()
                control_list.append(s)
        return control_list

    def write_content(self, control_list):
        '''
            填写表单内容
        '''
        for c in control_list:
            if c[0] == 'text':
                ele = WebDriverWait(self.driver, 999).until(
                    lambda driver: driver.find_element_by_id(c[1]))
                ele.send_keys('123')
            if c[0] == 'choice':
                self.driver.find_element_by_id(c[1]).click()
                self.driver.find_element_by_xpath(c[2]).click()
                self.driver.find_element_by_xpath(ElePath.title_xpath).click()
            if c[0] == 'click':
                ele = WebDriverWait(self.driver, 999).until(
                    lambda driver: driver.find_element_by_id(c[1]))
                ele.click()

    def submit_flow(self):
        '''
            提交流程
        '''

        if self.step == 1:

            # 表单提交
            self.driver.execute_script(
                "document.getElementsByTagName('button')[1].click()")
            time.sleep(5)

            if ('没有满足出口条件的节点，请与系统管理员联系！' in self.driver.page_source):
                self.flow_step.append("失败")
                self.driver.quit()

            # 流程提交
            test = WebDriverWait(self.driver, 999).until(lambda driver: driver.find_element_by_xpath("//*[text()='提交']"))
            test.click()
            time.sleep(2)

        else:
            self.driver.find_element_by_xpath(
                ElePath.flow_submit_1_xpath).click()
            time.sleep(3)
            try:
                if ('没有满足出口条件的节点，请与系统管理员联系！' in driver.page_source):
                    print('没有满足出口条件的节点，请与系统管理员联系！')
                    flow_step.append("失败")
                    return
            except:
                pass

            # 上面点击提交后，如果还保持有两个窗口，则在当前弹出的窗口再次点击提交
            if len(self.driver.window_handles) == 2:
                self.driver.execute_script(
                    'document.querySelector("body > div.eui-modal.fade.in > div > div > div > ng-transclude > div.eui-modal-footer > ng-transclude > button.eui-btn.eui-btn-primary > span").click()')

    def get_next_user(self):

        # 返回首页
        self.driver.get(OaTest.index_url)

        # 点击已办流程标签
        already_flow = WebDriverWait(self.driver, 999).until(
            lambda driver: driver.find_element_by_link_text('已办流程'))
        time.sleep(2)
        already_flow.click()

        # 获取已办流程最新一项的下一步办理人
        ele = WebDriverWait(self.driver, 999).until(
            lambda driver: driver.find_element_by_xpath(ElePath.next_user_xpath))
        self.user = ele.text

        self.flow_step.append(self.user)

        self.step += 1

    def get_flow_url(self):
        '''
            获取提交后流程的url地址
        '''

        # 点击已办流程中最新一项
        ele = self.driver.find_element_by_xpath(ElePath.already_flow)
        ele.click()

        # 切换到第2个窗口
        self.driver.switch_to_window(self.driver.window_handles[1]) 

        # 获取当前浏览器窗口的url地址
        self.flow_url = self.driver.current_url  

        self.driver.close()

        # 切换回第1个窗口
        self.driver.switch_to_window(self.driver.window_handles[0])  

    def approval_flow(self, user):
        '''
            流程审批
        '''
        self.login(user)

        # 点击第一个待办流程
        todo_flow = WebDriverWait(self.driver, 999).until(
            lambda driver: driver.find_element_by_xpath(ElePath.todo_flow_xpath))
        todo_flow.click()
        time.sleep(1)

        # 切换到流程页面所在窗口
        self.driver.switch_to_window(self.driver.window_handles[1])

        # 审核同意
        agree = WebDriverWait(self.driver, 999).until(
            lambda driver: driver.find_element_by_css_selector('.eui-m-r-1:nth-child(1) > i'))
        agree.click()

        # 填写审批意见
        content = WebDriverWait(self.driver, 999).until(
            lambda driver: driver.find_element_by_xpath('//*[@id="mce_19"]'))
        content.click()
        content.send_keys('OK')

        self.submit_flow()

        # 切换窗口
        self.driver.switch_to_window(self.driver.window_handles[0])

        # 打开该流程页面，检测该流程是否已经结束
        self.driver.get(self.flow_url)
        WebDriverWait(self.driver, 999).until(
            lambda driver: driver.find_element_by_css_selector("[class='eui-pull-right number']"))
        
        # 如果流程未结束，则继续进入下一个节点审批
        if 'div class="flow-seal" ng-show' not in self.driver.page_source:
            self.get_next_user()
            self.approval_flow(self.user)

    def run(self):
        self.login(self.user)
        self.create_flow()
        self.approval_flow(self.user)
        print(self.flow_step)


# (流程ID, 流程发起人)
test = OaTest(70, '张三')  
test.run()
