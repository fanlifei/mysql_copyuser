#!/usr/bin/env python
#-*- coding:utf-8  -*-
from datetime import date, datetime, timedelta
import pymysql.cursors
import os, sys, argparse, datetime
import re



def parse_args(args):
        """parse args for copyuser"""
        parser = argparse.ArgumentParser(description='Parse Mysql Copy account you want',add_help=False)
        connect_setting = parser.add_argument_group('connect setting')
        connect_setting.add_argument('-h','--host',dest='host',type=str,help='Host the MySQL database server located',default='127.0.0.1')
        connect_setting.add_argument('-u','--user',dest='user',type=str,help='MySQL Username to log in as',default='root')
        connect_setting.add_argument('-p','--password',dest='password',type=str,help='MySQL Password to use', default='')
        connect_setting.add_argument('-P', '--port', dest='port', type=int,help='MySQL port to use', default=3306)
        copy_user = parser.add_argument_group('copy user')
        copy_user.add_argument('--src-user',dest='srcuser',type=str,help='copy from the user',nargs='*',default='*')
        copy_user.add_argument('--src-host',dest='srchost',type=str,help='copy from the host',nargs='*',default='*')
        copy_user.add_argument('--dest-user',dest='destuser',type=str,help='copy to the user',nargs='*',default='')
        copy_user.add_argument('--dest-host',dest='desthost',type=str,help='copy to the host',nargs='*',default='')

        parser.add_argument('--help', dest='help', action='store_true', help='help infomation', default=False)

        return parser
def command_line_args(args):
        needPrintHelp = False if args else True
        parser = parse_args(args)
        args = parser.parse_args(args)
        if args.help or needPrintHelp:
                parser.print_help()
                sys.exit(1)
        return args

def copyuser(args):
        conn=command_line_args(args)
        if conn.srcuser == '*':
                where_user=''
        else:
                if len(conn.srcuser) == 1:
                        users="".join(tuple(conn.srcuser))
                        where_user=' and user in ("{0}")'.format(users)
                else:
                        users=tuple(conn.srcuser)
                        where_user=' and user in {0}'.format(users)
        if conn.srchost == '*':
                where_host=''
        else:
                if len(conn.srchost) == 1:
                        hosts="".join(tuple(conn.srchost))
                        where_host='and host in ("{0}")'.format(hosts)
                else:
                        hosts=tuple(conn.srchost)
                        where_host='and host in {0}'.format(hosts)

        if not conn.destuser:
                 raise ValueError('The target user can not be empty')
        if not conn.desthost:
                raise ValueError('The target host can not be empty')
        connectionSettings = {'host':conn.host, 'port':conn.port, 'user':conn.user, 'passwd':conn.password}
        connection=pymysql.connect(**connectionSettings)
        get_privilege="select concat('show grants for ''',user,'''@''',host, ''';') a from mysql.user where 1=1 {0} {1};".format(where_user,where_host)
        try:
            with connection.cursor() as cursor:
                 cursor.execute(get_privilege)
                 results = cursor.fetchall()
                 for result in results:
                        dest_pri="".join(result)
                        cursor.execute(dest_pri)
                        results = cursor.fetchall()
                        for result in results:
                                result="".join(result)
                                for user in conn.srcuser:
                                        for host in conn.srchost:
                                                newuser="".join(tuple(conn.destuser))
                                                newhost="".join(tuple(conn.desthost))
                                                if user != '*' and host !='*':
                                                        print re.sub('\d.\d.\d.\d.\d',newhost,re.sub("TO\s.*@",newuser+'@',result))
                                                elif user != '*':
                                                        print re.sub("TO\s.*@",newuser+'@',result)
                                                else:
                                                        print re.sub('\d.\d.\d.\d.\d',newhost,result)

            connection.commit()

        finally:
                connection.close();
if __name__=='__main__':
        args=sys.argv[1:]
        copyuser(args)

