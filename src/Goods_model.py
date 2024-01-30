import sqlite3


class Goods(object):
    def __init__(self, DB_FILES):
        self.DB_FILES = DB_FILES

    def init_db(self):
        conn = sqlite3.connect(self.DB_FILES)

        try:
            sql = """
            CREATE TABLE IF NOT EXISTS goods(
                goods_name TEXT primary key,
                price INT DEFAULT 0,
                buyers TEXT)
            """
            conn.execute(sql)
            print("goods database created successfully")
        except:
            print("goods database create database failed")
        finally:
            conn.close()

    def find_all(self):
        goods_list = []

        conn = sqlite3.connect(self.DB_FILES)

        try:
            cursor = conn.cursor()
            sql = """
                SELECT goods_name, price, buyers FROM goods
                """
            cursor.execute(sql)
            result_set = cursor.fetchall()
            print(result_set)
            for row in result_set:
                goods_dict = {}
                goods_dict['goods_name'] = row[0]
                goods_dict['price'] = row[1]
                goods_dict['buyers'] = row[2]
                goods_list.append(goods_dict)
            print(goods_list)
        finally:
            conn.close()
        return goods_list

    def create(self, goods):
        conn = sqlite3.connect(self.DB_FILES)

        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO users(goods_name, price) VALUES (?,?)
                """
            afcount = cursor.execute(sql, [goods["goods_name"], goods["price"]])
            print("insert info row{0}".format(afcount))
            conn.commit()
        except:
            print("insert info failed")
            conn.rollback()
        finally:
            conn.close()

    def remove(self, goods_name):
        conn = sqlite3.connect(self.DB_FILES)

        try:
            cursor = conn.cursor()
            sql = """
                DELETE FROM goods WHERE good_name=?
                """
            afcount = cursor.execute(sql, [goods_name])
            print("remove info row{0}".format(afcount))

            conn.commit()
        except:
            print("remove info failed")
            conn.rollback()
        finally:
            conn.close()

    def delete(self):
        conn = sqlite3.connect(self.DB_FILES)

        try:
            cursor = conn.cursor()
            sql = """
                DELETE FROM goods
                """
            cursor.execute(sql)
            print("delete successfully")

            conn.commit()
        except:
            print("delete failed")
            conn.rollback()
        finally:
            conn.close()

    def find_one(self, good_name):
        conn = sqlite3.connect(self.DB_FILES)
        try:
            cursor = conn.cursor()
            sql = """
                    SELECT good_name, price, buyers FROM goods WHERE goods_name=?
                    """
            cursor.execute(sql, [good_name])
            result_set = cursor.fetchone()
            return result_set

        finally:
            conn.close()

    def find_price(self, goods_name):
        conn = sqlite3.connect(self.DB_FILES)
        try:
            cursor = conn.cursor()
            sql = """
                    SELECT price FROM goods WHERE goods_name=?
                    """
            cursor.execute(sql, [goods_name])
            result_set = cursor.fetchone()
            if result_set is not None:
                return result_set[0]
            else:
                return 0
        finally:
            conn.close()

    def sell(self, goods_name, username):
        conn = sqlite3.connect(self.DB_FILES)
        try:
            cursor = conn.cursor()
            sql1 = "SELECT buyers FROM goods WHERE goods_name=?"
            cursor.execute(sql1, [goods_name])
            result = cursor.fetchone()
            if result[0] is not None:
                result += (username,)
                sql2 = "UPDATE goods SET buyers=? WHERE goods_name=?"
                cursor.execute(sql2, [",".join(result), goods_name])
            else:
                sql3 = "UPDATE goods SET buyers=? WHERE goods_name=?"
                cursor.execute(sql3, [username, goods_name])
            print("sell successfully")
            conn.commit()
            # sql4 = "select buyers from users where goods_name=?"
            # cursor.execute(sql4, [goods_name])
            # buyers = cursor.fetchone()
            # return buyers
        except:
            print("sell failed")
            conn.rollback()
        finally:
            conn.close()



