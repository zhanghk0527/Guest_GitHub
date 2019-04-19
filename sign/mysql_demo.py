#-*-coding:utf-8-*-

from pymysql import cursors, connect

# 链接数据库
conn = connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    db = 'guest',
    charset = 'utf8mb4',
    cursorclass = cursors.DictCursor
)

try:
    # 获取数据库游标
    with conn.connect() as cursors:
        # 创建嘉宾数据
        sql = 'insert into sign_guest (realname,phone,email,sign,event_id,create_time) values ("tom",18800110002,"tom@mail.com",0,1,NOW());'
        # 执行sql语句
        cursors.execute(sql)
        # 提交事务（提交数据库执行）
        conn.commit()

        # 获取数据游标
        with conn.cursor() as cursors:
            # 查询添加的嘉宾
            sql = "select realname,phone,email,sign from sign_guest where phone = %s"
            # 执行sql语句
            cursors.execute(sql, ('18800110002',))
            result = cursors.fetchone()
            print (result)

finally:
    # 关闭数据库连接
    conn.close()