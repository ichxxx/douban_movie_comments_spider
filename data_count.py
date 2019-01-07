import sqlite3

def count(content, extra_order):
	data = cursor.execute('select count(' + content + ') from comments_data ' + extra_order)
	return data.fetchall()[0]

def select_by_rating(rating):
	data = cursor.execute('select comment from comments_data where rating=' + str(rating))
	return data.fetchall()

def count_long_comments(comments):
	counter = 0
	for each in comments:
		comment = each[0].replace('\n', '')
		if len(comment) > 50:
			counter+=1
	return counter

if __name__ == '__main__':
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()

	total_comments = count('*', '')
	total_movies = count('distinct id', '')
	rating_1_comments = count('*', 'where rating=1')[0]
	rating_2_comments = count('*', 'where rating=2')[0]
	rating_3_comments = count('*', 'where rating=3')[0]

	long_comments_in_1 = count_long_comments(select_by_rating(1))
	long_comments_in_2 = count_long_comments(select_by_rating(2))
	long_comments_in_3 = count_long_comments(select_by_rating(3))

	print('来自 %d 部电影' % total_movies)
	print('共有 %d 个评论\n' % total_comments)

	print('1星评论有 %d 个，其中有 %d 个短评论，有 %d 个长评论' % (rating_1_comments,int(rating_1_comments)-long_comments_in_1,long_comments_in_1))
	print('2星评论有 %d 个，其中有 %d 个短评论，有 %d 个长评论' % (rating_2_comments,int(rating_2_comments)-long_comments_in_2,long_comments_in_2))
	print('3星评论有 %d 个，其中有 %d 个短评论，有 %d 个长评论' % (rating_3_comments,int(rating_3_comments)-long_comments_in_3,long_comments_in_3))