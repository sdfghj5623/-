from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from contextlib import contextmanager
import os
import base64
import logging
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory
import json
import io
from flask import send_file
# 初始化Flask应用
app = Flask(__name__)
CORS(app)

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置上传文件夹和允许的文件类型
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class DatabaseInterface:
    def __init__(self, db_name):
        """ 初始化数据库连接 """
        self.db_name = db_name

    def get_connection(self):
        """ 获取数据库连接 """
        connection = sqlite3.connect(self.db_name)
        return connection

    @contextmanager
    def get_cursor(self):
        """ 获取游标并确保自动提交和关闭连接 """
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except sqlite3.Error as e:
            logger.error(f"数据库操作发生错误: {e}")
            if connection:
                connection.rollback()  # 发生错误时回滚事务
            raise
        finally:
            if connection:
                connection.close()

    def insert_user(self, data):
        """ 插入新数据到users表 """
        with self.get_cursor() as cursor:
            # 不再对密码进行哈希处理，直接使用原始密码
            password = data['password']
            nickname = data.get('nickname', '匿名用户')
            ip_address = data.get('IP', '火星')
            role = data.get('role', '普通用户')

            insert_sql = """
                INSERT INTO users (zhanghao, nickname, password, IP, role)
                VALUES (?, ?, ?, ?, ?)
            """

            cursor.execute(insert_sql, (
                data['zhanghao'],
                nickname,
                password,  # 直接存储明文密码
                ip_address,
                role
            ))

    def fetch_user_by_zhanghao(self, zhanghao):
        """ 根据账号或者手机号码查询用户信息 """
        with self.get_cursor() as cursor:
            # 使用 OR 来同时匹配 zhanghao 或者 mobile
            select_sql = """
                SELECT id, zhanghao, nickname, password, role 
                FROM users 
                WHERE zhanghao = ? OR mobile = ?
            """
            cursor.execute(select_sql, (zhanghao, zhanghao))  # 传递相同的参数进行查询
            return cursor.fetchone()

    def update_article(self, data):
        """ 更新现有文章 """
        with self.get_cursor() as cursor:
            update_sql = """
                UPDATE article
                SET title = ?, leibie = ?, content = ?, time = ?
                WHERE id = ?
            """
            cursor.execute(update_sql, (
                data['title'],
                data['leibie'],
                data['content'],
                data['time'],
                data['article_id']
            ))
            return cursor.rowcount  # 返回更新的行数

    def update_article_pictures(self, article_id, pictures):
        """ 更新文章的图片，将旧图片删除后插入新的图片 """
        with self.get_cursor() as cursor:
            # 删除旧的图片
            delete_sql = "DELETE FROM article_pictures WHERE article_id = ?"
            cursor.execute(delete_sql, (article_id,))

            # 插入新的图片
            for picture in pictures:
                picture_sql = """
                    INSERT INTO article_pictures (article_id, picture_data)
                    VALUES (?, ?)
                """
                cursor.execute(picture_sql, (article_id, picture))
            return cursor.rowcount  # 返回插入的行数

    def delete_article_pictures(self, picture_id):
        """ 更新文章的图片，将旧图片删除后插入新的图片 """
        with self.get_cursor() as cursor:
            # 删除旧的图片
            delete_sql = "DELETE FROM article_pictures WHERE picture_id = ?"
            cursor.execute(delete_sql, (picture_id))

    # 插入文章到article表
    def insert_article(self, data):
        """ 插入新文章到article表 """
        with self.get_cursor() as cursor:
            insert_sql = """
                INSERT INTO article (ip, title, leibie, content, time)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(insert_sql, (
                data['ip'],
                data['title'],
                data['leibie'],
                data['content'],
                data['time']
            ))
            # 获取插入后的article_id
            article_id = cursor.lastrowid
        return article_id

    def insert_quanzi_article(self, data):
        """ 插入新文章到article表 """
        with self.get_cursor() as cursor:
            insert_sql = """
                INSERT INTO quanzi_article (ip, title, user_id, content, publish_date)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(insert_sql, (
                data['ip'],
                data['title'],
                data['user_id'],
                data['content'],
                data['publish_date']
            ))
            # 获取插入后的article_id
            quanzi_article_id = cursor.lastrowid
        return quanzi_article_id

    def insert_quanzi_article_user(self, data):
        """ 插入新文章到article表 """
        with self.get_cursor() as cursor:
            insert_sql = """
                INSERT INTO user_article (user_id,article_id)
                VALUES (?, ?)
            """
            cursor.execute(insert_sql, (
                data['user_id'],
                data['article_id']
            ))


    def insert_shibie(self, data):
        """ 插入新文章到article表 """
        with self.get_cursor() as cursor:
            insert_sql = """
                INSERT INTO shibie (tem, shidu, co2, pic,user_id,flag,time,className,sco,resu)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_sql, (
                data['tem'],
                data['shidu'],
                data['co2'],
                data['pic'],
                data['user_id'],
                data['flag'],
                data['time'],
                data['className'],
                data['sco'],
                data['resu']
            ))


    def insert_shibie_return(self, data):
        """ 插入新文章到article表 """
        with self.get_cursor() as cursor:
            insert_sql = """
                INSERT INTO shibie_return (TF, zhuangtai, pingjia,time)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(insert_sql, (
                data['TF'],
                data['zhuangtai'],
                data['pingjia'],
                data['time']
            ))
            shibie_return_id = cursor.lastrowid
        return shibie_return_id

    def insert_article_pictures(self, article_id, pictures):
        """ 插入图片到article_pictures表 """
        with self.get_cursor() as cursor:
            for picture in pictures:
                picture_sql = """
                    INSERT INTO article_pictures (article_id, picture_data)
                    VALUES (?, ?)
                """
                cursor.execute(picture_sql, (article_id, picture))

    def insert_quanzi_article_pictures(self, quanzi_article_id, pictures):
        """ 插入图片到article_pictures表 """
        with self.get_cursor() as cursor:
            for picture in pictures:
                picture_sql = """
                    INSERT INTO quanzi_article_pic (quanzi_article_id, pic)
                    VALUES (?, ?)
                """
                cursor.execute(picture_sql, (quanzi_article_id, picture))

    def insert_shibie_return_pictures(self, shibie_return_id, pictures):
        """ 插入图片到article_pictures表 """
        with self.get_cursor() as cursor:
            for picture in pictures:
                picture_sql = """
                    INSERT INTO shibie_return_pic (shibie_return_id, pic)
                    VALUES (?, ?)
                """
                cursor.execute(picture_sql, (shibie_return_id, picture))

    import base64

    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def fetch_articles(self, skip=0, limit=10):
        """ 从article表和article_pictures表中获取文章列表 """
        with self.get_cursor() as cursor:
            select_sql = """
                SELECT a.id, a.ip, a.title, a.leibie, a.content, a.time
                FROM article a
                ORDER BY a.id DESC
                LIMIT ? OFFSET ?
            """
            cursor.execute(select_sql, (limit, skip))
            articles = cursor.fetchall()

            processed_articles = []
            for row in articles:
                article_id = row[0]
                select_pictures_sql = """
                    SELECT picture_data
                    FROM article_pictures
                    WHERE article_id = ?
                """
                cursor.execute(select_pictures_sql, (article_id,))
                pictures_rows = cursor.fetchall()
                pictures = [
                    base64.b64encode(pic[0]).decode('utf-8')  # 将图片BLOB数据转换为Base64编码的字符串
                    for pic in pictures_rows
                ]

                processed_article = {
                    'id': row[0],
                    'ip': row[1],
                    'title': row[2],
                    'leibie': row[3],
                    'content': row[4],
                    'time': row[5],
                    'pictures': pictures  # 图片字段返回多个图片
                }

                processed_articles.append(processed_article)
            return processed_articles

    def fetch_shibie_return_data(self, skip=0, limit=10):
        """ 从article表和article_pictures表中获取文章列表 """
        with self.get_cursor() as cursor:
            select_sql = """
                SELECT a.id, a.TF, a.zhuangtai, a.pingjia,  a.time
                FROM shibie_return a
                ORDER BY a.id DESC
                LIMIT ? OFFSET ?
            """
            cursor.execute(select_sql, (limit, skip))
            shibie_return_datas = cursor.fetchall()
            print("111",shibie_return_datas)

            processed_shibie_return_datas = []
            for row in shibie_return_datas:
                shibie_return_data_id = row[0]
                select_pictures_sql = """
                    SELECT pic
                    FROM shibie_return_pic
                    WHERE shibie_return_id = ?
                """
                cursor.execute(select_pictures_sql, (shibie_return_data_id,))
                pictures_row = cursor.fetchone()
                print('pictures_row',pictures_row)
                if pictures_row:
                    pictures = base64.b64encode(pictures_row[0]).decode('utf-8')
                    print('111')
                else:
                    pictures = None

                processed_shibie_return_data = {
                    'id': row[0],
                    'TF': row[1],
                    'zhuangtai': row[2],
                    'pingjia': row[3],
                    'time': row[4],
                    'pictures': pictures  # 图片字段返回多个图片
                }

                processed_shibie_return_datas.append(processed_shibie_return_data)
            return processed_shibie_return_datas

    def fetch_quanzi_articles(self, skip=0, limit=10, order_by="id DESC"):
        """ 从article表和article_pictures表中获取文章列表，支持动态排序 """
        with self.get_cursor() as cursor:
            # 构建 SQL 查询语句，order_by 默认值是 'id DESC'
            print('order_by',order_by)
            select_sql = f"""
                SELECT a.id, a.user_id, a.title, a.status, a.view_count, a.like_count, a.comment_count, a.publish_date, a.content, a.ip
                FROM quanzi_article a
                ORDER BY {order_by}  -- 动态插入排序条件
                LIMIT ? OFFSET ?
            """
            cursor.execute(select_sql, (limit, skip))
            quanzi_articles = cursor.fetchall()

            processed_articles = []
            for row in quanzi_articles:
                quanzi_article_id = row[0]
                select_pictures_sql = """
                    SELECT pic
                    FROM quanzi_article_pic
                    WHERE quanzi_article_id = ?
                """
                cursor.execute(select_pictures_sql, (quanzi_article_id,))
                pictures_rows = cursor.fetchall()
                pictures = [
                    base64.b64encode(pic[0]).decode('utf-8')  # 将图片BLOB数据转换为Base64编码的字符串
                    for pic in pictures_rows
                ]

                processed_article = {
                    'id': row[0],
                    'user_id': row[1],
                    'title': row[2],
                    'status': row[3],
                    'view_count': row[4],
                    'like_count': row[5],
                    'comment_count': row[6],
                    'publish_date': row[7],
                    'content': row[8],
                    'ip': row[9],
                    'pictures': pictures  # 图片字段返回多个图片
                }

                processed_articles.append(processed_article)
            print("content",len(processed_articles))

            return processed_articles

    import base64

    def fetch_shibie_lishi(self, user_id, skip=0, limit=10):
        """ 从article表和article_pictures表中获取文章列表 """
        with self.get_cursor() as cursor:
            select_sql = """
                SELECT a.tem, a.shidu, a.co2, a.pic, a.flag, a.time, a.className, a.sco, a.resu
                FROM shibie a
                WHERE a.user_id = ?
                ORDER BY a.tem DESC
                LIMIT ? OFFSET ?
            """
            cursor.execute(select_sql, (user_id, limit, skip))
            lishi = cursor.fetchall()
            # print('lishi',lishi)

            processed_articles = []
            for row in lishi:
                # 对图片字段进行Base64编码
                pic_base64 = base64.b64encode(row[3]).decode('utf-8') if row[3] else None
                resu_base64 = base64.b64encode(row[8]).decode('utf-8') if row[8] else None

                processed_article = {
                    'tem': row[0],
                    'shidu': row[1],
                    'co2': row[2],
                    'pic': pic_base64,  # 将编码后的图片添加到结果中
                    'flag': row[4],
                    'time': row[5],
                    'className': row[6],
                    'sco': row[7],
                    'resu': resu_base64,  # 将编码后的图片添加到结果中
                }

                processed_articles.append(processed_article)
            return processed_articles

    # def fetch_article_by_id(self, article_id):
    #     """ 根据文章ID查询详细内容和关联图片 """
    #     with self.get_cursor() as cursor:
    #
    #
    #         # 获取文章基本信息
    #         select_article_sql = """
    #             SELECT id, ip, title, leibie, content, time
    #             FROM article
    #             WHERE id = ?
    #         """
    #         cursor.execute(select_article_sql, (article_id,))
    #         article = cursor.fetchone()
    #
    #         if not article:
    #             return None  # 文章不存在
    #
    #         # 获取该文章的所有图片
    #         select_pictures_sql = """
    #             SELECT picture_data
    #             FROM article_pictures
    #             WHERE article_id = ?
    #         """
    #         cursor.execute(select_pictures_sql, (article_id,))
    #         pictures_rows = cursor.fetchall()
    #
    #         pictures = [
    #             base64.b64encode(pic[0]).decode('utf-8')  # 将图片BLOB数据转换为Base64编码的字符串
    #             for pic in pictures_rows
    #         ]
    #
    #         # 构建文章详情数据
    #         processed_article = {
    #             'id': article[0],
    #             'ip': article[1],
    #             'title': article[2],
    #             'leibie': article[3],
    #             'content': article[4],
    #             'time': article[5],
    #             'pictures': pictures  # 图片字段返回多个图片
    #         }
    #
    #         return processed_article

    def fetch_article_by_id(self, article_id):
        """根据文章ID查询详细内容和关联图片"""
        with self.get_cursor() as cursor:

            # 使用JOIN查询一次性获取文章和图片数据
            select_article_with_pictures_sql = """
                SELECT a.id, a.ip, a.title, a.leibie, a.content, a.time, ap.picture_data
                FROM article a
                LEFT JOIN article_pictures ap ON a.id = ap.article_id
                WHERE a.id = ?
            """
            cursor.execute(select_article_with_pictures_sql, (article_id,))
            rows = cursor.fetchall()

            if not rows:
                return None  # 文章不存在

            # 提取文章的基本信息
            article = rows[0]  # 获取第一行的文章信息
            pictures = []

            # 提取所有图片
            for row in rows:
                picture_data = row[6]  # 图片数据在第7列
                if picture_data:
                    pictures.append(base64.b64encode(picture_data).decode('utf-8'))

            # 构建文章详情数据
            processed_article = {
                'id': article[0],
                'ip': article[1],
                'title': article[2],
                'leibie': article[3],
                'content': article[4],
                'time': article[5],
                'pictures': pictures  # 图片字段返回多个图片
            }

            return processed_article

    def delete_article_by_id(self, article_id):
        """ 根据文章ID删除文章及其关联图片 """
        with self.get_cursor() as cursor:
            try:
                # 删除文章的所有图片
                delete_pictures_sql = """
                    DELETE FROM article_pictures WHERE article_id = ?
                """
                cursor.execute(delete_pictures_sql, (article_id,))

                # 删除文章记录
                delete_article_sql = """
                    DELETE FROM article WHERE id = ?
                """
                cursor.execute(delete_article_sql, (article_id,))

            except sqlite3.Error as e:
                logger.error(f"删除文章或图片失败: {e}")
                raise

    # def delete_article_by_id(self, article_id):
    #     """ 根据文章ID删除文章及其关联图片 """
    #     with self.get_cursor() as cursor:
    #         try:
    #             # 删除文章的所有图片
    #             # delete_pictures_sql = """
    #             #     DELETE FROM article_pictures LEFT JOIN  WHERE article_id = ?
    #             # """
    #             # cursor.execute(delete_pictures_sql, (article_id,))
    #
    #             # 删除文章记录
    #             delete_article_sql = """
    #                 DELETE FROM article a LEFT JOIN article_pictures ap ON a.id = ap.article_id WHERE id = ?
    #             """
    #             cursor.execute(delete_article_sql, (article_id,))
    #
    #         except sqlite3.Error as e:
    #             logger.error(f"删除文章或图片失败: {e}")
    #             raise



