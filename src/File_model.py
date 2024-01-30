# from filedb_models import create
# ALLOWED_EXTENSIONS = ('txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF')
import sqlite3


class Subject(object):
    def __init__(self, subject, DB_FILES):
        self.subject = subject
        self.DB_FILES = DB_FILES

    def init_db(self):
        conn = sqlite3.connect(self.DB_FILES)

        try:
            sql = """
            CREATE TABLE IF NOT EXISTS files(
                filename TEXT primary key,
                uploader TEXT,
                type TEXT,
                downloads INT DEFAULT 0,
                likes INT DEFAULT 0)
            """
            conn.execute(sql)
            print("{0} database created successfully".format(self.subject))
        except:
            print("file database create database failed")
        finally:
            conn.close()

    def find_all(self):
        file_list = []
        conn = sqlite3.connect(self.DB_FILES)
        try:
            cursor = conn.cursor()
            sql = """
                SELECT filename, uploader, type, downloads, likes FROM files
                """
            cursor.execute(sql)
            result_set = cursor.fetchall()

            for row in result_set:
                file_dict = {}
                file_dict['filename'] = row[0]
                file_dict['uploader'] = row[1]
                file_dict['type'] = row[2]
                file_dict['downloads'] = row[3]
                file_dict['likes'] = row[4]
                file_list.append(file_dict)
        finally:
            conn.close()
        return file_list

    def delete(self):
        conn = sqlite3.connect(self.DB_FILES)

        try:
            cursor = conn.cursor()
            sql = """
                DELETE FROM files
                """
            cursor.execute(sql)
            print("delete successfully")

            conn.commit()
        except:
            print("delete failed")
            conn.rollback()
        finally:
            conn.close()

    def remove(self, filename):
        conn = sqlite3.connect(self.DB_FILES)

        try:
            cursor = conn.cursor()
            sql = """
                DELETE FROM files WHERE filename=?
                """
            afcount = cursor.execute(sql, [filename])
            print("remove info row{0}".format(afcount))

            conn.commit()
        except:
            print("remove info failed")
            conn.rollback()
        finally:
            conn.close()

    def find_one(self, filename):
        conn = sqlite3.connect(self.DB_FILES)
        try:
            cursor = conn.cursor()
            sql = """
                    SELECT * FROM files WHERE filename=?
                    """
            cursor.execute(sql, [filename])
            result_set = cursor.fetchone()
            return result_set

        finally:
            conn.close()

    def create(self, filename, uploader, type):
        conn = sqlite3.connect(self.DB_FILES)

        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO files(filename, uploader, type) VALUES (?,?,?)
                """
            afcount = cursor.execute(sql, [filename, uploader, type])
            print("insert info row{0}".format(afcount))
            conn.commit()
        except:
            print("insert info failed")
            conn.rollback()
        finally:
            conn.close()


class File(object):
    def __init__(self, subject, filename, uploader, type, downloads, likes):
        self.subject = subject
        self.DB_FILES = self.subject.DB_FILES
        self.filename = filename
        self.uploader = uploader
        self.type = type
        self.downloads = downloads
        self.likes = likes

    def likes_plus(self):
        connd = sqlite3.connect(self.DB_FILES)
        connu = sqlite3.connect('db/user_database.sqlite3')
        self.likes += 1
        try:
            cursord = connd.cursor()
            cursoru = connu.cursor()
            sql = """
                            UPDATE files SET likes=? WHERE filename=?
                            """
            sql2 = 'update users set reward_points=reward_points + 10 where username=?'
            cursord.execute(sql, [self.likes, self.filename])
            cursoru.execute(sql2, [self.uploader])
            connd.commit()
            connu.commit()
            print('likes success')
        except:
            print("likes failed")
        finally:
            connd.close()
            connu.close()

    def downloads_plus(self):
        connd = sqlite3.connect(self.DB_FILES)
        connu = sqlite3.connect('db/user_database.sqlite3')
        print(self.downloads)
        self.downloads += 1
        try:
            cursord = connd.cursor()
            cursoru = connu.cursor()
            sql1 = """
                                    UPDATE files SET downloads=? WHERE filename=?
                                    """
            sql2 = 'update users set reward_points=reward_points + 50 where username=?'

            cursord.execute(sql1, [self.downloads, self.filename])
            cursoru.execute(sql2, [self.uploader])
            connd.commit()
            connu.commit()
            print('downloads success')
        except:
            print("downloads failed")
        finally:
            connd.close()
            connu.close()

    # def assign_reward(self):
    #     print(self.uploader)
    #     conn = sqlite3.connect('db/user_database.sqlite3')
    #     reward_points_new = self.downloads * 50 + self.likes * 10
    #     print('reward_points_new is {0}'.format(reward_points_new))
    #     try:
    #         cursor = conn.cursor()
    #         sql1 = 'select reward_points from users where username=?'
    #         cursor.execute(sql1, [self.uploader])
    #         rows = cursor.fetchone()
    #         reward_points_old = rows[0]
    #         # reward_points += reward_points_new
    #         print('reward points is {0}'.format(reward_points_old))
    #         sql2 = 'update users set reward_points=reward_points + ? where username=?'
    #         cursor.execute(sql2, [reward_points_new, self.uploader])
    #         conn.commit()
    #         print('assign reward successfully')
    #     except:
    #         print('assign reward failed')
    #     finally:
    #         conn.close()



    # def upload_to_db(self, filename, uploader, type):
    #     create(filename, uploader, type)

    # def allowed_file(filename):
    #     return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# math = Subject('math', 'db/math.sqlite3')
# a = math.find_one("001.jpg")
# print(a)
# a = math.find_downloads_likes('Carl')
# print(a)


