# ppmd
python  pop3 mail downloader, download attachments from pop3 server and save all to a directory.

refs:
https://zh-cn.facebook.com/notes/eashwar-raghunathan/code-to-download-all-email-attachments-from-your-pop3-email-account/472554896150795/

python�����ʼ�����������ı��룬���ո����Ͳ鿴�ʼ���Ϣ��, Python Receive new mail and save attachment, solved Chinese code problem
http://blog.sina.com.cn/s/blog_4deeda2501016eyf.html

Python���պ�ת���ʼ�
http://www.logme.cn/blog/48/receive_and_forward_mail_using_python/

usage:
python Pop3MailDownloader.py configfile

configfile:
#config sample

[MailDownloader]
mailserver = mail.xxx.com
user = foo@mail.xxx.com
password = foo123
savepath = d:\temp\download\

#1 will delete from server, 0 wont
deletefromserver = 0

#waiting time for each round
waitingtime = 5
