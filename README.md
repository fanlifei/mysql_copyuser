# mysql_copyuser

 生产环境经常有增加服务器的需求，增加服务器需要添加权限，次脚本为了快速实现用户权限复制

## 1、所需模块
  pymysql、argparse
## 2、用法
  1、帮助文档
 ``` python mysql_copyuser.py --help
  usage: copyuser.py [-h HOST] [-u USER] [-p PASSWORD] [-P PORT]
                   [--src-user [SRCUSER [SRCUSER ...]]]
                   [--src-host [SRCHOST [SRCHOST ...]]]
                   [--dest-user [DESTUSER [DESTUSER ...]]]
                   [--dest-host [DESTHOST [DESTHOST ...]]] [--help]

Parse Mysql Copy account you want

optional arguments:
  --help                help infomation

connect setting:
  -h HOST, --host HOST  Host the MySQL database server located
  -u USER, --user USER  MySQL Username to log in as
  -p PASSWORD, --password PASSWORD
                        MySQL Password to use
  -P PORT, --port PORT  MySQL port to use

copy user:
  --src-user [SRCUSER [SRCUSER ...]]
                        copy from the user
  --src-host [SRCHOST [SRCHOST ...]]
                        copy from the host
  --dest-user [DESTUSER [DESTUSER ...]]
                        copy to the user
  --dest-host [DESTHOST [DESTHOST ...]]
                        copy to the host
     ```                   
                        
  2、--dest-user、--dest-host 为必填项
