# 必要的依赖库
import re
import base64
import hashlib
import os
import sys
import shutil
import json
from pprint import pprint
from zfn_api import Client
from pushplus import send_message

# 从环境变量中提取教务系统的URL、用户名、密码和TOKEN等信息
force_push_message = os.environ.get("FORCE_PUSH_MESSAGE")
url = os.environ.get("URL")
cookies = (os.environ.get("COOKIES"))
token = os.environ.get("TOKEN")
github_event_name = os.environ.get("GITHUB_EVENT_NAME")
github_triggering_actor = os.environ.get("GITHUB_TRIGGERING_ACTOR")
repository_name = os.environ.get("REPOSITORY_NAME")
github_sha = os.environ.get("GITHUB_SHA")
github_workflow = os.environ.get("GITHUB_WORKFLOW")
github_run_number = os.environ.get("GITHUB_RUN_NUMBER")
github_run_id = os.environ.get("GITHUB_RUN_ID")
beijing_time = os.environ.get("BEIJING_TIME")
github_step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
main_yml_files_inconsistent = os.environ.get("MAIN_YML_FILES_INCONSISTENT")

# 将字符串转换为布尔值
# 是否强制推送信息
force_push_message = force_push_message == "True"
# 当前分支的main.yml文件与上游分支的main.yml文件是否不一致
main_yml_files_inconsistent = main_yml_files_inconsistent == "True"

# 定义文件路径

time_file_path = "time.txt"


# 初始化变量
base_url = url
raspisanie = []
ignore_type = []
detail_category_type = []
timeout = 5

# 创建教务系统客户端对象
student_client = Client(
    cookies=cookies,
    base_url=base_url,
    raspisanie=raspisanie,
    ignore_type=ignore_type,
    detail_category_type=detail_category_type,
    timeout=timeout,
)

# 如果time.txt文件不存在,则创建文件
if not os.path.exists(time_file_path):
    open(grade_file_path, "w").close()




# 读取time.txt文件的内容
with open(time_file_path, "r") as time_file:
    time_content = time_file.read()

if not time_content:
    # 首次运行
    first_run_text = (
    "检测到首次使用该程序\n"
    "如果你接下来收到目前教务系统的最新消息\n"
    "则代表你的程序运行成功\n"
    "从现在开始,程序将会每隔 30 分钟自动检测一次通知是否有更新\n"
    "若有更新,将通过微信推送及时通知你\n"
    "------"
    )
    # 推送信息
    first_run_text_response_text = send_message(
        token,
        "首次运行通知",
        first_time_text,
    )
    info = student_client.get_notifications()
    send_message('bd2b5248430d41d3b45d2ff49343e2e5','首次运行成功提醒',info['data'][0]['content'])
    with open(time_file_path, "w") as time_file:
        time_file.write(info['data'][0]['create_time'])
else:
    # 非首次运行
    info = student_client.get_notifications()
    # 判断是否有更新
    if time_content != info['data'][0]['create_time']:
        for i in range(len(info['data'])):
            if info['data'][i]['create_time'] != time_content:
                send_message('bd2b5248430d41d3b45d2ff49343e2e5','新消息提醒',info['data'][i]['content'])
            else:
                break
        with open(time_file_path, "w") as time_file:
            time_file.write(info['data'][0]['create_time'])
    
# 删除 __pycache__ 缓存目录及其内容
current_directory = os.getcwd()
cache_folder = os.path.join(current_directory, "__pycache__")
# 检查目录是否存在
if os.path.exists(cache_folder):
    # 删除目录及其内容
    shutil.rmtree(cache_folder)
