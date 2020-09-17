import sqlite3
import numpy as np
import cv2
import bcrypt
import email_sender

def send_base64():
	with open("profile.txt") as f:
		return f.read()

def enter_to_db(email, password, age):
	try:
		conn = sqlite3.connect('usersdb.db')
		cur = conn.cursor()
		name_u = email.split('@')[0]
		cur.execute('''INSERT INTO User 
				(email, password, age, profile, name) 
				VALUES (?, ?, ?, ?, ?)''', 
				(email, password, age, send_base64(),name_u))
		conn.commit()
		conn.close()
		msg = '''
		Hey Buddy..
		Thanks For registering...
		From now you are die hard fan of Pranava Adiga..
		you can post now in our website.
		Try it now.'''
		email_sender.send_mail(email, msg, subject="Successfully Registered")
		return (True, "Registered Successfully")
	except:
		return (False, "Can't Registered due to some internal issue")


def create_db():
	conn = sqlite3.connect('usersdb.db')
	cur = conn.cursor()
	cur.execute('''	CREATE TABLE IF NOT EXISTS User (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
									    email varchar(255) NOT NULL,
									    password varchar(255),
									    name varchar(255),
									    profile varchar(100000),
									    age int)''')
	cur.execute('''	CREATE TABLE IF NOT EXISTS Posts (
										Post_ID INTEGER PRIMARY KEY AUTOINCREMENT,
										User_ID INTEGER NOT NULL,
										post varchar(100000),
										likes int)''')
	conn.commit()
	conn.close()
 	

def check_from_db(email, password, age):
	conn = sqlite3.connect('usersdb.db')
	cur = conn.cursor()
	cur.execute('SELECT email FROM User WHERE email = ? ', (email,))
	row = cur.fetchone()
	conn.commit()
	conn.close()
	if row is None:
		try:
			response = email_sender.send_key(email)
			if response[0]:
				return(True, "enter the code", False, response[1])
			else:
				return(False, "Invalid email-id", False)
		except:
			return(False, "We are facing some issue, Please try later", False)
	else:
		return (False,"email already registered!!", True)
	
def check_if_exist(email, password):
	conn = sqlite3.connect('usersdb.db')
	cur = conn.cursor()
	cur.execute('''SELECT email 
					FROM User 
					WHERE email = ? ''', (email,))
	row = cur.fetchone()
	if row is None:
		conn.commit()
		conn.close()
		return(False,"This mail is not registered")
	else:
		cur.execute('SELECT password FROM User WHERE email = ? ', (email,))
		password_r = cur.fetchone()[0]
		conn.commit()
		conn.close()
		if bcrypt.checkpw(password.encode(), password_r):
			return (True, "You were successfully logged in")
		else:
			return (False, "Please check the email/password")

def give_details(email):
	conn = sqlite3.connect('usersdb.db')
	cur = conn.cursor()
	cur.execute('SELECT name, profile FROM User WHERE email = ? ', (email,))
	get = cur.fetchone()
	conn.commit()
	conn.close()
	pic = get[1]
	name_u = get[0]
	#make dictionary of name, email, pic;
	dic = {
	"email" : email,
	"name"  : name_u,
	"pic" : pic
	}
	return dic

def update_profile(name, email, dp = send_base64()):
	try:
		conn = sqlite3.connect('usersdb.db')
		cur = conn.cursor()
		cur.execute('''UPDATE User 
					SET name = ? , profile = ?
					WHERE email = ?''',(name, dp ,email)) 
		conn.commit()
		conn.close()
		return True
	except:
		return False

def add_post(email, post):
	try:
		conn = sqlite3.connect('usersdb.db')
		cur = conn.cursor()
		cur.execute('SELECT ID FROM User WHERE email = ? ', (email,))
		User_ID = int(cur.fetchone()[0])
		cur.execute('''INSERT INTO Posts 
					(User_ID, post, likes) 
					VALUES (?, ?, ?)''', 
					(User_ID, post, 0))
		conn.commit()
		conn.close()
		return True
	except:
		return False

def get_post(p_id, latest = True):
	if latest:
		conn = sqlite3.connect('usersdb.db')
		cur = conn.cursor()
		cur.execute('''SELECT COUNT(Post_ID)
								FROM Posts;''')
		no_posts = cur.fetchone()
		no_posts = no_posts[0]
		#print("posts:",no_posts)
		conn.commit()
		if no_posts != 0:
			p_id = p_id%no_posts
			new_id = (no_posts-p_id)
		else:
			return None
		
		cur.execute('SELECT User_ID, post, likes FROM Posts WHERE Post_ID = ? ', (new_id,))
		get = cur.fetchone()
		conn.commit()

		cur.execute('SELECT name, profile FROM User WHERE ID = ? ', (get[0],))
		get_2 = cur.fetchone()
		conn.commit()
		conn.close()
		name = get_2[0]
		dp = get_2[1]
		post = get[1]
		likes = get[2]
		#make dictionary of name, email, pic;
		dic = {
		"post_id" : new_id,
		"name": name,
		"dp": dp,
		"post"  : post,
		"likes" : likes
		}
		return dic

if __name__ == '__main__':
	conn = sqlite3.connect('usersdb.db')
	cur = conn.cursor()
	cur.execute('SELECT ID, email, name FROM User ')
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	print("users", len(rows))
	for row in rows:
		print("\t",row[0],row[1], row[2])
	print(len(send_base64()))
	#print(give_details("pranavaadiga.is19@bmsce.ac.in"))
	#update_profile("pranavaadiga.is19",'pranavaadiga.is19@bmsce.ac.in')
	print(get_post(14))
