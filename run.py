from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
import sys, os
import obsws_python 
import yaml

class startBilibili:
    def __init__(self):
        print("----------正在开启Bilibili直播----------")
        try:
            # 加载cookie
            with open('cookies.json', 'r') as f:
                print("发现存在的cookies文件，进入自动开播进程：")
                self.cookies = json.loads(f.read())
        except:
            print("未能找到包含cookies的json文件，请您按照接下来的指引生成。")
            self.get_cookies()
        # 加载设置
        try:
            with open('settings.yaml', 'r') as f:
                print("加载Bilibili直播设置：")
                settings = yaml.load(f.read(), Loader=yaml.FullLoader)['liveroom_settings']
                print(settings)
                self.category = settings['category']
                self.sub_category = settings['sub_category']
                self.liveroom_id = settings['liveroom_id']
        except:
            print("加载配置文件失败，请检查文件格式和内容是否正确。")
            sys.exit()
        self.start_streaming()



    def get_cookies(self):
        input("1、接下来，脚本会为您创建一个新的浏览器页面，请在页面中登录直播所用的账号（按下回车键继续）：")
        driver = webdriver.Chrome()
        driver.get("https://www.bilibili.com")
        input("2、接下来，脚本会抓取您的cookie并以json文件的形式保存在本地，请您妥善保管，避免泄露导致被盗号等损失（按下回车键继续）：")
        cookies = driver.get_cookies()
        print('cookies:', cookies)
        with open('cookies.json', 'w') as f:
            f.write(json.dumps(cookies))
        driver.close()
        print("已为您抓取cookies，以cookies.json文件保存在脚本的同一级目录，请您重新运行脚本以继续自动化操作。")
        sys.exit()

    def start_streaming(self):
        # 启动webdriver
        print("即将呼出浏览器，请您不要进行任何键鼠操作。")
        time.sleep(2)
        driver = webdriver.Chrome()
        driver.set_window_size(1280, 720)
        driver.get('https://www.bilibili.com')

        # 注入cookie
        driver.delete_all_cookies()
        for cookie in self.cookies:  
            driver.add_cookie(cookie_dict=cookie)
        print("注入cookies完成。")
        driver.get('https://link.bilibili.com/p/center/index#/my-room/start-live')
        # 开播
        action = ActionChains(driver)
        # 打开直播分类
        print("呼出开播分类……")
        live_area_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="live-center-app"]/div/main/div/div[1]/div[2]/div/div[1]/section/div[1]/div[1]/div[1]/a''')))
        action.move_to_element(live_area_btn).click().perform()
        print("完成。")
        time.sleep(1)
        # 点击单机游戏
        print(f"选择{self.category}……")
        category_list = ['网游', '手游', '单机游戏', '娱乐', '电台', '虚拟主播', '生活', '知识', '赛事']
        for i in range(len(category_list)):
            if category_list[i] == self.category:
                local_games_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'''//*[@id="live-center-app"]/div/main/div/div[1]/div[2]/div/div[1]/section/div[1]/div[1]/div[2]/div[2]/div/ul/li[{i+1}]''')))
                break
            if i == len(category_list) - 1:
                print("无法找到对应的直播间分类，请检查配置文件是否填写正确！")
                sys.exit()
        action.move_to_element(local_games_btn).click().perform()
        print("完成。")
        time.sleep(1)
        # 搜索框内搜索其他单机
        print(f"选择“{self.sub_category}”……")
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="live-center-app"]/div/main/div/div[1]/div[2]/div/div[1]/section/div[1]/div[1]/div[2]/div[2]/div/input''')))
        action.send_keys_to_element(search_input, self.sub_category).perform()
        time.sleep(1)
        other_local_games_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="live-center-app"]/div/main/div/div[1]/div[2]/div/div[1]/section/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div/div/a''')))
        action.move_to_element(other_local_games_btn).click().perform()
        print("完成。")
        time.sleep(1)
        # 点击确定
        print("提交中……")
        live_area_submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '''/html/body/div[1]/div/main/div/div[1]/div[2]/div/div[1]/section/div[1]/div[1]/div[2]/div[2]/div/div/div[3]/button[1]''')))
        action.move_to_element(live_area_submit_btn).click().perform()
        print("完成。")
        time.sleep(1)
        # 点击开播
        print("点击开播……")
        live_straming_start_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="live-center-app"]/div/main/div/div[1]/div[2]/div/div[1]/section/div[1]/div[8]/button''')))
        action.move_to_element(live_straming_start_btn).click().perform()
        print("完成。")
        print("正在关闭浏览器……")
        time.sleep(2)
        driver.close()
        print("完成。")


class startOBS:
    def __init__(self):
        print("----------正在开启OBS串流----------")
        time.sleep(1)
        try:
            with open('settings.yaml', 'r') as f:
                print("开始启动OBS串流：")
                settings = yaml.load(f.read(), Loader=yaml.FullLoader)['obs_websocket']
            self.host = settings['host']
            self.port = settings['port']
            self.password = settings['password']
        except:
            print("未能找到包含obs-websocket配置的文件或文件内容错误，请重新检查。")
            sys.exit()
        self.startStreaming()

    def startStreaming(self):
        if self.host == '':
            self.host = 'localhost'
        if self.port == '':
            self.port = '4455'
        print(f"主机地址：{self.host}\n端口：{self.port}\n密码：{self.password}")
        while True:
            try:
                obs = obsws_python.ReqClient(host=self.host, port=self.port, password=self.password)
                print("与OBS主机连接成功！")
                break
            except:
                print('无法与OBS主机建立连接，5秒钟后重试。\n若长时间仍无法连接，请检测obs端websocket是否开启，以及地址、端口、密码是否正确。')
                time.sleep(5)
        version = obs.get_version()
        print(f"OBS版本：{version.obs_version}；OBS-websocket版本：{version.obs_web_socket_version}；运行平台：{version.platform_description}")
        video_settings = obs.get_video_settings()
        print(f"当前画布分辨率：{video_settings.base_width}x{video_settings.base_height}")
        print(f"当前输出分辨率：{video_settings.output_width}x{video_settings.output_height}")
        print(f"当前输出帧率：{video_settings.fps_numerator/video_settings.fps_denominator}")
        stream_settings = obs.get_stream_service_settings().stream_service_settings
        print(f"当前串流服务：{stream_settings['service']}\n当前串流服务器：{stream_settings['server']}\n当前串流密钥：{stream_settings['key']}")
        print("正在开启串流……")
        # 开启直播
        def start_stream():
            while True:
                obs.start_stream()
                time.sleep(3)
                status = obs.get_stream_status().output_active
                if status == True:
                    print("OBS串流已开启！")
                    stream_monitor()
                else:
                    print(f"OBS串流开启失败，正在重试……")
                    time.sleep(3)
        # 直播监视
        def stream_monitor():
            platform = sys.platform
            if platform == 'darwin' or platform == 'linux':
                clear_cmd = 'clear'
            elif platform == 'cygwin' or platform == 'win32':
                clear_cmd = 'cls'
            while True:
                os.system(clear_cmd)
                stream_status = obs.get_stream_status()
                print("-----Bilibili直播-OBS自动开播脚本-----")
                print("---------由Mallow&Mana用爱开发--------\n")
                print(f"输出状态：{stream_status.output_active}")
                print(f"重连状态：{stream_status.output_reconnecting}")
                print(f"当前输出分辨率：{video_settings.output_width}x{video_settings.output_height}")
                print(f"当前输出帧率：{video_settings.fps_numerator/video_settings.fps_denominator}")
                print(f"时间码（持续时间）：{stream_status.output_timecode}")
                print(f"丢帧：{stream_status.output_skipped_frames}")            
                print(f"本次上传流量：{round(stream_status.output_bytes/1024/1024, 2)}MB")
                print("\n-----基本信息-----")
                print(f"OBS版本：{version.obs_version}\nOBS-websocket版本：{version.obs_web_socket_version}\n运行平台：{version.platform_description}")
                print(f"当前串流平台：{stream_settings['service']}")
                if stream_status.output_active == False:
                    print("直播发生中断，5秒钟后尝试重新连接……")
                    time.sleep(5)
                    break
                time.sleep(3)
        start_stream()


if __name__ == '__main__':
    print("-----Bilibili直播-OBS自动开播脚本-----")
    print("---------由Mallow&Mana用爱开发--------\n")
    startBilibili()
    startOBS()