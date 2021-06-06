import requests
import json
import sys
import os

url: str = "https://dasai.lanqiao.cn/api/action/http/get"
local_data_path = sys.path[0] + "/news.txt"


class PostData:
    def __init__(self, page: int = 1, news_count_per_page: int = 10):
        self.page_id = 20
        self.page = page
        self.news_count_per_page = news_count_per_page

    def __str__(self):
        return f"http://10.251.196.135/API.php?m=list&id={self.page_id}&p={self.page}&s={self.news_count_per_page}"


def update():
    data = requests.post(url, data={
        "url": str(PostData())
    }).json()
    data = json.loads(data)
    with open(local_data_path, "w") as f:
        f.write(data["new_list"][0]["id"])


def diff():
    if not os.path.exists(local_data_path):
        print("不存在老版本的新闻文件，请用-u或者--update更新")
        return
    data = requests.post(url, data={
        "url": str(PostData())
    }).json()
    data = json.loads(data)

    with open(local_data_path, "r") as f:
        old_id = int(f.read().strip())

    new_id = int(data["new_list"][0]["id"])
    if new_id > old_id:
        print(f'一共有{new_id - old_id}条新信息：')
        curr_id = new_id
        i = 0
        while curr_id > old_id:
            print(f'{i + 1}. title: {data["new_list"][i]["title"]} \n  content: {data["new_list"][i]["content"]}\n')
            i += 1
            curr_id -= 1
    else:
        print("无新信息")


def top(num: int):
    data = requests.post(url, data={
        "url": str(PostData())
    }).json()
    data = json.loads(data)
    for i in range(0, num):
        print(f'{i + 1}. title: {data["new_list"][i]["title"]} \n  content: {data["new_list"][i]["content"]}\n')


if __name__ == '__main__':
    # -u --update: 更新当前新闻信息，便于比较
    # -t --top num: 展示前num条信息
    # 无参：获取最新信息，并比较输出
    if len(sys.argv) > 1 and (sys.argv[1] == "-u" or sys.argv[1] == '--update'):
        update()
    elif len(sys.argv) > 2 and (sys.argv[1] == '-t' or sys.argv[1] == '--top'):
        top(int(sys.argv[2].strip()))
    elif len(sys.argv) == 1:
        diff()
    else:
        pass
