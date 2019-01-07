import json
import sqlite3
import random
import time
import requests
import string
from bs4 import BeautifulSoup
from headers_config import headers, USERAGENT_CONFIG

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

movies_id = []

def get_resp(url, trys):
	if random.randint(0, 5) == 1:
		refresh_cookies()

	try:
		if trys < 0:
			return
		resp = session.get(url)
		return resp

	except:
		return get_resp(session, url, trys - 1)

def set_checkpoint(movie_id):
	with open('checkpoint', 'w') as f:
		f.write(json.dumps({
		    "movie_id": movie_id
		}))
		f.close()

def get_checkpoint():
	try:
		with open('checkpoint', 'r') as f:
			content = f.read()
			if not content:
				return 0
			data = json.loads(content)
			if data:
				return data['movie_id']
			else:
				return 0
	except IOError as e:
		return 0

def get_movies_id():
	global movies_id
	try:
		with open('movies', 'r') as f:
			content = f.read()
			if not content:
				return 0
			movies = json.loads(content)
			if movies:
				for movie_id in list(movies.keys()):
					movies_id.append(movie_id)
			else:
				return 0
	except IOError as e:
		return 0

def get_comments_url(movie_id, start):
	url = "https://movie.douban.com/subject/" + str(movie_id) + "/comments?start=" + str(start) + "&limit=20&sort=new_score&status=P"
	return url

def get_comments(movie_id):
	for p in range(0, 11):
		time.sleep(0.5)
		start = p * 20
		url = get_comments_url(movie_id, start)
		data = get_resp(url, 3)

		if data is None:
			print("ip被封!")
			return

		soup = BeautifulSoup(data.text, 'html.parser')

		comments = soup.find_all("div", class_="comment-item")

		if not comments:
			set_comment_check_point(i+1, 0)
			break

		for comment in comments:
			rating = comment.find("span", class_="rating")
			if not rating:
				continue
			rating_class = rating['class']
			rating_num = 1
			if "allstar10" in rating_class or "allstar20" in rating_class:
				rating_num = 1
			if "allstar30" in rating_class:
				rating_num = 2
			if "allstar40" in rating_class or "allstar50" in rating_class:
				rating_num = 3

			comment_p = comment.find('p')
			comment_content = comment_p.get_text()
			save_comments(movie_id, comment_content, rating_num)

		set_checkpoint(movie_id)

def save_comments(movie_id, comment, rating):
	save_command = '''insert into comments_data
					(id, comment, rating)
					values
					(:id, :comment, :rating)'''

	cursor.execute(save_command,{'id':movie_id, 'comment':comment, 'rating':rating})
	conn.commit()

def get_new_cookie():
	data = session.get("https://accounts.douban.com/login")

	if data.status_code != 200:
		print("获取cookie失败: " + str(data.status_code))
	else:
		print("获取cookie成功")

	session.headers['Host'] = "movie.douban.com"

def refresh_cookies():
	session.headers.clear()
	session.cookies.clear()
	random_useragent = random.choice(USERAGENT_CONFIG)
	session.headers = {
		"User-Agent": random_useragent,
		"Host": "movie.douban.com",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate, sdch, br",
		"Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
		"Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
	}

def main():
	get_new_cookie()
	get_movies_id()
	checkpoint = get_checkpoint()

	if checkpoint == 0:
		last_pos = 0
	else:
		last_pos = movies_id.index(checkpoint)

	for i in range(last_pos,len(movies_id)):
		print("正在获取 %d 的评论...进度 %.2f %" % (movies_id[i], i*100/(len(movies_id)-1)))
		get_comments(movies_id[i])

	print('完成')

if __name__ == '__main__':
	with requests.Session() as session:
		main()
