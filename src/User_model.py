import sqlite3


class User(object):
    def __init__(self, username, fullname, upload_record, reward_points, purchase_record):
        self.username = username
        self.fullname = fullname
        self.upload_record = upload_record
        self.reward_points = reward_points
        self.purchase_record = purchase_record

    def upload(self, filename, username):
        conn = sqlite3.connect('db/user_database.sqlite3')
        try:
            cursor = conn.cursor()
            sql1 = "SELECT upload_record FROM users WHERE username=?"
            cursor.execute(sql1, [username])
            result = cursor.fetchone()
            if result[0] is not None:
                result += (filename,)
                sql2 = "UPDATE users SET upload_record=? WHERE username=?"
                cursor.execute(sql2, [",".join(result), username])
            else:
                sql3 = "UPDATE users SET upload_record=? WHERE username=?"
                cursor.execute(sql3, [filename, username])
            print("update successfully")
            conn.commit()
            sql4 = "select upload_record from users where username=?"
            cursor.execute(sql4, [username])
            record = cursor.fetchone()
            self.upload_record = record
        except:
            print("update failed")
            conn.rollback()
        finally:
            conn.close()

    def buy(self, goods_name):
        conn_g = sqlite3.connect('db/goods.sqlite3')
        conn_u = sqlite3.connect('db/user_database.sqlite3')
        try:
            cursor_g = conn_g.cursor()
            cursor_u = conn_u.cursor()
            sql_g = 'select price from goods where goods_name=?'
            cursor_g.execute(sql_g, [goods_name])
            result_g = cursor_g.fetchone()
            print(result_g)
            for price in result_g:
                self.reward_points -= int(price)
            sql_u1 = 'update users set reward_points=? where username=?'
            cursor_u.execute(sql_u1, [self.reward_points, self.username])
            sql_u2 = 'select purchase_record from users where username=?'
            cursor_u.execute(sql_u2, [self.username])
            result = cursor_u.fetchone()
            if result[0] is not None:
                result += (goods_name,)
                sql_u3 = 'update users set purchase_record=? where username=?'
                cursor_u.execute(sql_u3, [",".join(result), self.username])
            else:
                sql_u4 = "UPDATE users SET purchase_record=? WHERE username=?"
                cursor_u.execute(sql_u4, [goods_name, self.username])
            conn_u.commit()
            sql_u5 = "select purchase_record from users where username=?"
            cursor_u.execute(sql_u5, [self.username])
            record = cursor_u.fetchone()
            self.purchase_record = record
            print('buy successfully')
        except:
            print("buy failed")
            conn_u.rollback()
        finally:
            conn_u.close()
            conn_g.close()