# 创建DatabaseInterface实例
db = DatabaseInterface(r'D:\mydb.db')  # 指定数据库文件

@app.route('/api/register', methods=['POST'])
def register_user():
    """ 处理用户注册请求 """
    try:
        data = request.json  # 假设客户端发送JSON格式的数据

        # 检查必要的字段是否存在
        required_fields = {'zhanghao', 'password'}
        if not required_fields.issubset(set(data.keys())):
            return jsonify({'error': '缺少必要的字段'}), 400

        try:
            db.insert_user(data)
            return jsonify({'message': '注册成功'}), 201
        except sqlite3.IntegrityError as e:
            return jsonify({'error': '用户名或账号已存在'}), 409
        except Exception as e:
            logger.error(f"注册失败: {str(e)}")
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        logger.error(f"服务器内部错误: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


@app.route('/api/login', methods=['POST'])
def login_user():
    """ 处理用户登录请求 """
    try:
        data = request.json  # 假设客户端发送JSON格式的数据

        # 检查必要的字段是否存在
        required_fields = {'zhanghao', 'password'}
        if not required_fields.issubset(set(data.keys())):
            return jsonify({'error': '缺少必要的字段'}), 400

        # 从数据库查询用户
        user = db.fetch_user_by_zhanghao(data['zhanghao'])
        print('user',user[3])
        print('Stored password type:', type(user[3]))

        if user is None:
            return jsonify({'error': '账号不存在'}), 401

        stored_password = user[3]
        print('data',data['password'])

        # 比较输入的密码与存储的密码是否一致
        if stored_password == data['password']:
            return jsonify({
                'message': '登录成功',
                'user': {
                    'id': user[0],
                    'zhanghao': user[1],
                    'nickname': user[2],
                    'role': user[4]
                }
            }), 200
        else:
            return jsonify({'error': '密码错误'}), 401

    except Exception as e:
        logger.error(f"登录失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

@app.route('/api/user_info_get/<int:user_id>', methods=['GET'])
def user_info_get(user_id):
    try:
        with db.get_cursor() as cursor:
            cursor.execute("SELECT avatar FROM users WHERE id = ?", (user_id,))
            user_pic = cursor.fetchone()

            # 检查 user_pic 是否存在，且提取字节数据进行 Base64 编码
            if user_pic and user_pic[0]:  # 确保 user_pic 存在且不为空
                user_pic_data = user_pic[0]  # 获取头像的字节数据
                user_pic_base64 = base64.b64encode(user_pic_data).decode('utf-8')  # 转换为 Base64 字符串
            else:
                user_pic_base64 = None  # 如果没有头像，设置为 None

            cursor.execute("SELECT  nickname FROM users WHERE id = ?", (user_id,))
            user_nickname = cursor.fetchone()

            cursor.execute("SELECT  mobile FROM users WHERE id = ?", (user_id,))
            user_mobile = cursor.fetchone()


            user_data = {
                'user_nickname': user_nickname,
                'user_pic': user_pic_base64,
                'user_mobile':user_mobile
            }

            # 返回JSON响应
            return jsonify({'user_info': user_data}), 200



        return jsonify({'message': '点赞状态更新成功'}), 200
    except Exception as e:
        logger.error(f"更新点赞状态失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


def normalize_path(path):
    return os.path.normpath(path).replace(os.sep, '/')

@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        skip = int(request.args.get('skip', 0))  # 默认从第0篇文章开始
        limit = int(request.args.get('limit', 10))  # 每页限制10篇文章

        articles = db.fetch_articles(skip, limit)

        return jsonify({
            'articles': articles,
            'count': len(articles)
        }), 200

    except ValueError as ve:
        return jsonify({'error': '无效的参数'}), 400
    except Exception as e:
        logger.error(f"获取文章列表失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


@app.route('/api/shibie_return_data', methods=['GET'])
def get_shibie_return_data():
    try:
        skip = int(request.args.get('skip', 0))  # 默认从第0篇文章开始
        limit = int(request.args.get('limit', 10))  # 每页限制10篇文章

        shibie_return_datas = db.fetch_shibie_return_data(skip, limit)

        return jsonify({
            'articles': shibie_return_datas,
            'count': len(shibie_return_datas)
        }), 200

    except ValueError as ve:
        return jsonify({'error': '无效的参数'}), 400
    except Exception as e:
        logger.error(f"获取用户反馈列表失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

@app.route('/api/quanzi_articles', methods=['GET'])
def get_quanzi_articles():
    try:
        skip = int(request.args.get('skip', 0))  # 默认从第0篇文章开始
        limit = int(request.args.get('limit', 10))  # 每页限制10篇文章
        canshu = request.args.get('canshu')

        quanzi_articles = db.fetch_quanzi_articles(skip, limit,canshu)

        return jsonify({
            'quanzi_articles': quanzi_articles,
            'count': len(quanzi_articles)
        }), 200

    except ValueError as ve:
        return jsonify({'error': '无效的参数'}), 400
    except Exception as e:
        logger.error(f"获取文章列表失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


# 删除文章
# @app.route('/api/delete_quanzi_article', methods=['POST'])
# def delete_quanzi_article():
#     try:
#         article_id = int(request.json.get('article_id'))
#         user_id = int(request.json.get('user_id'))
#
#         with db.get_cursor() as cursor:
#             # 开始事务，确保操作的原子性
#             cursor.execute("BEGIN TRANSACTION;")
#
#             # 1. 更新 quanzi_article 表，标记文章为已删除
#             delete_sql = """
#                 DELETE quanzi_article
#                 SET status = 1
#                 WHERE id = ?
#             """
#             cursor.execute(delete_sql, (article_id,))
#
#             # 2. 删除 user_article 表中的记录，移除与该文章相关的用户记录
#             # delete_sql = """
#             #     DELETE FROM user_article
#             #     WHERE article_id = ? AND user_id = ?
#             # """
#             # cursor.execute(delete_sql, (article_id, user_id))
#
#             # 提交事务
#             cursor.execute("COMMIT;")
#
#         return jsonify({'message': '文章及相关记录已删除'}), 200
#     except Exception as e:
#         # 如果发生任何异常，回滚事务并返回错误信息
#         cursor.execute("ROLLBACK;")
#         logger.error(f"删除文章失败: {str(e)}")
#         return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

# @app.route('/api/delete_quanzi_article', methods=['POST'])
# def delete_quanzi_article():
#     try:
#         article_id = int(request.json.get('article_id'))
#         user_id = int(request.json.get('user_id'))
#
#         with db.get_cursor() as cursor:
#             # 开始事务，确保操作的原子性
#             cursor.execute("BEGIN TRANSACTION;")
#
#             # 1. 更新 quanzi_article 表，标记文章为已删除
#             delete_sql = """
#                 DELETE quanzi_article
#                 WHERE id = ?
#             """
#             cursor.execute(delete_sql, (article_id,))
#
#             # 2. 删除 user_article 表中的记录，移除与该文章相关的用户记录
#             # delete_sql = """
#             #     DELETE FROM user_article
#             #     WHERE article_id = ? AND user_id = ?
#             # """
#             # cursor.execute(delete_sql, (article_id, user_id))
#
#             # 提交事务
#             cursor.execute("COMMIT;")
#
#         return jsonify({'message': '文章及相关记录已删除'}), 200
#     except Exception as e:
#         # 如果发生任何异常，回滚事务并返回错误信息
#         cursor.execute("ROLLBACK;")
#         logger.error(f"删除文章失败: {str(e)}")
#         return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

@app.route('/api/delete_quanzi_article_comment', methods=['POST'])
def delete_quanzi_article_comment():
    try:
        article_id = int(request.json.get('article_id'))
        comment_id = int(request.json.get('comment_id'))
        print(article_id,comment_id)

        with db.get_cursor() as cursor:
            # 开始事务，确保操作的原子性
            cursor.execute("BEGIN TRANSACTION;")

            # 1. 更新 quanzi_article 表，标记文章为已删除
            # update_sql = """
            #     UPDATE quanzi_article
            #     SET comment_count = comment_count-1
            #     WHERE id = ?
            # """
            # cursor.execute(update_sql, (article_id,))

            # 2. 删除 user_article 表中的记录，移除与该文章相关的用户记录
            delete_sql = """
                DELETE FROM quanzi_comment
                WHERE id = ?
            """
            cursor.execute(delete_sql, (comment_id,))

            # 提交事务
            cursor.execute("COMMIT;")

        return jsonify({'message': '评论及相关记录已删除'}), 200
    except Exception as e:
        # 如果发生任何异常，回滚事务并返回错误信息
        cursor.execute("ROLLBACK;")
        logger.error(f"删除评论失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}),




@app.route('/api/delete_quanzi_article', methods=['POST'])
def delete_quanzi_article():
    connection = None
    cursor = None
    try:
        article_id = int(request.json.get('article_id'))
        user_id = int(request.json.get('user_id'))

        # 手动获取数据库连接
        connection = db.get_connection()  # 假设这是你获取数据库连接的方式
        cursor = connection.cursor()

        # 开始事务
        cursor.execute("BEGIN TRANSACTION;")

        # 1. 更新 quanzi_article 表，标记文章为已删除
        delete_sql = """
            DELETE FROM quanzi_article
            WHERE id = ?
        """
        cursor.execute(delete_sql, (article_id,))

        # 2. 删除 user_article 表中的记录，移除与该文章相关的用户记录
        # delete_sql = """
        #     DELETE FROM user_article
        #     WHERE article_id = ? AND user_id = ?
        # """
        # cursor.execute(delete_sql, (article_id, user_id))

        # 提交事务
        connection.commit()

        return jsonify({'message': '文章及相关记录已删除'}), 200

    except Exception as e:
        if connection:
            connection.rollback()  # 发生异常时回滚事务
        logger.error(f"删除文章失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

    finally:
        if cursor:
            cursor.close()  # 关闭游标
        if connection:
            connection.close()  # 关闭连接






# 判断用户是否点赞过文章
@app.route('/api/check_like', methods=['GET'])
def check_like():
    try:
        user_id = int(request.args.get('user_id'))
        article_id = int(request.args.get('article_id'))

        with db.get_cursor() as cursor:
            select_sql = """
                SELECT 1 FROM user_like_article 
                WHERE user_id = ? AND like_article_id = ?
            """
            cursor.execute(select_sql, (user_id, article_id))
            is_liked = cursor.fetchone() is not None

        return jsonify({'is_liked': is_liked}), 200
    except Exception as e:
        logger.error(f"检查点赞状态失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

# 添加一个获取用户信息的接口
@app.route('/api/user_info', methods=['GET'])
def get_user_info():
    try:
        user_id = int(request.args.get('user_id'))
        with db.get_cursor() as cursor:
            select_sql = """
                SELECT nickname, avatar
                FROM users
                WHERE id = ?
            """
            cursor.execute(select_sql, (user_id,))
            user_info = cursor.fetchone()

        if user_info:
            nickname, avatar = user_info
            return jsonify({
                'nickname': nickname,
                'avatar': base64.b64encode(avatar).decode('utf-8') if avatar else None
            }), 200
        else:
            return jsonify({'error': '用户未找到'}), 404
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

#用户评论视图
@app.route('/api/user_comment', methods=['GET'])
def get_user_comment():
    try:
        # 获取传入的 user_id 参数
        user_id = int(request.args.get('user_id'))

        # 执行 SQL 查询
        with db.get_cursor() as cursor:
            select_sql = """
                SELECT user_id, user_nickname, comment_id, comment_content, comment_date, comment_staus
                FROM user_comments_view
                WHERE user_id = ?
            """
            cursor.execute(select_sql, (user_id,))
            user_comments = cursor.fetchall()  # 获取所有数据

        # 如果查询到数据
        if user_comments:
            # 将查询结果转换为字典列表
            user_comments_list = [
                {
                    'user_id': comment[0],
                    'user_nickname': comment[1],
                    'comment_id': comment[2],
                    'comment_content': comment[3],
                    'comment_date': comment[4],
                    'comment_staus': comment[5]
                }
                for comment in user_comments
            ]
            return jsonify({'user_comments': user_comments_list}), 200

        # 如果没有找到对应的评论
        else:
            return jsonify({'error': '未找到该用户的评论'}), 404

    except Exception as e:
        logger.error(f"获取用户评论信息失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500



@app.route('/api/shibie_lishi/<int:user_id>', methods=['GET'])
def get_shibie_lishi(user_id):
    try:
        skip = int(request.args.get('skip', 0))  # 默认从第0篇文章开始
        limit = int(request.args.get('limit', 10))  # 每页限制10篇文章

        lishi = db.fetch_shibie_lishi(user_id,skip, limit, )

        return jsonify({
            'lishi': lishi,
            'count': len(lishi)
        }), 200

    except ValueError as ve:
        return jsonify({'error': '无效的参数'}), 400
    except Exception as e:
        logger.error(f"获取历史列表失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

@app.route('/api/article/<int:id>', methods=['GET'])
def get_article_by_id(id):
    try:
        # 从数据库中获取文章详情
        article = db.fetch_article_by_id(id)

        if article:
            return jsonify({
                'article': article
            }), 200
        else:
            return jsonify({'error': '文章未找到'}), 404

    except Exception as e:
        logger.error(f"获取文章详情失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


@app.route('/api/images/<int:image_id>', methods=['GET'])
def serve_image(image_id):
    try:
        with db.get_cursor() as cursor:
            select_sql = "SELECT pictures FROM article WHERE id = ?"
            cursor.execute(select_sql, (image_id,))
            result = cursor.fetchone()
            if result:
                pictures = result[0]
                if pictures:
                    # 假设pictures字段存储的是单个图片的BLOB数据
                    image_stream = io.BytesIO(pictures)
                    return send_file(image_stream, mimetype='image/jpeg')
                else:
                    return jsonify({'error': 'No pictures found'}), 404
            else:
                return jsonify({'error': 'Article not found'}), 404
    except Exception as e:
        logger.error(f"获取图片失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


import io
from werkzeug.utils import secure_filename


@app.route('/api/insert_articles', methods=['POST'])  # 修正了路由路径
def add_article():
    try:
        # 获取表单字段
        title = request.form.get('title')
        leibie = request.form.get('leibie')
        content = request.form.get('content')
        time = request.form.get('time')
        ip = request.remote_addr

        # 检查必要的字段是否存在
        if not all([title, leibie, content, time]):
            return jsonify({'error': '缺少必要的字段'}), 400

        # 调试：打印表单数据
        print('Form data:', request.form)
        print('Files:', request.files)

        # 处理上传的图片
        pictures_data = []  # 用于存储所有图片的二进制数据
        if 'pictures[]' in request.files:  # 检查文件字段是否存在
            files = request.files.getlist('pictures[]')  # 获取所有上传的文件
            for file in files:
                if file and allowed_file(file.filename):  # 验证文件类型
                    img_data = file.read()  # 读取图片为字节流
                    pictures_data.append(img_data)  # 将字节流加入到列表中
                else:
                    return jsonify({'error': '上传的文件无效'}), 400
        else:
            print("没有收到图片文件")

        # 创建文章数据
        article_data = {
            'ip': ip,
            'title': title,
            'leibie': leibie,
            'content': content,
            'time': time,
        }

        # 插入文章数据
        article_id = db.insert_article(article_data)

        # 插入图片数据
        if pictures_data:
            db.insert_article_pictures(article_id, pictures_data)

        return jsonify({'message': '文章发布成功'}), 201

    except Exception as e:
        logging.error(f"发布文章失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


@app.route('/api/insert_quanzi_articles', methods=['POST'])  # 修正了路由路径
def add_quanzi_article():
    try:
        # 获取表单字段
        title = request.form.get('title')
        user_id = request.form.get('user_id')
        content = request.form.get('content')
        publish_date = request.form.get('publish_date')
        ip = request.remote_addr

        # 检查必要的字段是否存在
        if not all([title, user_id, content, publish_date]):
            return jsonify({'error': '缺少必要的字段'}), 400

        # 调试：打印表单数据
        print('Form data:', request.form)
        print('Files:', request.files)

        # 处理上传的图片
        pictures_data = []  # 用于存储所有图片的二进制数据
        if 'pictures[]' in request.files:  # 检查文件字段是否存在
            files = request.files.getlist('pictures[]')  # 获取所有上传的文件
            for file in files:
                if file and allowed_file(file.filename):  # 验证文件类型
                    img_data = file.read()  # 读取图片为字节流
                    pictures_data.append(img_data)  # 将字节流加入到列表中
                else:
                    return jsonify({'error': '上传的文件无效'}), 400
        else:
            print("没有收到图片文件")

        # 创建文章数据
        quanzi_article_data = {
            'ip': ip,
            'title': title,
            'user_id': user_id,
            'content': content,
            'publish_date': publish_date,
        }



        # 插入文章数据
        quanzi_article_id = db.insert_quanzi_article(quanzi_article_data)

        quanzi_article_user_data = {
            'user_id': user_id,
            'article_id':quanzi_article_id
        }

        # 插入图片数据
        if pictures_data:
            db.insert_quanzi_article_pictures(quanzi_article_id, pictures_data)

        db.insert_quanzi_article_user(quanzi_article_user_data)

        return jsonify({'message': '文章发布成功'}), 201

    except Exception as e:
        logging.error(f"发布文章失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


@app.route('/api/inster_shibie', methods=['POST'])
def addshibie():
    try:
        # 获取表单字段
        tem = request.form.get('tem')
        shidu = request.form.get('shidu')
        co2 = request.form.get('co2')
        pic = request.files.get('pic')  # 改成 request.files.get() 来获取文件
        resu = request.files.get('result_pic')  # 获取 result_pic 文件
        time = request.form.get('time')  # user_id 使用 request.form.get()
        flag = request.form.get('flag')
        className = request.form.get('className')
        sco = request.form.get('sco')
        user_id = request.form.get('user_id')


        # 检查必要的字段是否存在
        if not all([tem, shidu, co2, user_id, pic,flag,resu,time,className,sco]):
            return jsonify({'error': '缺少必要的字段'}), 400

        # 打印调试信息
        print('Form data:', request.form)
        print('Files:', request.files)

        # 处理上传的图片文件
        if pic and allowed_file(pic.filename):
            pic_data = pic.read()  # 读取文件字节流
        else:
            return jsonify({'error': '上传的 pic 文件无效'}), 400

        if resu and allowed_file(resu.filename):
            result_pic_data = resu.read()  # 读取结果图字节流
        else:
            result_pic_data = None  # 如果没有结果图文件

        # 将数据插入数据库
        shibie_data = {
            'tem': tem,
            'shidu': shidu,
            'co2': co2,
            'pic': pic_data,  # 存储为字节流
            'user_id': user_id,
            'flag':flag,
            'resu':result_pic_data,
            'time':time,
            'sco':sco,
            'className':className
        }

        db.insert_shibie(shibie_data)

        return jsonify({'message': '识别保存成功'}), 201

    except Exception as e:
        logging.error(f"识别保存失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

@app.route('/api/insert_shibie_return', methods=['POST'])  # 修正了路由路径
def add_shibie_return():
    try:
        # 获取表单字段
        TF = request.form.get('TF')
        zhuangtai = request.form.get('zhuangtai')
        pingjia = request.form.get('pingjia')
        time = request.form.get('time')


        # 检查必要的字段是否存在
        if not all([TF, zhuangtai, pingjia,time]):
            return jsonify({'error': '缺少必要的字段'}), 400

        # 调试：打印表单数据
        print('Form data:', request.form)
        print('Files:', request.files)

        # 处理上传的图片
        pic = []  # 用于存储所有图片的二进制数据
        if 'pictures[]' in request.files:  # 检查文件字段是否存在
            files = request.files.getlist('pictures[]')  # 获取所有上传的文件
            for file in files:
                if file and allowed_file(file.filename):  # 验证文件类型
                    img_data = file.read()  # 读取图片为字节流
                    pic.append(img_data)  # 将字节流加入到列表中
                else:
                    return jsonify({'error': '上传的文件无效'}), 400
        else:
            print("没有收到图片文件")

        # 创建文章数据
        shibie_return_data = {
            'TF': TF,
            'zhuangtai': zhuangtai,
            'pingjia': pingjia,
            'time':time,
        }

        # 插入文章数据
        shibie_return_id = db.insert_shibie_return(shibie_return_data)

        # 插入图片数据
        if pic:
            db.insert_shibie_return_pictures(shibie_return_id, pic)

        return jsonify({'message': '文章发布成功'}), 201

    except Exception as e:
        logging.error(f"发布文章失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


# 假设允许的文件类型是 jpg, png, jpeg
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/article/remove_pic/<int:id>', methods=['DELETE'])
def delete_article_pic(picture_id):
    try:
        # 删除文章及其关联的图片
        db.delete_article_pictures(picture_id)
        return jsonify({'message': '文章删除成功'}), 200

    except Exception as e:
        logger.error(f"删除文章失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


@app.route('/api/article/<int:id>', methods=['DELETE'])
def delete_article(id):
    try:
        # 删除文章及其关联的图片
        db.delete_article_by_id(id)
        return jsonify({'message': '文章删除成功'}), 200

    except Exception as e:
        logger.error(f"删除文章失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

@app.route('/api/update_article', methods=['POST'])
def update_article():
    try:
        # 获取表单字段
        print("111",request.form.get('article_id'))
        article_id = request.form.get('article_id')  # 文章ID，用于定位要更新的文章
        title = request.form.get('title')
        leibie = request.form.get('leibie')
        content = request.form.get('content')
        time = request.form.get('time')

        # 检查必要的字段是否存在
        if not all([article_id, title, leibie, content, time]):
            return jsonify({'error': '缺少必要的字段'}), 400

        # 打印表单数据
        print('Form data:', request.form)
        print('Files:', request.files)

        # 处理上传的图片
        pictures_data = []  # 用于存储所有图片的二进制数据
        if 'pictures[]' in request.files:  # 检查文件字段是否存在
            files = request.files.getlist('pictures[]')  # 获取所有上传的文件
            for file in files:
                if file and allowed_file(file.filename):  # 验证文件类型
                    img_data = file.read()  # 读取图片为字节流
                    pictures_data.append(img_data)  # 将字节流加入到列表中
                else:
                    return jsonify({'error': '上传的文件无效'}), 400
        else:
            print("没有收到图片文件")

        # 创建更新文章的数据
        article_data = {
            'article_id': article_id,
            'title': title,
            'leibie': leibie,
            'content': content,
            'time': time,
        }

        # 更新文章数据
        db.update_article(article_data)

        # 如果上传了新的图片，则删除旧图片并插入新图片
        if pictures_data:
            db.update_article_pictures(article_id, pictures_data)

        return jsonify({'message': '文章更新成功'}), 200

    except Exception as e:
        logging.error(f"更新文章失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500





@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # 这里可以添加额外逻辑，例如将文件路径保存到数据库中

            with open(filepath, 'rb') as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

            # 返回Base64编码的图片或者其他响应信息
            response_data = {
                'filename': filename,
                'filepath': filepath,
                'base64': encoded_string,
                'message': 'File uploaded successfully'
            }

            return jsonify(response_data), 200
        else:
            return jsonify({'error': 'File type not allowed'}), 400

    except Exception as e:
        logger.error(f"上传文件失败: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/toggle_like', methods=['POST'])
def toggle_like():
    try:
        user_id = int(request.json.get('user_id'))
        article_id = int(request.json.get('article_id'))
        like_status = int(request.json.get('like_status'))
        ip = request.remote_addr
        time = request.json.get('time')

        with db.get_cursor() as cursor:
            if like_status == 1:
                # 点赞
                # insert_sql = """
                #     INSERT INTO user_like_article (user_id, like_article_id)
                #     VALUES (?, ?)
                # """
                # cursor.execute(insert_sql, (user_id, article_id))

                insert_sql = """
                    INSERT INTO quanzi_like (time, quanzi_article_id,user_id,ip) 
                    VALUES (?, ?, ?, ?)
                """
                cursor.execute(insert_sql, (time, article_id,user_id,ip))

                # update_sql = """
                #                 UPDATE quanzi_article
                #                 SET like_count = like_count + 1
                #                 WHERE id = ?
                #             """
                # cursor.execute(update_sql, (article_id,))
            else:
                # 取消点赞
                # delete_sql = """
                #     DELETE FROM user_like_article
                #     WHERE user_id = ? AND like_article_id = ?
                # """
                # cursor.execute(delete_sql, (user_id, article_id))

                # update_sql = """
                #                 UPDATE quanzi_article
                #                 SET like_count = like_count - 1
                #                 WHERE id = ?
                #             """
                # cursor.execute(update_sql, (article_id,))

                update_sql = """
                    DELETE FROM quanzi_like 
                    WHERE user_id = ? AND quanzi_article_id = ?
                            """
                cursor.execute(update_sql, (user_id, article_id,))

            # db.commit()

        return jsonify({'message': '点赞状态更新成功'}), 200
    except Exception as e:
        logger.error(f"更新点赞状态失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


import base64

# @app.route('/api/quanzi_article_details/<int:article_id>', methods=['GET'])
# def get_article_detail(article_id):
#     with db.get_cursor() as cursor:
#         # 查询文章详情
#         cursor.execute(
#             "SELECT id, title, content, publish_date, view_count, like_count, comment_count, user_id, ip "
#             "FROM quanzi_article WHERE id = ?", (article_id,))
#         article = cursor.fetchone()
#         if not article:
#             return jsonify({'error': '文章未找到'}), 404
#
#         # 获取喜欢该文章的用户
#         cursor.execute("SELECT user_id FROM quanzi_like WHERE quanzi_article_id = ?", (article_id,))
#         like_users_ids = cursor.fetchall()
#         like_users = []
#         for user_id in like_users_ids:
#             cursor.execute("SELECT id, nickname, avatar FROM users WHERE id = ?", (user_id[0],))
#             like_users.append(cursor.fetchone())
#
#         # 获取评论
#         cursor.execute("SELECT id, user_id, comment_content, comment_date, comment_ip, quanzi_article_id FROM quanzi_comment WHERE quanzi_article_id = ?",
#                        (article_id,))
#         comments = cursor.fetchall()
#
#         # 获取文章相关的所有图片
#         cursor.execute("SELECT pic FROM quanzi_article_pic WHERE quanzi_article_id = ?", (article_id,))
#         pictures = cursor.fetchall()
#
#         # 获取评论用户信息
#         cursor.execute("SELECT user_id FROM quanzi_comment WHERE quanzi_article_id = ?", (article_id,))
#         comment_users_ids = cursor.fetchall()
#         comment_users = []
#         for user_id in comment_users_ids:
#             cursor.execute("SELECT id, nickname, avatar FROM users WHERE id = ?", (user_id[0],))
#             comment_users.append(cursor.fetchone())
#
#         # 获取评论用户头像的 Base64 编码，如果为空则填充为 None
#         comment_user_pic = []
#         for pic in comment_users:
#             if pic and pic[2]:  # 如果头像存在，则编码为Base64
#                 comment_user_pic.append(base64.b64encode(pic[2]).decode('utf-8'))
#             else:  # 如果头像为空，则添加 None
#                 comment_user_pic.append(None)
#
#         # 获取文章作者的头像
#         cursor.execute("SELECT avatar FROM users WHERE id = ?", (article[7],))
#         user_pic = cursor.fetchone()
#
#         # 检查 user_pic 是否存在，且提取字节数据进行 Base64 编码
#         if user_pic and user_pic[0]:  # 确保 user_pic 存在且不为空
#             user_pic_data = user_pic[0]  # 获取头像的字节数据
#             user_pic_base64 = base64.b64encode(user_pic_data).decode('utf-8')  # 转换为 Base64 字符串
#         else:
#             user_pic_base64 = None  # 如果没有头像，设置为 None
#
#         # 获取文章作者的昵称
#         cursor.execute("SELECT nickname FROM users WHERE id = ?", (article[7],))
#         user_nickname = cursor.fetchone()
#
#     # 将图片数据转为Base64编码字符串
#     picture_urls = []
#     for pic in pictures:
#         if pic[0]:  # 确保 pic[0] 不是 None 或空
#             picture_urls.append(base64.b64encode(pic[0]).decode('utf-8'))
#
#     # 获取喜欢该文章的用户头像的 Base64 编码
#     like_user_pic = []
#     for pic in like_users:
#         if pic[2]:
#             like_user_pic.append(base64.b64encode(pic[2]).decode('utf-8'))
#         else:
#             like_user_pic.append(None)
#
#     # 构造返回的文章数据
#     article_data = {
#         'id': int(article[0]),
#         'title': article[1],
#         'content': article[2],
#         'publish_date': article[3],
#         'view_count': article[4],
#         'like_count': article[5],
#         'comment_count': article[6],
#         'user_id': article[7],
#         'ip': article[8],
#         'user_nickname': user_nickname,
#         'user_pic': user_pic_base64,
#         'pictures': picture_urls,  # 返回图片的Base64编码字符串列表
#         'like_users': [{'user_id': user[0], 'nickname': user[1]} for user in like_users],
#         'like_users_avatar': like_user_pic,
#         'comments': [
#             {
#                 'id': comment[0],
#                 'user_id': comment[1],
#                 'comment_content': comment[2],
#                 'comment_date': comment[3],
#                 'comment_ip': comment[4],
#                 'quanzi_article_id': comment[5],
#                 'user_nickname': comment_users[idx][1],  # 添加评论用户昵称
#                 'user_avatar': comment_user_pic[idx],    # 添加评论用户头像
#             }
#             for idx, comment in enumerate(comments)
#         ]
#     }
#
#     # 返回JSON响应
#     return jsonify({'article': article_data}), 200

@app.route('/api/quanzi_article_details/<int:article_id>', methods=['GET'])
def get_article_detail(article_id):
    with db.get_cursor() as cursor:
        # 查询文章详情
        cursor.execute(
            "SELECT id, title, content, publish_date, view_count, like_count, comment_count, user_id, ip "
            "FROM quanzi_article WHERE id = ?", (article_id,))
        article = cursor.fetchone()
        if not article:
            return jsonify({'error': '文章未找到'}), 404

        # 获取喜欢该文章的用户及其信息
        cursor.execute("""
            SELECT u.id, u.nickname, u.avatar
            FROM quanzi_like l
            JOIN users u ON l.user_id = u.id
            WHERE l.quanzi_article_id = ?
        """, (article_id,))
        like_users = cursor.fetchall()

        # 获取评论信息及评论用户的详细信息
        cursor.execute("""
            SELECT c.id, c.user_id, c.comment_content, c.comment_date, c.comment_ip, c.quanzi_article_id,
                   u.nickname, u.avatar
            FROM quanzi_comment c
            JOIN users u ON c.user_id = u.id
            WHERE c.quanzi_article_id = ?
        """, (article_id,))
        comments = cursor.fetchall()

        # 获取文章相关的所有图片
        cursor.execute("SELECT pic FROM quanzi_article_pic WHERE quanzi_article_id = ?", (article_id,))
        pictures = cursor.fetchall()

        # 获取文章作者的头像和昵称
        cursor.execute("""
            SELECT u.nickname, u.avatar
            FROM users u
            WHERE u.id = ?
        """, (article[7],))
        user_info = cursor.fetchone()

        # 构造返回的文章数据
        article_data = {
            'id': int(article[0]),
            'title': article[1],
            'content': article[2],
            'publish_date': article[3],
            'view_count': article[4],
            'like_count': article[5],
            'comment_count': article[6],
            'user_id': article[7],
            'ip': article[8],
            'user_nickname': user_info[0],
            'user_pic': base64.b64encode(user_info[1]).decode('utf-8') if user_info[1] else None,
            'pictures': [base64.b64encode(pic[0]).decode('utf-8') for pic in pictures if pic[0]],
            'like_users': [{'user_id': user[0], 'nickname': user[1]} for user in like_users],
            'like_users_avatar': [
                base64.b64encode(user[2]).decode('utf-8') if user[2] else None for user in like_users
            ],
            'comments': [
                {
                    'id': comment[0],
                    'user_id': comment[1],
                    'comment_content': comment[2],
                    'comment_date': comment[3],
                    'comment_ip': comment[4],
                    'quanzi_article_id': comment[5],
                    'user_nickname': comment[6],
                    'user_avatar': base64.b64encode(comment[7]).decode('utf-8') if comment[7] else None,
                }
                for comment in comments
            ]
        }

    # 返回JSON响应
    return jsonify({'article': article_data}), 200






# 获取喜欢该文章的用户
@app.route('/api/quanzi_article/<int:article_id>/likes', methods=['GET'])
def get_article_likes(article_id):
    with db.get_cursor() as cursor:
        # 获取喜欢该文章的用户
        cursor.execute("SELECT user_id FROM quanzi_like WHERE quanzi_article_id = ?", (article_id,))
        like_users_ids = cursor.fetchall()
        users = []
        for user_id in like_users_ids:
            cursor.execute("SELECT id, nickname, avatar_url FROM users WHERE id = ?", (user_id[0],))
            users.append(cursor.fetchone())

        like_users_data = [{'user_id': user['id'], 'nickname': user['nickname'], 'avatar': user['avatar_url']} for user
                           in users]

    return jsonify({'like_users': like_users_data}), 200


# 获取所有评论
@app.route('/api/quanzi_article/<int:article_id>/comments', methods=['GET'])
def get_article_comments(article_id):
    with db.get_cursor() as cursor:
        # 获取评论
        cursor.execute("SELECT id, user_id, content, publish_date FROM quanzi_comment WHERE quanzi_article_id = ?",
                       (article_id,))
        comments = cursor.fetchall()

    comment_data = [
        {
            'id': comment['id'],
            'user_id': comment['user_id'],
            'comment_content': comment['content'],
            'comment_date': comment['publish_date']
        }
        for comment in comments
    ]

    return jsonify({'comments': comment_data}), 200


# 添加评论
@app.route('/api/quanzi_article/<int:article_id>/comment', methods=['POST'])
def add_comment(article_id):
    user_id = request.json.get('user_id')
    content = request.json.get('content')
    datetime = request.json.get('datetime')
    ip = request.remote_addr

    if not user_id or not content:
        return jsonify({'error': '用户ID或评论内容缺失'}), 400

    with db.get_cursor() as cursor:
        # 插入评论数据
        cursor.execute(
            "INSERT INTO quanzi_comment (user_id, comment_content, comment_date, quanzi_article_id,comment_ip) VALUES (?, ?, ?, ?, ?)",
            (user_id, content, datetime, article_id, ip))

        # 更新文章的评论数量
        cursor.execute("UPDATE quanzi_article SET comment_count = comment_count + 1 WHERE id = ?", (article_id,))

    return jsonify({'success': True, 'message': '评论成功'}), 201

@app.route('/api/add_quanzi_article_look', methods=['POST'])
def add_quanzi_article_look_count():
    try:
        article_id = int(request.json.get('article_id'))
        with db.get_cursor() as cursor:
            update_sql = """
                            UPDATE quanzi_article
                            SET view_count = view_count + 1
                            WHERE id = ?
                        """
            cursor.execute(update_sql, (article_id,))

        return jsonify({'message': '浏览量状态更新成功'}), 200
    except Exception as e:
        logger.error(f"更新浏览量状态失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


@app.route('/api/user_info_update_nickname/<int:user_id>', methods=['PUT'])
def user_info_update_nickname(user_id):
    try:
        # 从请求体中获取 nickname，确保是字符串类型
        nickname = request.json.get('nickname')

        # 如果 nickname 为空或不是字符串，返回400错误
        if not nickname or not isinstance(nickname, str):
            return jsonify({'error': '无效的昵称'}), 400

        with db.get_cursor() as cursor:
            update_sql = """
                UPDATE users
                SET nickname = ?
                WHERE id = ?
            """
            cursor.execute(update_sql, (nickname, user_id,))

        return jsonify({'message': '用户昵称更新成功'}), 200

    except Exception as e:
        # 错误日志信息调整为更符合实际操作
        logger.error(f"更新用户昵称失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500








@app.route('/api/user_info_update_avatar/<int:user_id>', methods=['PUT'])
def user_info_update_avatar(user_id):
    try:
        # 获取传递的 avatar 数据
        avatar = request.json.get('avatar')

        # 如果 avatar 存在，解码 Base64 数据
        if avatar:
            avatar_data = base64.b64decode(avatar)
        else:
            avatar_data = None

        # 更新数据库中的头像字段
        with db.get_cursor() as cursor:
            update_sql = """
                UPDATE users
                SET avatar = ?
                WHERE id = ?
            """
            cursor.execute(update_sql, (avatar_data, user_id,))

        return jsonify({'message': '用户头像更新成功'}), 200

    except Exception as e:
        # 错误日志信息调整为更符合实际操作
        logger.error(f"更新用户头像失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500



@app.route('/api/user_info_update_mobile/<int:user_id>', methods=['PUT'])
def user_info_update_mobile(user_id):
    try:
        mobile = request.json.get('mobile')

        if not mobile:
            return jsonify({'error': '无效的手机号'}), 400

        with db.get_cursor() as cursor:
            # 检查手机号是否已被其他用户注册
            select_sql = """
                        SELECT COUNT(*) 
                        FROM users 
                        WHERE mobile = ? AND id != ?
                    """
            cursor.execute(select_sql, (mobile, user_id))
            result = cursor.fetchone()

            # 如果有其他用户的手机号与传入的手机号相同，返回错误
            if result[0] > 0:
                return jsonify({'error': '该手机号已被其他用户注册'}), 400

        # 更新用户的手机号
        with db.get_cursor() as cursor:
            update_sql = """
                        UPDATE users
                        SET mobile = ?
                        WHERE id = ?
                    """
            cursor.execute(update_sql, (mobile, user_id))

        return jsonify({'message': '用户手机号更新成功'}), 200

    except Exception as e:
        logger.error(f"更新用户手机号失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500


# with db.get_cursor() as cursor:

@app.route('/api/user_info_update_password/<int:user_id>', methods=['PUT'])
def user_info_update_password(user_id):
    try:
        # 获取请求中的旧密码和新密码
        old = request.json.get('oldpassword')
        new = request.json.get('newpassword')

        # 检查密码是否为空
        if not old or not new:
            return jsonify({'error': '无效的密码'}), 400

        # 获取数据库中的原始密码
        with db.get_cursor() as cursor:
            get_sql = """
                        SELECT password
                        FROM users 
                        WHERE id = ?
                    """
            cursor.execute(get_sql, (user_id,))
            origin_password = cursor.fetchone()

        # 如果找到了用户且密码匹配
        if origin_password:
            if origin_password[0] == old:
                # 如果旧密码正确，更新密码
                with db.get_cursor() as cursor:
                    update_sql = """
                                UPDATE users
                                SET password = ?
                                WHERE id = ?
                            """
                    cursor.execute(update_sql, (new, user_id))

                return jsonify({'message': '密码更新成功'}), 200
            else:
                # 返回一个明确的错误信息
                return jsonify({'error': '旧密码不正确'}), 400
        else:
            return jsonify({'error': '用户未找到'}), 404

    except Exception as e:
        # 记录日志并返回内部服务器错误
        logger.error(f"更新用户密码失败: {str(e)}")
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

@app.route('/api/user_info_return_password/<int:user_id>', methods=['PUT'])
def user_info_return_password(user_id):
   try:
       # 获取请求中的手机号和新密码
       mobile = request.json.get('mobile')
       new = request.json.get('newpassword')

       # 检查手机号和新密码是否为空
       if not mobile or not new:
           return jsonify({'error': '无效的密码'}), 400

       print('mobile',type(mobile))

       # 获取数据库中的手机号
       with db.get_cursor() as cursor:
           get_sql = """
                       SELECT mobile
                       FROM users 
                       WHERE id = ?
                   """
           cursor.execute(get_sql, (user_id,))
           origin_mobile = cursor.fetchone()

       print('origim', type(origin_mobile[0]))


       # 如果找到了用户
       if origin_mobile:
           # 如果手机号为空
           if not origin_mobile[0]:
               return jsonify({'error': '用户手机号为空'}), 400

           # 如果手机号匹配
           if str(origin_mobile[0]) == mobile:
               # 如果手机号正确，更新密码
               with db.get_cursor() as cursor:
                   update_sql = """
                               UPDATE users
                               SET password = ?
                               WHERE id = ?
                           """
                   cursor.execute(update_sql, (new, user_id))

               return jsonify({'message': '密码更新成功'}), 200
           else:
               # 返回手机号不匹配的错误信息
               return jsonify({'error': '手机号不正确'}), 400
       else:
           # 如果用户不存在
           return jsonify({'error': '用户未找到'}), 404

   except Exception as e:
       # 记录日志并返回服务器内部错误
       logger.error(f"更新用户密码失败: {str(e)}")
       return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500




@app.route('/api/user_article/<int:user_id>', methods=['GET'])
def get_user_article(user_id):
    # 获取用户相关的所有 article_id
    with db.get_cursor() as cursor:
        cursor.execute("SELECT article_id FROM user_article WHERE user_id = ?", (user_id,))
        article_ids = cursor.fetchall()  # 这里返回的是一个列表，可能包含多个 article_id

    # 如果 article_ids 为空，直接返回空列表
    if not article_ids:
        return jsonify({'articles': []}), 200

    # 从查询结果中提取 article_id
    article_ids = [row[0] for row in article_ids]  # 提取每一行的第一个元素，即 article_id

    # 获取所有与这些 article_id 匹配的文章数据
    with db.get_cursor() as cursor:
        # 使用 IN 子句来匹配多个 article_id
        placeholders = ','.join('?' for _ in article_ids)
        cursor.execute(f"SELECT id, title FROM quanzi_article WHERE id IN ({placeholders}) AND status = 0", tuple(article_ids))
        articles_data = cursor.fetchall()

    return jsonify({'articles': articles_data}), 200


@app.route('/api/user_article_count/<int:user_id>', methods=['GET'])
def get_user_article_count(user_id):
    # 获取用户相关的所有 article_id
    with db.get_cursor() as cursor:
        cursor.execute("SELECT article_id FROM user_article WHERE user_id = ?", (user_id,))
        article_ids = cursor.fetchall()

        print('121', article_ids)

    # 如果没有找到相关的 article_id，返回 0
    if not article_ids:
        return jsonify({'title_count': 0}), 200

    # 提取出所有 article_id
    article_ids = [row[0] for row in article_ids]

    print('1212', article_ids)

    # 查询对应的 title 的数量
    with db.get_cursor() as cursor:
        # 构建 IN 子句的占位符
        placeholders = ','.join('?' for _ in article_ids)
        query = f"SELECT COUNT(id) FROM quanzi_article WHERE id IN ({placeholders}) AND status = 0"
        cursor.execute(query, tuple(article_ids))
        title_count = cursor.fetchone()[0]

        print(title_count)

    return jsonify({'title_count': title_count}), 200




@app.route('/api/user_like_article/<int:user_id>', methods=['GET'])
def get_user_like_article(user_id):
    # 获取用户喜欢的所有文章 ID
    with db.get_cursor() as cursor:
        cursor.execute("SELECT like_article_id FROM user_like_article WHERE user_id = ?", (user_id,))
        like_article_ids = cursor.fetchall()  # 这里返回的是一个列表，可能包含多个 like_article_id

    # 如果 like_article_ids 为空，直接返回空列表
    if not like_article_ids:
        return jsonify({'articles': []}), 200

    # 提取出所有 like_article_id
    like_article_ids = [row[0] for row in like_article_ids]  # 提取每一行的第一个元素，即 like_article_id

    # 获取所有与这些 like_article_id 匹配的文章数据
    with db.get_cursor() as cursor:
        # 使用 IN 子句来匹配多个 like_article_id
        placeholders = ','.join('?' for _ in like_article_ids)
        cursor.execute(f"SELECT id, title FROM quanzi_article WHERE id IN ({placeholders}) AND status = 0", tuple(like_article_ids))
        like_articles_data = cursor.fetchall()

    return jsonify({'articles': like_articles_data}), 200


@app.route('/api/user_like_article_count/<int:user_id>', methods=['GET'])
def get_user_like_article_count(user_id):
    with db.get_cursor() as cursor:
        cursor.execute("SELECT like_article_id FROM user_like_article WHERE user_id = ?",
                       (user_id,))
        like_article_id = cursor.fetchall()

    # 如果没有找到相关的 article_id，返回 0
    if not like_article_id:
        return jsonify({'title_count': 0}), 200

    # 提取出所有 article_id
    article_ids = [row[0] for row in like_article_id]

    # 查询对应的 title 的数量
    with db.get_cursor() as cursor:
        # 构建 IN 子句的占位符
        placeholders = ','.join('?' for _ in article_ids)
        query = f"SELECT COUNT(id) FROM quanzi_article WHERE id IN ({placeholders}) AND status = 0"
        cursor.execute(query, tuple(article_ids))
        title_count = cursor.fetchone()[0]

    return jsonify({'like_title_count': title_count}), 200


@app.route('/api/delete_user_info/<int:user_id>', methods=['DELETE'])
def delete_user_info(user_id):
    with db.get_cursor() as cursor:
        # 删除用户点赞的文章记录
        delete_sql = "DELETE FROM user_like_article WHERE user_id = ?"
        cursor.execute(delete_sql, (user_id,))

        # 删除用户发表的文章记录
        delete_sql = "DELETE FROM user_article WHERE user_id = ?"
        cursor.execute(delete_sql, (user_id,))

        # 删除用户的识别返回图片记录
        # delete_sql = """
        #     DELETE FROM shibie_return_pic
        #     WHERE shibie_return_id IN (
        #         SELECT id FROM shibie_return
        #         WHERE id IN (
        #             SELECT id FROM shibie WHERE user_id = ?
        #         )
        #     )
        # """
        # cursor.execute(delete_sql, (user_id,))

        # 删除用户的识别返回记录
        delete_sql = """
            DELETE FROM shibie_return
            WHERE id IN (
                SELECT id FROM shibie WHERE user_id = ?
            )
        """
        cursor.execute(delete_sql, (user_id,))

        # 删除用户的识别结果记录
        # delete_sql = """
        #     DELETE FROM shibie_result
        #     WHERE id IN (
        #         SELECT id FROM shibie WHERE user_id = ?
        #     )
        # """
        # cursor.execute(delete_sql, (user_id,))

        # 删除用户的识别记录
        delete_sql = "DELETE FROM shibie WHERE user_id = ?"
        cursor.execute(delete_sql, (user_id,))

        # 删除用户的评论记录
        delete_sql = "DELETE FROM quanzi_comment WHERE user_id = ?"
        cursor.execute(delete_sql, (user_id,))

        # 删除用户的文章图片记录
        # delete_sql = """
        #     DELETE FROM quanzi_article_pic
        #     WHERE quanzi_article_id IN (
        #         SELECT id FROM quanzi_article WHERE user_id = ?
        #     )
        # """
        # cursor.execute(delete_sql, (user_id,))

        # 删除用户的文章记录
        # delete_sql = "DELETE FROM quanzi_article WHERE user_id = ?"
        # cursor.execute(delete_sql, (user_id,))

        # 最后删除用户本身的记录
        delete_sql = "DELETE FROM users WHERE id = ?"
        cursor.execute(delete_sql, (user_id,))

    return {'message': 'User and related data deleted successfully'}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)