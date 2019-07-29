import sqlite3


class EasySqlite:
    """
    sqlite数据库操作工具类
    database: 数据库文件地址，例如：db/mydb.db
    """
    _connection = None

    def __init__(self, database):
        # 连接数据库
        self._connection = sqlite3.connect(database)

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql, args=[], result_dict=True, commit=True) -> list:
        """
        执行数据库操作的通用方法
        Args:
        sql: sql语句
        args: sql参数
        result_dict: 操作结果是否用dict格式返回
        commit: 是否提交事务
        Returns:
        list 列表，例如：
        [{'id': 1, 'name': '张三'}, {'id': 2, 'name': '李四'}]
        """
        if result_dict:
            self._connection.row_factory = self._dict_factory
        else:
            self._connection.row_factory = None
        # 获取游标
        _cursor = self._connection.cursor()
        # 执行SQL获取结果
        _cursor.execute(sql, args)
        if commit:
            self._connection.commit()
        data = _cursor.fetchall()
        _cursor.close()
        return data


if __name__ == '__main__':
    db = EasySqlite('article.db')
    # db.execute("create table article_down("
    #            "id int AUTO_INCREMENT primary key,"
    #            "source varchar(256),"   # 网站来源 中国知网/维普网
    #            "type varchar(256),"   # 类型 文献/期刊
    #            "title       varchar(256),"  # 标题
    #            "head_author varchar(256),"  # 首作者
    #            "file_name   varchar(256),"  # 文件名，不带.pdf后缀的
    #            "path        varchar(256),"  # 文件路径
    #            "create_time TIMESTAMP default (datetime('now', 'localtime'))"
    #            ")")
    # # 建立索引
    # db.execute("create index article_down__file_author on article_down (title, head_author)")
    # db.execute("create index article_down__filename on article_down (file_name)")
    #
    # # 插入语句
    # db.execute("insert into article_down(source,type,title,head_author,file_name,path) "
    #            "values ('cnki','cqvip','title','head_author','file_name','path')")

    r = db.execute("select * from article_down where source='中国知网' and type ='qikan' and title='title' and head_author='head_author'")
    print(r)
    print()
    # print(db.execute("select name from sqlite_master where type=?", ['table']))
    # print(db.execute("pragma table_info([user])"))
    # print(execute("insert into user(id, name, password) values (?, ?, ?)", [2, "李四", "123456"]))
    # print(db.execute("select id, name userName, password pwd from user"))
    # print(db.execute("select * from user", result_dict=False))
    # print(db.execute("select * from user"))
