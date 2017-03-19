# ppmd
python 3.5, windows test

python  pop3/IMAP mail downloader, download attachments from pop3/IMAP server and save all to a directory.

refs: used code of:
https://zh-cn.facebook.com/notes/eashwar-raghunathan/code-to-download-all-email-attachments-from-your-pop3-email-account/472554896150795/
https://gist.github.com/baali/2633554 baali@github

useful links:
https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
http://www.cnblogs.com/yhlx/archive/2013/03/22/2975817.html
https://pymotw.com/2/imaplib/

python收新邮件（解决了中文编码，可收附件和查看邮件信息）, 
Python Receive new mail and save attachment, solved Chinese code problem
http://blog.sina.com.cn/s/blog_4deeda2501016eyf.html

Python接收和转发邮件
http://www.logme.cn/blog/48/receive_and_forward_mail_using_python/

usage:
python Pop3MailDownloader.py configfile
will download by time interval in configfile

python IMAPMailDownloader.py configfile
download once

configfile: maildlcfg.ini

