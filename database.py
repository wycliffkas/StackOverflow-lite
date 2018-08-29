import psycopg2
class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(database="stackoverflow", user="postgres",host="localhost",password="wyco2018!",port="5432")
            self.cursor = self.connection.cursor()
            print("successfully connects to database")
        except:
            print("Failed to connect to database")

    #creates table users in the database
    def create_table_users(self):
        query = "CREATE TABLE users(Id serial PRIMARY KEY,fullName varchar(25),\
        userName varchar(15),email varchar(25),password text)"
        self.cursor.execute(query)  
        self.connection.commit()
        print("table users created successfully")
        self.connection.close()  

    #inserts users into the database
    def insert_users_database(self,fullname,userName,email,password):
        query = "INSERT INTO users(fullName,userName,email,password) \
        VALUES (%s,%s,%s,%s)"   
        self.cursor.execute(query,(fullname,userName,email,password))
        self.connection.commit()
        print("user successfully added")
        self.connection.close()  

    #fetches users from the database
    def fetch_users_database(self):
        self.cursor.execute("SELECT * from users")
        rows = self.cursor.fetchall()
        self.connection.close()
        return rows

    #creates table questions in the database
    def create_table_questions(self):
        query = "CREATE TABLE questions(questionId serial PRIMARY KEY,question text,\
        description text, userId int, answers text, date_added date, FOREIGN KEY (userId) REFERENCES users (Id))"
        self.cursor.execute(query)  
        self.connection.commit()
        print("table questions created successfully")
        self.connection.close()  

    #inserts questions into the database
    def insert_questions_database(self,question,description,userId,date_added):
        query = "INSERT INTO questions(question,description,userId,date_added) \
        VALUES (%s,%s,%s,%s)"   
        self.cursor.execute(query,(question,description,userId,date_added))
        self.connection.commit()
        print("question successfully added")
        self.connection.close()

    #fetches questions from the database
    def fetch_questions_database(self):
        self.cursor.execute("SELECT * from questions")
        rows = self.cursor.fetchall()
        return rows  
        self.connection.close()
        

         


    #creates table answers in the database
    def create_table_answers(self):
        query = "CREATE TABLE answers(answerId serial PRIMARY KEY,questionId int,\
        answer text, userId int, date_added date,FOREIGN KEY (questionId) REFERENCES questions (questionId))"
        self.cursor.execute(query)  
        self.connection.commit()
        print("table answers created successfully")
        self.connection.close()     


          

# cur.fetchall()
 
  
if __name__ == '__main__':
    my_database = Database()