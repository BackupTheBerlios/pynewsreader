#!/usr/bin/python
# -*- coding: utf-8  -*-

"""

"""

#
# Project page: developer.berlios.de/projects/pynewsreader
#
# (C) Leonardo Gregianin, 2006-2007
#
# Distributed under the terms of the GPL license.
# details see http://www.gnu.org/licenses/gpl.txt
# 
# TODO:
#  Imprimir lista de todos os grupos do servidor
#  Envio de novas mensagens ao grupo
#  Se o grupo for privado, se inscrever
#  Suporte a unicode para o conteúdo das mensagens
#  Adaptar configurações pessoais (config.py)
#  Perguntar o que quer fazer (read, post, list groups)
#
# Thanks:
#  effbot.org
#  pythonbrasil.com.br
#  

import nntplib, rfc822, socket, getpass
import string, StringIO, sys

class PostNews:
    pass

class ListGroups:
    pass

class ReadNews:
    pass

class News:

    def __init__(self, server, newsgroup, user=None, password=None, port='119'):
        self.server = server
        self.newsgroup = newsgroup
        self.user = user
        self.password = password
        self.port = port

    def run(self):
        try:
            servername = nntplib.NNTP(self.server)
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
                        text = string.join(text, '\n')
                        file = StringIO.StringIO(text)
                        message = rfc822.Message(file)

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
                        sys.exit()
                    else:
                        pass # Menu again
                except KeyboardInterrupt, ex:
                    print 'Quit... (%s)\n'%ex

        except socket.error, ex:
            print 'Error: (%s)'%ex

        except nntplib.NNTPTemporaryError, ex:
            print 'Error: (%s)'%ex

def main():
    try:
        # for arg in argv[1:]:
        server = sys.argv[1]
        newsgroup = sys.argv[2]
        user = sys.argv[3]
        # header = '-h'; header = True 
        password = getpass.getpass('Password: ')
        news = News(server, newsgroup, user, password, port='119')
        news.run()
        
    except IndexError:
        # usage newsreader.py [action] 
        print 'Usage: %s <server> <newsgroup> <user>' % argv[0]
        print 'Try: newsreader.py news.gmane.org gmane.comp.python.announce guest' # Public group
        raise SystemExit

if __name__ == '__main__':
    main()
