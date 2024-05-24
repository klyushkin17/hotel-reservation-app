import psycopg2


class ConnectionManager:
    def __init__(self, user):
        self.__dbname = "hotelDatabase"
        self.user = user
        self.__password = "12345678"
        self.__host = "localhost"

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.__dbname,
                user=self.user,
                password=self.__password,
                host=self.__host,
                client_encoding="utf8",
            )
            print("Соединение установлено")
            return self.connection
        except psycopg2.Error as e:
            print(f'Ошибка подключения к базе данных: {e}')

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()