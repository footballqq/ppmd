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
import re
# def get_config():
#     pass

def get_emails(config):
    savepath = config.get('MailDownloader', 'savepath')
    user = config.get('MailDownloader', 'user')
    password = config.get('MailDownloader', 'password')
    mailserver = config.get('MailDownloader', 'mailserver')
    deletefromserver = int(config.get('MailDownloader', 'deletefromserver'))
    waitingtime  = config.get('MailDownloader', 'waitingtime')
    logging.debug('downloading..............')

    while 1:
        try:
            logging.debug('fetch at {0:s}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            print('fetch at {0:s}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            p = poplib.POP3(mailserver)
            print(p.getwelcome())
            p.user(user)
            p.pass_(password)
            print("This mailbox has %d messages, totaling %d bytes." % p.stat())
            logging.debug("This mailbox has %d messages, totaling %d bytes." % p.stat())
            msg_list = p.list()
#            print(msg_list)
            if not msg_list[0].decode("utf-8").startswith('+OK'):
                    print("error !!!!")
                    logging.debug("error download mail list.")
                    exit(1)

            for msg in msg_list[1]:
                    msg_num, _ = msg.split()
                    logging.debug("processing No.{} / {} msg".format(msg_num, len(msg_list[1])))
                    print("processing No.{} / {} msg".format(int(msg_num.decode("utf-8")), len(msg_list[1])))
                    resp = p.retr(int(msg_num.decode("utf-8")))
                    if resp[0].decode("utf-8").startswith('+OK'):
                        #print resp, '=======================\n'
                        #print(resp[1])
                        respstr =   [ x.decode('utf-8') for x in resp[1]]
                        #print("test1")
                        parsed_msg = email.message_from_string('\n'.join(respstr))
                        #print("test2")
                        subjectwithcode = email.header.decode_header(parsed_msg['Subject'])
                        code = subjectwithcode[0][1]
                        #print(code)
                        if code != None :
                            #if code == 'gb2312' :
                            #    code = 'gbk'
                            subject = subjectwithcode[0][0].decode(code, errors = 'ignore')
                        else :
                            subject = subjectwithcode[0][0]
                        #print("test3")
                        #subject = subject.encode('gbk',errors = 'ignore')
                        #print(subject)
                        logging.debug(subject)
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
                            filename = re.sub('[^\w\s-]', '.', filename).strip().lower()
                            filename = filename.replace('\n','')
                            filename = filename.replace('\r','')
                            filename = filename.replace('\t','')
                            print(filename)
                            #filename = filename.encode('gbk', errors = 'ignore')
                            filename = os.path.join(savepath, filename)
                            while  os.path.exists(filename)==True:
                                filename_tmp, file_extension = os.path.splitext(filename)
                                filename = filename_tmp + '1' + file_extension
                            logging.debug("saving file : {0:s} ".format(filename))
                            fp = open(filename, 'wb')
                            fp.write(part.get_payload(decode=1))
                            fp.close()
                        payload= parsed_msg.get_payload(decode=True)
    #                    print(payload)
                    if deletefromserver == 1:
                        p.dele(int(msg_num.decode("utf-8")))
            print("quit")
            p.quit()
        except TimeoutError as Argument:
            logging.debug(Argument)
        except Exception as e:
            #pass
            if sys.exc_info()[0] is None:
                logging.debug("Unexpected error: value none") # {0:s}".format(sys.exc_info()[0]))
            else:
                pass # logging.debug("Unexpected error:  {0:s}".format(sys.exc_info()[0]))
            #logging.error(traceback.format_exc())
            logging.exception('Got exception on main handler')
            logging.error(e.__doc__)
            logging.error(e.message)
        else:
            logging.debug('finished at {0:s}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        print("sleep")
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
    logging.basicConfig(filename=logfile, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    #logging.Formatter(fmt='%(asctime)s.%(msecs)03d',datefmt='%Y-%m-%d,%H:%M:%S')
    logging.debug('log start at {0:s}'.format(datetime.date.today().strftime("%Y%m%d")) )
    get_emails(config)



if __name__=='__main__':
    main()