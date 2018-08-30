from flask import Response,json
import psycopg2
from passlib.hash import sha256_crypt
from datetime import date
from flask import jsonify
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity

class Database(object):
    def __init__(self):
        try:
            self.connection = psycopg2.connect(database="stackoverflow", user="postgres",host="localhost",password="wyco2018!",port="5432")
            self.cursor = self.connection.cursor()
            self.connection.autocommit = True
            print("successfully connects to database")
        except:
            print("Failed to connect to database")
    date_added = date.today().strftime("%d/%m/%Y")
    #creates table users in the database
    def create_table_users(self):
        query = "CREATE TABLE users(Id serial PRIMARY KEY,fullName varchar(25),\
        userName varchar(15),email varchar(25),password text,role varchar)"
        self.cursor.execute(query)  
        # self.connection.commit()
        print("table users created successfully")
        # self.connection.close()  

    #inserts users into the database
    def save_users_database(self,fullname,username,email,password):
        query = "SELECT id FROM users WHERE username = %s"
        self.cursor.execute(query,[username])
        user_with_username_specified = self.cursor.fetchall()
        if user_with_username_specified:
            return "pick another username, user already exits"
        else:
            query = "INSERT INTO users(fullName,userName,email,password) \
            VALUES (%s,%s,%s,%s)"  
            new_password = sha256_crypt.encrypt(password) 
            self.cursor.execute(query,(fullname,username,email,new_password))
            return "user successfully registered"
         

    #verify login
    def verify_login(self,username,password):
        query = "SELECT username,password FROM users WHERE username = %s"
        self.cursor.execute(query,(username,))
        rows = self.cursor.fetchall()
        if rows:
            if sha256_crypt.verify(password, rows[1][1]):
                access_token = create_access_token(identity=username)

                results = {'access_token':access_token,'message':'user successfully logged in'}
                return jsonify(results), 200
                # return Response(json.dumps(results), 201, mimetype="application/json")
                # return access_token
                # # return "message user successfully logged in" 
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
        self.cursor.execute("SELECT * FROM questions")
        rows = self.cursor.fetchall()
        return rows  
        # self.connection.close()

    #fetch a question from the database
    def fetch_a_question_database(self,questionId):
        query = "SELECT * FROM questions where questionId = %s"
        self.cursor.execute(query,[questionId])
        rows = self.cursor.fetchall()
        return rows  
        # self.connection.close() 


    #deletes questions from the database
    def delete_question(self,questionId):
        query = "SELECT * FROM questions where questionId = %s"
        self.cursor.execute(query,[questionId])
        rows = self.cursor.fetchall()
        if rows:
            query = "DELETE FROM questions WHERE questionId = %s" 
            self.cursor.execute(query,[questionId,])
            self.connection.commit()
            return "question successfully deleted"
        return "Question with the specified QuestionId doesnt exist in the database"


    #creates table answers in the database
    def create_table_answers(self):
        query = "CREATE TABLE answers(answerId serial PRIMARY KEY,questionId int,\
        answer text, userId int, date_added date,FOREIGN KEY (questionId) REFERENCES questions (questionId))"
        self.cursor.execute(query)  
        # self.connection.commit()
        print("table answers created successfully")
        # self.connection.close() 

    #saves answer into the database
    def save_answer(self,questionId,answer,userId):
        query = "SELECT id FROM users WHERE id = %s"
        self.cursor.execute(query,[userId])
        user_with_id = self.cursor.fetchall()

        query = "SELECT questionId FROM questions where questionId = %s"
        self.cursor.execute(query,[questionId])
        question_with_id = self.cursor.fetchall()        
        
        if question_with_id:
            if user_with_id:
                query = ('''INSERT INTO answers (answer,questionId,userId,date_added)VALUES (%s,%s,%s,%s)''')
                self.cursor.execute(query,(answer,questionId,userId,self.date_added))
                return "answer successfully added"
            return "No user with specified user Id"
        return "No question with specified Question Id in the database"

    #update answer in the database
    def update_answer_database(self,questionId,answer,answerId):
        query = ('''UPDATE answers set answer = %s where answerid = %s''')
        self.cursor.execute(query,(answer,answerId))
        return "answer successfully updated"

  
if __name__ == '__main__':
    my_database = Database()
