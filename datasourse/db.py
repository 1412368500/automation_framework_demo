# coding=utf-8
import configparser
import os

from framework.logger import Logger

from DBUtils.PooledDB import PooledDB
import pymysql
logger = Logger(logger="CommonDB").getlog()

class CommonDB(object):
    POOL = None

    def __init__(self):
        config = configparser.ConfigParser()
        file_path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
        config.read(file_path)
        host = config.get("db_ami", "host")
        port = config.get("db_ami", "port")
        db_name = config.get("db_ami", "dbname")
        user = config.get("db_ami", "user")
        password = config.get("db_ami", "password")
        charset = config.get("db_ami", "charset")
        CommonDB.POOL = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=20,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=1,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。
            # PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，
            # _maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=4,
            # ping MySQL服务端，检查是否服务可用。
            # 如：0 = None = never, 1 = default = whenever it is requested,
            # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=db_name,
            charset=charset
        )

    # 执行语句，有数据则返回所有数据,返回的是一个二维元组
    # 理论上可以删除，新增，查询都
    def exec_query(self, str_sql):
        conn = CommonDB.POOL.connection()
        cur = conn.cursor()  # 获取一个游标
        try:
            cur.execute(str_sql)  # 执行一条数据库查询语句
            data = cur.fetchall()  # 将执行结果返回给data，data为一个二维数组
            logger.info("执行sql【%s】，查询到数据总量为：【%d】" % (str_sql, cur.rowcount))
            conn.commit()
            return data
        finally:
            cur.close()
            conn.close()

    def exec_delete(self, sql_delete):
        conn = CommonDB.POOL.connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_delete)
            logger.info("执行删除数据sql【%s】，删除数据总量为：【%d】" % (sql_delete, cur.rowcount))
            # 提交事务，否则数据信息无变化，操作回滚
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
            conn.close()

    # 执行语句，返回第一行数据,返回的是一个一维元组
    def get_first_row_data(self, str_sql):
        # 取所有数据
        data = self.exec_query(str_sql)
        if len(data) == 0:
            return None
        # 返回第一行数据
        return data[0]

    # 执行语句，返回第一行第一列数据,返回的是一个字段的数据
    def get_first_row_first_column(self, str_sql):
        # 取第一行数据
        first_row_data = self.get_first_row_data(str_sql)
        if len(first_row_data) == 0:
            return None
        # 返回第一行第一列数据
        return first_row_data[0]

    # 判断符合sql条件的数据是否存在，存在返回true，否则返回false
    def data_is_exist(self, str_sql):
        data = self.exec_query(str_sql)
        if len(data) > 0:
            return True
        else:
            return False
