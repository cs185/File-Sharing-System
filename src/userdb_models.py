import sqlite3
DB_FILES = 'db/user_database.sqlite3'


def init_db():
    conn = sqlite3.connect(DB_FILES)

    try:
        sql = """
        CREATE TABLE IF NOT EXISTS users(
            username TEXT primary key,
            password TEXT,
            fullname TEXT,
            upload_record TEXT, 
            reward_points INT DEFAULT 1000,
            purchase_record TEXT)
        """
        conn.execute(sql)
        print("user database created successfully")
    except:
        print("user database create database failed")
    finally:
        conn.close()


def find_all():
    user_list = []

    conn = sqlite3.connect(DB_FILES)

    try:
        cursor = conn.cursor()
        sql = """
            SELECT username, password, fullname, upload_record, reward_points, purchase_record FROM users
            """
        cursor.execute(sql)
        result_set = cursor.fetchall()

        for row in result_set:
            user_dict = {}
            user_dict['username'] = row[0]
            user_dict['password'] = row[1]
            user_dict['fullname'] = row[2]
            user_dict['upload_record'] = row[3]
            user_dict['reward_point'] = row[4]
            user_dict['purchase_record'] = row[5]
            user_list.append(user_dict)
    finally:
        conn.close()
    return user_list


def create(user):
    conn = sqlite3.connect(DB_FILES)

    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO users(username, password, fullname) VALUES (?,?,?)
            """
        afcount = cursor.execute(sql, [user["username"], user["password"], user["fullname"]])
        print("insert info row{0}".format(afcount))
        conn.commit()
    except:
        print("insert info failed")
        conn.rollback()
    finally:
        conn.close()


def remove(username):
    conn = sqlite3.connect(DB_FILES)

    try:
        cursor = conn.cursor()
        sql = """
            DELETE FROM users WHERE username=?
            """
        afcount = cursor.execute(sql, [username])
        print("remove info row{0}".format(afcount))

        conn.commit()
    except:
        print("remove info failed")
        conn.rollback()
    finally:
        conn.close()


def find_one(username):
    conn = sqlite3.connect(DB_FILES)
    try:
        cursor = conn.cursor()
        sql = """
                SELECT username, fullname, upload_record, reward_points, purchase_record FROM users WHERE username=?
                """
        cursor.execute(sql, [username])
        result_set = cursor.fetchone()
        return result_set

    finally:
        conn.close()


def delete(DB_FILES):
    conn = sqlite3.connect(DB_FILES)

    try:
        cursor = conn.cursor()
        sql = """
            DELETE FROM users
            """
        cursor.execute(sql)
        print("delete successfully")

        conn.commit()
    except:
        print("delete failed")
        conn.rollback()
    finally:
        conn.close()
