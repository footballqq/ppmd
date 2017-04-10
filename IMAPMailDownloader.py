#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#@Filename : IMAPMailDownloader
#@Date : 2017-03-19-09-37
#@Poject: emaildownloader
#@AUTHOR : footballqq


import poplib
import imaplib
import email
import os
import sys
import configparser
import logging
import datetime
import time
import re

#https://pymotw.com/2/imaplib/
#https://gist.github.com/baali/2633554 baali@github
#https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/

def parse_list_response(line):
    list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
    flags, delimiter, mailbox_name = list_response_pattern.match(line.decode()).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

def get_emails(config):
    savepath = config.get('MailDownloader', 'savepath')
    user = config.get('MailDownloader', 'user')
    password = config.get('MailDownloader', 'password')
    mailserver = config.get('MailDownloader', 'mailserver')
    deletefromserver = int(config.get('MailDownloader', 'deletefromserver'))
#    waitingtime  = config.get('MailDownloader', 'waitingtime')
    logging.debug('downloading..............')

    try:
        logging.debug('fetch at {0:s}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        print('fetch at {0:s}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        connection = imaplib.IMAP4(mailserver)
        connection.login(user, password)
        typ, data = connection.list()
        logging.debug('Response code:{0:s}'.format(typ))
#        print('Response code:', typ)
#        for line in data:
#            print('Server response:', line)
#            flags, delimiter, mailbox_name = parse_list_response(line)
#            print('Parsed response:', (flags, delimiter, mailbox_name))
        connection.select('Inbox')
        #typ, data = connection.search(None, 'ALL')
        typ, data = connection.uid('search', None, 'ALL')
        if typ != 'OK':
            print('Error searching Inbox.')
            logging.debug('Error searching Inbox.')
            raise

        # Iterating over all emails
        for msgId in data[0].split():
            #typ, messageParts = connection.fetch(msgId, '(RFC822)')
            typ, messageParts = connection.uid('fetch', msgId, '(RFC822)')
            if typ != 'OK':
                print('Error fetching mail.')
                logging.debug('Error fetching mail.')
                raise

            emailBody = messageParts[0][1]
            mail = email.message_from_string(emailBody.decode())
            subjectwithcode = email.header.decode_header(mail['Subject'])
            code = subjectwithcode[0][1]
            if code != None :
                subject = subjectwithcode[0][0].decode(code)
            else :
                subject = subjectwithcode[0][0]
            #print("test3")
            print(subject)
            logging.debug(subject)

            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                    # print part.as_string()
                    continue
                if part.get('Content-Disposition') is None:
                    # print part.as_string()
                    continue
                filenamedecode = email.header.decode_header(part.get_filename())
                code = filenamedecode[0][1]
                if code != None :
                    fileName = filenamedecode[0][0].decode(code)
                else :
                    fileName = filenamedecode[0][0]
                # remove unprintable char or invalid char for filenames.
                fileName = re.sub('[^\w\s-]', '.', fileName).strip().lower()

                print(fileName)

                if bool(fileName):
                    filePath = os.path.join(savepath, fileName)
                    while  os.path.exists(filePath)==True:
                        filename_tmp, file_extension = os.path.splitext(filePath)
                        filePath = filename_tmp + '1' + file_extension
                    if not os.path.isfile(filePath) :
                        print(filePath)
                        logging.debug("saving file : {0:s} ".format(filePath))
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

            if deletefromserver == 1:
                connection.uid('store', msgId, '+FLAGS', '\\Deleted')
        connection.expunge()
        connection.close()
        connection.logout()

#empty trash?
        logging.debug('empty trash')
        connection = imaplib.IMAP4(mailserver)
        connection.login(user, password)
        connection.select('Trash')
        #typ, data = connection.search(None, 'ALL')
        typ, data = connection.uid('search', None, 'ALL')
        if typ != 'OK':
            print('Error searching Trash.')
            logging.debug('Error searching Trash.')
            raise

        # Iterating over all emails
        for msgId in data[0].split():
            if deletefromserver == 1:
                connection.uid('store', msgId, '+FLAGS', '\\Deleted')

        connection.expunge()
        connection.close()
        connection.logout()

    except TimeoutError as Argument:
        logging.debug(Argument)
    except Exception as e:
        logging.debug("Unexpected error: {0:s}".format(str(e)))
    else:
        logging.debug('finished at {0:s}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

def main():
#    global cfgfile
    config = configparser.ConfigParser()
    if len(sys.argv) == 2:
        cfgfile = sys.argv[1]
        cfgfile = "maildlcfg.ini"
        config.read(cfgfile)
    else:
        print("please use config file: python IMAPMailDownloader.py maildlcfg.ini")
        sys.exit(0)

    logfile = 'download.log'
    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    logging.debug('log start at {0:s}'.format(datetime.date.today().strftime("%Y%m%d")) )
    get_emails(config)




if __name__=='__main__':
    main()