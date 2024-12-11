"""
database conection can be used application-wide
"""

import pymysql.cursors
# conn = pymysql.connect(host='localhost',
#                        port=8889,
#                        user='root',
#                        password='root',
#                        db='airline',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)


conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='',
                       db='airport',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
