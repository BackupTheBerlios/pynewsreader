#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nntplib import NNTP, NNTPTemporaryError
from rfc822 import Message
from string import join
from StringIO import StringIO
from sys import exit, argv
from getpass import getpass
from socket import error

class NewsReader:

    def __init__(self, server, newsgroup, user=None, password=None, port='119'):
        self.server = server
        self.newsgroup = newsgroup
        self.user = user
        self.password = password
        self.port = port

    def run(self):
        try:
            servername = NNTP(self.server)
            resp, count, first, last, name = servername.group(self.newsgroup)
            print 'Group', name, 'has', count, 'articles, range', first, 'to', last
            print 'Please wait...\n'
            resp, subs = servername.xhdr('subject', first + '-' + last)

            for index in xrange(0,int(count)):
                print '\n'+'*'*60+'\n'+'MAIN MENU (LAST 12 MESSAGES)\n'+'*'*60
                for id, sub in subs[-12:]:
                    print id, sub
                print '*'*60
                id = raw_input('\nMessage ID to read (or "q" to quit): ')
                try:
                    if (id >= first) and (id <= last):
                        resp, id, message_id, text = servername.article(str(id))
                        text = join(text, '\n')
                        file = StringIO(text)
                        message = Message(file)

                        # Print all header
                        # for k, v in message.items(): print k, '=', v

                        # Print condensed header
                        headers = ['subject', 'from', 'date']
                        print '\n'
                        for k in headers:
                            print k, '=', message[k]
                        print '-'*60

                        print '\n'+message.fp.read()

                    elif (id in ['q', 'quit', 'Q', 'QUIT']):
                        print 'Quit...\n'
                        exit()
                    else:
                        pass # Menu again
                except KeyboardInterrupt, ex:
                    print 'Quit... (%s)\n'%ex

        except error, ex:
            print 'Error: (%s)'%ex

        except NNTPTemporaryError, ex:
            print 'Error: (%s)'%ex


def main():
    try:
        server = argv[1]
        newsgroup = argv[2]
        user = argv[3]
        password = getpass('Password: ')
        news = NewsReader(server, newsgroup, user, password, port='119')
        news.run()
        
    except IndexError:
        print 'Usage: %s <server> <newsgroup> <user>' % argv[0]
        print 'Try: pynewsreader.py news.gmane.org gmane.comp.python.announce guest' # Public group
        raise SystemExit

if __name__ == '__main__':
    main()
