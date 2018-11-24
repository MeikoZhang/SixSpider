import sqlite3


db_path="/Users/krison/data/result.db"

def getTables():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = """select name from sqlite_master where type='table' order by name"""
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    print(type(result))
    conn.close()


def getColumn():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = """pragma table_info(resultdb_video)"""
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    print(type(result))
    conn.close()

getColumn()

