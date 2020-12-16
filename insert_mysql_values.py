import pymysql

db = pymysql.connect(host="localhost", port=3306, user="root",
                     passwd="123456", database="mydict", charset="utf8")
cur = db.cursor()
f = open("英汉词典.txt", 'r', encoding='GBK')
for line in f:
    data = line.split("  ")
    sql = "insert into dict(word,interpret) values (%s,%s)"
    try:
        cur.execute(sql, [data[0], data[1]])
        db.commit()
    except Exception as e:
        db.rollback()
        print("插入失败", e)
        break
f.close()
cur.close()
db.close()
