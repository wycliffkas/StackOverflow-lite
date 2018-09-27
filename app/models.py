from flask import Response,json
import psycopg2
from passlib.hash import sha256_crypt
from datetime import date
from flask import jsonify
# from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from urllib.parse import urlparse
date_added = date.today().strftime("%d/%m/%Y")


# import os
# database_url = os.environ.get('DATABASE_URL')

class DatabaseModel:
    def __init__(self, database_url):
        """database connection"""
        # # parsed_url = postgres://vfrocsnlqepiuy:5f91140a1e8a258608fb65ebc6065718fa80867a763c68733774a1df91735551@ec2-174-129-18-98.compute-1.amazonaws.com:5432/d2abra34kiqavt
        # parsed_url = urlparse(database_url)
        # database = parsed_url.path[1:]
        # username = parsed_url.username
        # hostname = parsed_url.hostname
        # password = parsed_url.password
        # port = parsed_url.port
        # # import pdb; pdb.set_trace()
        
        # self.connection = psycopg2.connect(database=database,user=username,password=password,host=hostname,port=port)
        self.connection = psycopg2.connect("postgres://vfrocsnlqepiuy:5f91140a1e8a258608fb65ebc6065718fa80867a763c68733774a1df91735551@ec2-174-129-18-98.compute-1.amazonaws.com:5432/d2abra34kiqavt")
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

        query = """CREATE TABLE IF NOT EXISTS users(
                Id SERIAL PRIMARY KEY,
                fullName varchar(25) NOT NULL,
                userName varchar(15) NOT NULL,
                email varchar(25) NOT NULL,
                password text NOT NULL)"""

        query2 = """CREATE TABLE IF NOT EXISTS questions(
                questionId SERIAL PRIMARY KEY,
                question text NOT NULL,
                description text NOT NULL,
                author varchar(15),
                date_added date NOT NULL)"""

        query3 = """CREATE TABLE IF NOT EXISTS answers(
                answerId SERIAL PRIMARY KEY,
                questionId int NOT NULL,
                answer text NOT NULL,
                author varchar(15),
                date_added date NOT NULL,
                status varchar(15),
                vote int DEFAULT 0, 
                FOREIGN KEY (questionId) REFERENCES questions (questionId) )"""

        query4 = """CREATE TABLE IF NOT EXISTS comments(
                Id SERIAL PRIMARY KEY,
                comment text,
                answerid int,
                date_added date NOT NULL)"""                

        #create table users
        self.cursor.execute(query)
        #create table questions
        self.cursor.execute(query2)
        #create table answers
        self.cursor.execute(query3)
        #create table comments
        self.cursor.execute(query4)

    #inserts users into the database
    def save_users_database(self,fullname,username,email,password):
        query = "SELECT id FROM users WHERE username = %s"
        self.cursor.execute(query,[username])
        user_with_username_specified = self.cursor.fetchall()
        if user_with_username_specified:
            return jsonify({'message':'Pick another username, user already exits'}),400
        else:
            query = "INSERT INTO users(fullName,userName,email,password) VALUES (%s,%s,%s,%s)"  
            new_password = sha256_crypt.hash(password) 
            self.cursor.execute(query,(fullname,username,email,new_password))
            query2 = "select * from users ORDER BY id Desc LIMIT 1"
            self.cursor.execute(query2)
            users = self.cursor.fetchall()
            for user in users:
                user_object = {
                        'Id': user[0],
                        'fullname' : user[1],
                        'username' : user[2],
                        'email': user[3]
                    }            
            return jsonify(user_object),201
            
    #verify login
    def verify_login(self,username,password):
        query = "SELECT username,password FROM users WHERE username = %s"
        self.cursor.execute(query,(username,))
        rows = self.cursor.fetchall()
        if rows:
            if sha256_crypt.verify(password, rows[0][1]) and rows[0][0] == username:
                # access_token = create_access_token(identity=username)

                # results = {'access_token':access_token, 'message':'User successfully logged in'}
                results = {'message':'User successfully logged in'}
                
                return jsonify(results),200
            return jsonify({'message':'Login failed,check your password'}),400
        return jsonify({'message':'User with the above username doesnt exist in the database'}),400

    #inserts questions into the database
    def insert_questions_database(self,question,description):
        pass
        # author = get_jwt_identity()
        # query = "INSERT INTO questions(question,description,author,date_added) VALUES (%s,%s,%s,%s)"   
        # self.cursor.execute(query,(question,description,author,date_added))
        # query2 = "SELECT * FROM questions ORDER BY questionid Desc Limit 1"
        # self.cursor.execute(query2)
        # questions = self.cursor.fetchall()
        # for question in questions:
        #     questions_object = {
        #             'questionId': question[0],
        #             'question' : question[1],
        #             'description' : question[2],
        #             'author': question[3],
        #             'date_added': question[4]
        #         }
        # return questions_object

    #fetches all questions from the database
    def fetch_questions_database(self):
        query = "SELECT questionid,question,description,author,date_added FROM questions"
        self.cursor.execute(query)
        questions = self.cursor.fetchall()
        if questions:
            results = []
            for question in questions:
                question = {
                    'questionId': question[0],
                    'question' : question[1],
                    'description' : question[2],
                    'author': question[3],
                    'date_added': question[4]
                    }
                results.append(question)

            return jsonify(results),201
        else:
           return jsonify({'message':'No questions added yet'}),404


    #fetch a question from the database
    def fetch_a_question_database(self,questionId):

        query = "SELECT questionid FROM questions WHERE questionid = %s"
        self.cursor.execute(query,[questionId])
        questions = self.cursor.fetchall()        

        if questions:
            query = "SELECT questionid FROM answers WHERE questionid = %s"
            self.cursor.execute(query,[questionId])
            answers = self.cursor.fetchall()    
            if answers: 
                query = "SELECT questions.questionid,questions.description,answers.answer,answers.status,answers.vote\
                FROM questions INNER JOIN answers ON questions.questionid = answers.questionid\
                where questions.questionid = %s"
                self.cursor.execute(query,[questionId])
                questions = self.cursor.fetchall()

                answers = []
                answer = {}
                
                for row in questions:
                    answer.update({'answer':row[2]})
                    answer.update({'status':row[3]})
                    answer.update({'vote':row[4]})
                    answers.append(answer)
                question_object = {
                        "question id": questions[0][0],
                        "question": questions[0][1],
                        "description":questions[0][2],
                        "answers":answers
                }
                return jsonify(question_object),201     
            else:
                query = "SELECT questionid,question,description,author FROM questions WHERE questionid = %s"
                self.cursor.execute(query,[questionId])
                questions = self.cursor.fetchall()         
                question_object = {
                        "question Id": questions[0][0],
                        "question": questions[0][1],
                        "description": questions[0][2],
                        "author": questions[0][3],
                        "answers": "No answers"
                }
                return jsonify(question_object),201  
        else:
            return jsonify({'message':'Question deosnt exist in the database'}),404
                     


    #deletes questions from the database
    def delete_question(self,questionId):
        query = "SELECT * FROM questions where questionId = %s"
        self.cursor.execute(query,[questionId])
        rows = self.cursor.fetchall()
        if rows:
            # user = get_jwt_identity()
            query = "SELECT author FROM questions where questionId = %s"
            self.cursor.execute(query,[questionId])
            question_author = self.cursor.fetchall()
            

            # if question_author[0][0] == user:
            #     query = "DELETE FROM questions WHERE questionId = %s" 
            #     self.cursor.execute(query,[questionId,])
            #     return jsonify({'message':'question was succesfully deleted'}),201
            # else:
            #     return jsonify({'message':'its only the questions author who can delete a question'}),400
        return jsonify({'message':'Question with the specified QuestionId doesnt exist in the database'}),404

    #questions asked by the user
    def questions_asked_user_database(self):
        pass
        # user = get_jwt_identity()
        # query = "SELECT questionid,question,description,author,date_added FROM questions WHERE author= %s"
        # self.cursor.execute(query,(user,))
        # questions = self.cursor.fetchall()
        # if questions:

        #     results = {}
        #     for question in questions:
        #         results[question[0]] = {
        #             'questionId': question[0],
        #             'question' : question[1],
        #             'description' : question[2],
        #             'userid': question[3],
        #             'date_added': question[4]
        #             }

        #     return jsonify(results),201
        # else:
        #    return jsonify({'message':'No Questions asked by current user'}),404
           

    #saves answer into the database
    def save_answer(self,questionId,answer):
        pass
        # query = "SELECT questionId FROM questions where questionId = %s"
        # self.cursor.execute(query,[questionId])
        # question_with_id = self.cursor.fetchall()        
        
        # if question_with_id:
        #     author = get_jwt_identity()                
        #     query = ('''INSERT INTO answers (answer,questionId,author,date_added)VALUES (%s,%s,%s,%s)''')
        #     self.cursor.execute(query,(answer,questionId,author,date_added))
            
        #     query = ('''select answerid,questionid,answer,author,date_added from answers ORDER BY answerid DESC LIMIT 1''')
        #     self.cursor.execute(query)
        #     answers = self.cursor.fetchall()  

        #     response = {
        #         'Answer Id': answers[0][0],
        #         'Answer': answers[0][2],
        #         'Question Id':answers[0][1],
        #         'Author':answers[0][3],
        #         'Date Added': answers[0][4],
        #         'Message':"Answer successfully added"  
        #     }
        #     return jsonify(response),201
        # return jsonify({'message':'No question with the specified Question Id in the database'}),404

    #update answer in the database
    def update_answer_database(self,questionId,answer,answerId):
        pass
        # user = get_jwt_identity()
        # query = "SELECT author FROM answers where answerId = %s"
        # self.cursor.execute(query,[answerId])
        # answer_author = self.cursor.fetchall() 
        # if answer_author:
        #     if answer_author[0][0] == user:
        #         query = ('''UPDATE answers set answer = %s where answerid = %s''')
        #         self.cursor.execute(query,(answer,answerId))
        #         return jsonify({'Message':'answer successfully updated'}),201
        #     else:
        #         return jsonify({'Message':'Only author can update an answer'}),400
        # return jsonify({'message':'Wrong Id, please check the question or Answer ID'}),404

        

    #mark answer as prefered in the database
    def mark_prefered(self,answerId):
        query = ('''UPDATE answers set status = %s where answerid = %s''')
        self.cursor.execute(query,('prefered',answerId))
        return {"Message":"answer successfully updated"}
    

    #upvote or downvote answer in the database
    def vote_answer(self,answerId,vote):
        vote_answer = vote.lower()
        if vote_answer == "yes":
            query = "SELECT vote FROM answers where answerId = %s"
            self.cursor.execute(query,[answerId])
            current_vote = self.cursor.fetchall()  
            new_vote = current_vote[0][0] + 1
            
            query = ('''UPDATE answers set vote = %s where answerid = %s''')
            self.cursor.execute(query,(new_vote,answerId))
            return jsonify({'message':'Answer successfully up voted'}),201
        else:
            query = "SELECT vote FROM answers where answerId = %s"
            self.cursor.execute(query,[answerId])
            current_vote = self.cursor.fetchall()  
            new_vote = current_vote[0][0] - 1
            
            query = ('''UPDATE answers set vote = %s where answerid = %s''')
            self.cursor.execute(query,(new_vote,answerId))
            return jsonify({'message':'Answer successfully down voted'}),201

    def create_tables(self):
        query = """CREATE TABLE IF NOT EXISTS users(
                Id SERIAL PRIMARY KEY,
                fullName varchar(25) NOT NULL,
                userName varchar(15) NOT NULL,
                email varchar(25) NOT NULL,
                password text NOT NULL)"""

        query2 = """CREATE TABLE IF NOT EXISTS questions(
                questionId SERIAL PRIMARY KEY,
                question text NOT NULL,
                description text NOT NULL,
                author varchar(15),
                date_added date NOT NULL)"""

        query3 = """CREATE TABLE IF NOT EXISTS answers(
                answerId SERIAL PRIMARY KEY,
                questionId int NOT NULL,
                answer text NOT NULL,
                author varchar(15),
                date_added date NOT NULL,
                status varchar(15),
                vote int DEFAULT 0, 
                FOREIGN KEY (questionId) REFERENCES questions (questionId) )"""

        query4 = """CREATE TABLE IF NOT EXISTS comments(
                Id SERIAL PRIMARY KEY,
                comment text,
                answerid int,
                date_added date NOT NULL)"""                

        #create table users
        self.cursor.execute(query)
        #create table questions
        self.cursor.execute(query2)
        #create table answers
        self.cursor.execute(query3)
        #create table comments
        self.cursor.execute(query4)

    def tear_down(self):
        self.cursor.execute("DROP TABLE users;")
        self.cursor.execute("DROP TABLE answers;")
        self.cursor.execute("DROP TABLE questions;")

        
# class TearDownDatabase:
#     @classmethod
#     def tear_down(cls, database_url):
#         parsed_url = urlparse(database_url)
#         database = parsed_url.path[1:]
#         username = parsed_url.username
#         hostname = parsed_url.hostname
#         password = parsed_url.password
#         port = parsed_url.port
#         connection = psycopg2.connect(database=database,user=username,password=password,host=hostname,port=port)
#         cursor = connection.cursor()
#         connection.autocommit = True

#         # cursor.execute("SET FOREIGN_KEY_CHECKS=0")
#         cursor.execute("DELETE FROM users;")
#         cursor.execute("DELETE FROM answers;")
#         cursor.execute("DELETE FROM questions;")
#         # cursor.execute("SET FOREIGN_KEY_CHECKS=1")        















































