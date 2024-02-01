import sqlite3

class Database:
    def __init__(self, name: str):
        print(f"Iniciando conexion en la db_name: {name}")
        self.name = name

    def _get_db_connection(self):
        conn = sqlite3.connect(self.name)
        conn.row_factory = sqlite3.Row
        return conn

    def query_all(self, query: str):
        try:
            conn = self._get_db_connection()
            query_result = conn.execute(query).fetchall()
            conn.close()
            return query_result
        except Exception as e:
            print(f"Ocurrio un error al realizar la consulta, error:{e}")
            raise
    
    def query_where(self, query: str, params: tuple):
        try:
            conn = self._get_db_connection()
            query_result = conn.execute(query, params).fetchall()
            conn.close()
            return query_result
        except Exception as e:
            print(f"Ocurrio un error al realizar la consulta, error:{e}")
            raise
    
    def insert(self, query: str, params: tuple):
        try:
            conn = self._get_db_connection()
            conn.execute(query, params)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Ocurrio un error al intentar insertar los registos, error: {e}")
            raise

class User(Database):
    def get_user_by_username(self, username: str):
        """
            Busca un usuario en la base de datos por username
            Args: Username -> str
        """
        try:
            query = "SELECT * FROM users WHERE users.username == ?"
            params = (username,)
            user = self.query_where(query, params)
            return user
        except Exception as e:
            raise

    def create_user(self, username: str, password: str):
        try:
            query = "INSERT INTO users (username, password) VALUES (?,?)"
            params = (username, password)
            self.insert(query, params)
        except Exception as e:
            raise

class Post(Database):
    def get_all_posts(self):
        try:
            query = "SELECT * FROM posts"
            posts = self.query_all(query)
            return posts
        except Exception as e:
            raise

    def get_posts_by_id(self, id: str):
        try:
            query = "SELECT * FROM posts WHERE posts.id == ?"
            params = (id,)
            post = self.query_where(query, params)
            return post
        except Exception as e:
            raise

    def get_posts_by_title(self, title: str):
        try:
            query = "SELECT * FROM posts WHERE posts.titulo LIKE ?"
            params = (f"%{title}%",)
            posts = self.query_where(query, params)
            return posts
        except Exception as e:
            raise

    def create_post(self, autor: str, titulo: str, contenido: str):
        try:
            query = "INSERT INTO posts (autor, titulo, contenido) VALUES (?,?,?)"
            params = (autor, titulo, contenido)
            self.insert(query, params)
        except Exception as e:
            raise
        