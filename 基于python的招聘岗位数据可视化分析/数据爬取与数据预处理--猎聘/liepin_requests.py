from get_webdriver import get_driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import requests
import json
import time
import pandas as pd

# 创建 Chrome 的函数
driver = get_driver()
def get_job_json(name: str):
    url = f'https://we.51job.com/api/job/search-pc?api_key=51job&timestamp=1685976167&keyword={name}&searchType=2&function=&industry=&jobArea=000000&jobArea2=&landmark=&metro=&salary=&workYear=&degree=&companyType=&companySize=&jobType=&issueDate=&sortType=0&pageNum=1&requestId=&pageSize=10000&source=1&accountId=&pageCode=sou%7Csou%7Csoulb&u_atoken=455b534a-a28e-4d04-8530-d0d2f08b749d&u_asession=010_9k_MePnKelYNPfToltSDLSHrBb0Lt1GtOEry-lSG0G4fU69kCutl9QCVl8idjrX0KNBwm7Lovlpxjd_P_q4JsKWYrT3W_NKPr8w6oU7K_hfU3ZiDzGRohSWtbxGiJjby1SPx9aL3tr8MdW_TVLGGBkFo3NEHBv0PZUm6pbxQU&u_asig=05aXSDbnkUbpft9iJooN5CqqkhPMX7TevWJVtTOzB0PZdHY9quX2azSsN8DF3GxmzXxWkFXjELokTspbLlKwfy6lCidiN2xJEWmoC3I73mBLNUOpCCHG6eSlbhZM3q8Xl-7x3ftkyPvcL2Yt-emJYseSmLaZMAlKCiXR9DnVtLmrf9JS7q8ZD7Xtz2Ly-b0kmuyAKRFSVJkkdwVUnyHAIJzeJ8XmGHWzpAgjGoTTcg919TvxzJshkRsJFuiMpIJQqpas1gY9CSQJyBjThCr9w8Fe3h9VXwMyh6PgyDIVSG1W83x1plg7BVOqs14inQ1aIt3yLY6mZgdXquFtyGe0DheqW5M_wf7qL3xyguxHIqCTEQXllamN59rCdpCxoEtpqwmWspDxyAEEo4kbsryBKb9Q&u_aref=v8rOCY%2Bogk8t0YxWbyBuDVRCHIA%3D'


    driver.get(url)
    time.sleep(3)
    # 定位到滑块元素
    slider = driver.find_element(By.XPATH,
                                "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/span")  # 使用正确的XPath定位到滑块元素

    # 创建一个ActionChains对象
    actions = ActionChains(driver)

    # 模拟拖动滑块的操作
    actions.click_and_hold(slider).move_to_element(
        slider).move_by_offset(400, 0).release().perform()

    time.sleep(3)
    # 获取网页内容
    html = driver.find_element(
        By.XPATH, "/html/body/pre").get_attribute("innerHTML")
    html = json.loads(html)
    df = pd.DataFrame(html['resultbody']['job']['items'])
    df.to_csv(f'{name}.csv', index=False, encoding='utf_8_sig')

job_list = ['python', 'java', '前端', '后端']
for job_name in job_list:
    get_job_json(job_name)
# 关闭浏览器
driver.quit()