# bilibili-OBS-automatic-streaming
一个能够自动开启Bilibili直播并唤起OBS推流的脚本。

⚠️ 本脚本会将您Bilibili账号的cookies以明文保存在本地，用于开播时的自动登录，除此之外脚本不会收集任何个人信息。**只要获得cookies，任何人从任意设备都可以在不输入账号密码的情况下登录您的账号，请您务必妥善保管，避免cookies文件外泄！**
## 使用说明
### 运行脚本前
在使用脚本前，以下内容需要您手动配置：

1. 安装[Chrome浏览器](https://www.google.cn/chrome/)和对应版本的[WebDriver](https://chromedriver.chromium.org)；
2. 从[Bilibili直播个人中心](https://link.bilibili.com/p/center/index#/my-room/start-live)获取第三方直播软件所需的RTMP密钥；
3. 在OBS中的推流设置中完成与直播相关的设置，并填写上述获得的RTMP密钥；
4. 如果您的OBS版本低于v27及以下，请手动安装[obs-websocket](https://obsproject.com/forum/resources/obs-websocket-remote-control-obs-studio-using-websockets.466/)（从v28起，obs-websocket已经内置在OBS中）；
5. 在OBS的“工具”-“obs-websocket设置”一栏中开启obs-websocket服务器（对于v27及以下，该选项位于“工具”-“WebSocket Server Settings(4.x Compat)”中）；

### 运行脚本
**首次运行：**
在首次运行脚本时，脚本会进入抓取cookies的流程。脚本会唤起一个受控的Chrome页面并自动进入Bilibili主页，请您在本页面中登录您直播所使用的账号。在登录完成后，请您在脚本页面按下回车键，脚本会自动抓取并保存您的cookies，并以一个名为“cookies.json”的文件保存在脚本的同一目录。之后脚本会自动退出，完成首次运行的操作。

**再次运行：**
在cookies.json文件存在的情况下，脚本会自动进入开播流程。脚本会自动唤起Chrome，利用cookies完成登录操作，完成开播的点按操作，并控制OBS开始推流。之后，脚本会自动进入OBS的监视页面，显示包括推流状态、输出分辨率和帧率、时间码、丢帧、上传流量等统计信息。在监测到推流中断后，脚本会重新尝试开启推流的操作，直到推流成功。

### 自动化
将本脚本和OBS加入开机启动项，即可在直播设备上电开机时自动开启。除此之外，您可能还需要在直播设备的BIOS中将上电设置调整为上电即开机。

## 脚本原理

脚本本质上分为两部分：

第一部分：通过selenium唤起webdriver，注入直播账号的cookies完成登录，并自动进入开播设置，完成分区的选择和开播按钮的点击；

第二部分：通过[obsws-python](https://github.com/aatikturk/obsws-python)获取OBS的相关信息，执行“开始推流”操作，并监控推流状态，在直播发生中断时自动执行重连。

## TODO
- [ ] 利用[bilibili-api](https://pypi.org/project/bilibili-api/)完成对Bilibili开播状态的监视，并自动在断连时进行重连
- [ ] 加入直播分区的自定义功能
- [ ] 为本地保存的cookies加入加密功能（遥遥无期）
