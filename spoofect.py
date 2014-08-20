import imaplib , email , os ,getpass , time 
import smtplib , sys 
from email.mime.text import MIMEText
'''
NOTE : If you are willing to run this on a server remove all the print lines 
'''
def send( user , pwd  , text ) : 	
	print "[*] starting .. "
		
	msg = MIMEText(text)
	msg["To"] = user 
	msg["From"] = user
	msg["Subject"] = "WARNING , Spoofing Detected" 
	try : 
		smtp = smtplib.SMTP("smtp.gmail.com" , 587) # change it to your smtp mail server
		print "[*] connecting .. " 
		smtp.ehlo()
		print "[*] Encrypting .. "
		smtp.starttls()
		smtp.ehlo()
		print "[*]loggin.."
		smtp.login(user, pwd)		
		print "[*] sending .. "
		smtp.sendmail(user ,to, msg.as_string())
		smtp.close() 
		print "[+] sent to "+str(to)
	except Exception as e  : 
		print "[-] "+str(e)
print "[+] started"
feeds = [] 
username = raw_input('Please Enter your email: ')
password = getpass.getpass('Please Enter your password: ')
mail = imaplib.IMAP4_SSL('imap.gmail.com') # change it to your smtp mail server
mail.login(username, str(password))
mail.list()
print "[+] logged in "
mail.select("inbox")
e = "nothing"
while 1 : 
	result, data = mail.uid('search', None, "ALL")
	#print "[+] getting the latest email " 
	latest_email_uid = data[0].split()[-1]
	result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
	raw_email = data[0][1]
	email_message = email.message_from_string(raw_email)
	parser = email.parser.HeaderParser()
	headers = parser.parsestr(email_message.as_string())
	reply = "empty" 
	for h in headers.items():
		    if h[0] == "From" : from_s = h[1]
		    if h[0].lower() == "subject" : a = h[1]
		    elif h[0] == "reply-to" :reply = h[1]
		    elif h[0] == "Received" : details = h[1]
	if from_s != reply and reply !="empty" :
		print "[-] not clean"
		feed = "email from "+str(email.utils.parseaddr(email_message['From'][1]))+"was not clean \n more details : "+str(details) 
		send(username , password , str(feed))
	elif  a != e : 
		 print str("[+] New clean email \n here are the details \n")
		 e = a
	#Uncomment the following lines to see the details of each incoming email 
	else  :  
		time.sleep(1)
		pass
	for h in headers.items():
		print str(h[0] + " : " + h[1]+"\n")


