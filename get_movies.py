import json
import time
import requests
from headers_config import headers

def get_movies():
    total_page = 10 #想要获取的电影页数，一页20部电影，每部电影200条评论
    index = 0
    limit = 20
    data = {}
    for i in range(index, total_page):
        print("index: %d" % int(index))
        page_start = int(index) * 20
        json_url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=" + str(limit) + "&page_start=" + str(page_start)

        res = session.get(json_url, headers=headers)
        res_json = json.loads(res.text)
        subjects = res_json['subjects']

        for m in subjects:
            data[m["id"]] = {}
            data[m["id"]]["title"] = m["title"]
            data[m["id"]]["url"] = m["url"]

        time.sleep(1)
        index += 1

    f = open('movies', 'a')
    try:
        f.write(json.dumps(data))
    except IndexError as e:
        pass
    except ValueError as e:
        pass
    finally:
        f.close()

if __name__ == '__main__':
    with requests.Session() as session:
        get_movies()