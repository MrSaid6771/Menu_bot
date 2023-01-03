import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE myfiles_teacher (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO myfiles_teacher(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO myfiles_teacher(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM myfiles_teacher
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id=1 AND Name='John'"
        sql = "SELECT * FROM myfiles_teacher WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM myfiles_teacher;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM myfiles_teacher WHERE TRUE", commit=True)

###################################this line for users #################################################################

    def user_qoshish(self, ism: str, tg_id: int, fam: str = None, username: str = None):
        # SQL_EXAMPLE = "INSERT INTO myfiles_teacher(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO users(ism, tg_id, fam, username) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(ism, tg_id, fam, username), commit=True)

    def usersCount(self):
        return self.execute("SELECT COUNT(*) FROM users", fetchone=True, commit=True)

########### lines are for foods ########################################################################################
    def select_all_foods(self):
        sql = """
        SELECT * FROM food
        """
        return self.execute(sql, fetchall=True)

    def selectFood(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id=1 AND Name='John'"
        sql = "SELECT * FROM food WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def foodAdd(self, name: str, price: int, gcatalog: str, status='active'):
        sql = """
        INSERT INTO food(name, price, gcatalog, status) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(name, price, gcatalog, status), commit=True)

    def deleteFood(self, id: int):
        sql = f"DELETE FROM food WHERE id={id}"
        return self.execute(sql, commit=True)

########### lines are for drinks ########################################################################################
    def select_all_drinks(self):
        sql = """
        SELECT * FROM drink
        """
        return self.execute(sql, fetchall=True)

    def selectDrink(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id=1 AND Name='John'"
        sql = "SELECT * FROM drink WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def drinkAdd(self, name: str, gcatalog: str, status: str, price1: int=None, price2: int=None, price3: int=None):

        sql = """
        INSERT INTO drink(name, gcatalog, status, price1, price2, price3) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(name, gcatalog, status, price1, price2, price3), commit=True)

    def deleteDrink(self, id: int):
        sql = f"DELETE FROM drink WHERE id={id}"
        return self.execute(sql, commit=True)

######################## lines are for trollers KARZINKA ################################################################
    def korzinkaAddFood(self, user_id: int, food_name: str, count: int, sum: int, status: str, catalog: str, commend: str=None):

        sql = """
        INSERT INTO karzinka(user_id, food_name, count, sum, status, catalog, commend) VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, food_name, count, sum, status, catalog, commend), commit=True)

    def korzinkaAddDrink(self, user_id: int, food_name: str, count: int, sum: int, status: str, catalog: str, types: str):

        sql = """
        INSERT INTO karzinka(user_id, food_name, count, sum, status, catalog, types) VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, food_name, count, sum, status, catalog, types), commit=True)


    def orderUpdateKarzinka(self,commend: str ,id: int):
        # SQL_EXAMPLE = "UPDATE myfiles_teacher SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
           UPDATE karzinka SET commend = ? WHERE id = ? and catalog='fastfood'
           """
        return self.execute(sql, parameters=(commend, id), commit=True)


    def selectKarzinka(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM myfiles_teacher where id=1 AND Name='John'"
        sql = "SELECT * FROM karzinka WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)


    def deleteFoodOfKarzinka(self, id : int):
        sql = f"DELETE FROM karzinka WHERE id={id}"
        return self.execute(sql, commit=True)

    def selectAllKarzinka(self):
        sql = """
        SELECT * FROM karzinka
        """
        return self.execute(sql, fetchall=True)

    def deleteAllOfKarzinka(self, id: int):
        sql = f"DELETE FROM karzinka WHERE id={id}"
        return self.execute(sql, commit=True)

    def deleteKarzinka(self, user_id: int):
        sql = f"DELETE FROM karzinka WHERE user_id={user_id}"
        return self.execute(sql, commit=True)

    def update_Types(self, types, id: int):
        # SQL_EXAMPLE = "UPDATE myfiles_teacher SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
           UPDATE karzinka SET types = ? WHERE id = ?
           """
        return self.execute(sql, parameters=(types, id), commit=True)

    ####################### for orders #################################################################################

    def orderAdd(self, user_id: int, name: str, price: int ,commend: str, count: int, catalog: str, type: str, user_name: str):
        # SQL_EXAMPLE = "INSERT INTO myfiles_teacher(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO orders(user_id, name, price, commend, count, catalog, type, user_name) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, name, price, commend, count, catalog, type, user_name), commit=True)

    def selectOrder(self):
        sql = """
        SELECT * FROM orders
        """
        return self.execute(sql, fetchall=True)

    def deleteOrders(self, user_id: int):
        sql = f"DELETE FROM orders WHERE user_id={user_id}"
        return self.execute(sql, commit=True)


####################### For arxiv ######################################################################################
    def addForArxiv(self, user_id: int, ordername: str, count: int, price: int, types: str, catalog: str,day:str, month:str):

        sql = """
        INSERT INTO arxiv(user_id, ordername, count, price, types, catalog, day, month) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, ordername, count, price, types, catalog, day, month), commit=True)


    def calculateArxivDay(self, day: int):
        sql = f"""
        SELECT SUM(price) FROM arxiv WHERE day={day}
        """
        return self.execute(sql, fetchone=True)

    def calculateArxivMonth(self, month: int):
        sql = f"""
        SELECT SUM(price) FROM arxiv WHERE month={month}
        """
        return self.execute(sql, fetchone=True)

def logger(statement):
    print(f"""
    _____________________________________________________
    Executing:
    {statement}
    _____________________________________________________
""")
