import psycopg2
from passlib.hash import sha256_crypt
class Database(object):
    def __init__(self):
        try:
            self.connection = psycopg2.connect(database="stackoverflow", user="postgres",host="localhost",password="wyco2018!",port="5432")
            self.cursor = self.connection.cursor()
            self.connection.autocommit = True
            print("successfully connects to database")
        except:
            print("Failed to connect to database")

    #creates table users in the database
    def create_table_users(self):
        query = "CREATE TABLE users(Id serial PRIMARY KEY,fullName varchar(25),\
        userName varchar(15),email varchar(25),password text)"
        self.cursor.execute(query)  
        # self.connection.commit()
        print("table users created successfully")
        # self.connection.close()  

    #inserts users into the database
    def save_users_database(self,fullname,username,email,password):
        query = "INSERT INTO users(fullName,userName,email,password) \
        VALUES (%s,%s,%s,%s)"  
        new_password = sha256_crypt.encrypt(password) 
        self.cursor.execute(query,(fullname,username,email,new_password))
        # self.connection.commit()
         

    #verify login
    def verify_login(self,username,password):
        query = "SELECT username,password FROM users WHERE username = %s"
        self.cursor.execute(query,(username,))
        rows = self.cursor.fetchall()
        # import pdb; pdb.set_trace()
        if rows:
            if sha256_crypt.verify(password, rows[1][1]):
                return "user successfully logged in"
            return "Login failed,check your password and username"
        return "user with the above username doesnt exist in the database"

        

    #creates table questions in the database
    def create_table_questions(self):
        query = "CREATE TABLE questions(questionId serial PRIMARY KEY,question text,\
        description text, userId int, date_added date, FOREIGN KEY (userId) REFERENCES users (Id))"
        self.cursor.execute(query)  
        # self.connection.commit()
        print("table questions created successfully")
        # self.connection.close()  

    #inserts questions into the database
    def insert_questions_database(self,question,description,userId,date_added):
        query = "INSERT INTO questions(question,description,userId,date_added) \
        VALUES (%s,%s,%s,%s)"   
        self.cursor.execute(query,(question,description,userId,date_added))
        self.connection.commit()
        print("question successfully added")
        self.connection.close()

    #fetches all questions from the database
    def fetch_questions_database(self):
        self.cursor.execute("SELECT * from questions")
        rows = self.cursor.fetchall()
        return rows  
        # self.connection.close()

    #fetch a question from the database
    def fetch_a_question_database(self,questionId):
        query = "SELECT * from questions where questionId = %s"
        self.cursor.execute(query,[questionId])
        rows = self.cursor.fetchall()
        return rows  
        # self.connection.close() 


    #creates table answers in the database
    def create_table_answers(self):
        query = "CREATE TABLE answers(answerId serial PRIMARY KEY,questionId int,\
        answer text, userId int, date_added date,FOREIGN KEY (questionId) REFERENCES questions (questionId))"
        self.cursor.execute(query)  
        # self.connection.commit()
        print("table answers created successfully")
        # self.connection.close() 






          


 
  
if __name__ == '__main__':
    my_database = Database()
