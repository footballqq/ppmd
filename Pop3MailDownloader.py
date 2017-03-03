#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#@Filename : Pop3MailDownloader
#@Date : 2017-03-03-09-37
#@Poject: emaildownloader
#@AUTHOR : footballqq

import poplib
import email
import os
import sys
import configparser
import logging
import datetime
import time

# def get_config():
#     pass

def get_emails(config):
    savepath = config.get('MailDownloader', 'savepath')
    user = config.get('MailDownloader', 'user')
    password = config.get('MailDownloader', 'password')
    mailserver = config.get('MailDownloader', 'mailserver')
    deletefromserver = config.get('MailDownloader', 'deletefromserver')
    waitingtime  = config.get('MailDownloader', 'waitingtime')
    logging.debug('downloading..............')

    while 1:
        logging.debug('fetch at {0:s}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        p = poplib.POP3(mailserver)
#        print(p.getwelcome())
        p.user(user)
        p.pass_(password)
#        print("This mailbox has %d messages, totaling %d bytes." % p.stat())
        msg_list = p.list()
#       print(msg_list)
        if not msg_list[0].decode("utf-8").startswith('+OK'):
                print("error !!!!")
                logging.debug("error download mail list.")
                exit(1)

        for msg in msg_list[1]:
                msg_num, _ = msg.split()
                resp = p.retr(int(msg_num.decode("utf-8")))
                if resp[0].decode("utf-8").startswith('+OK'):
                    #print resp, '=======================\n'
                    respstr =   [ x.decode('utf-8') for x in resp[1]]
                    parsed_msg = email.message_from_string('\n'.join(respstr))
                    for part in parsed_msg.walk():
#                        print((part.get_content_type()))
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
#                           print("no content dispo")
                            continue
                        filenamedecode = email.header.decode_header(part.get_filename())
                        code = filenamedecode[0][1]
                        if code != None :
                            filename = filenamedecode[0][0].decode(code)
                        else :
                            filename = filenamedecode[0][0]
#                        print(filename)
                        while  os.path.exists(filename)==True:
                            filename_tmp, file_extension = os.path.splitext(filename)
                            filename = filename_tmp + '1' + file_extension
                        logging.debug("saving file : {0:s} ".format(filename))
                        fp = open(os.path.join(savepath, filename), 'wb')
                        fp.write(part.get_payload(decode=1))
                        fp.close
                    payload= parsed_msg.get_payload(decode=True)
#                    print(payload)
                if deletefromserver == 1:
                    p.dele(int(msg_num.decode("utf-8")))
        time.sleep(int(waitingtime))
    pass

def main():
#    global cfgfile
    config = configparser.ConfigParser()
    if len(sys.argv) == 2:
        cfgfile = sys.argv[1]
        config.read(cfgfile)
    else:
        print("please use config file: python Pop3MailDownloader.py maildlcfg.ini")
        sys.exit(0)
    logfile = 'download.log'
    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    logging.debug('log start at {0:s}'.format(datetime.date.today().strftime("%Y%m%d")) )
    get_emails(config)



if __name__=='__main__':
    main()