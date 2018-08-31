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
        userName varchar(15),email varchar(25),password text)"
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
            return {"Message":"pick another username, user already exits"}
        else:
            query = "INSERT INTO users(fullName,userName,email,password) \
            VALUES (%s,%s,%s,%s)"  
            new_password = sha256_crypt.encrypt(password) 
            self.cursor.execute(query,(fullname,username,email,new_password))
            return {"Message":"user successfully registered"}
         

    #verify login
    def verify_login(self,username,password):
        query = "SELECT username,password FROM users WHERE username = %s"
        self.cursor.execute(query,(username,))
        rows = self.cursor.fetchall()
        if rows:
            if sha256_crypt.verify(password, rows[0][1]):
                access_token = create_access_token(identity=username)

                results = {'access_token':access_token,'message':'user successfully logged in'}
                username = get_jwt_identity()
                return jsonify(results), 200
                # return Response(json.dumps(results), 201, mimetype="application/json")
                # return access_token
                # # return "message user successfully logged in" 
            return {"Message":"Login failed,check your password and username"}
        return {"Message":"user with the above username doesnt exist in the database"}



        

    #creates table questions in the database
    def create_table_questions(self):
        query = "CREATE TABLE questions(questionId serial PRIMARY KEY,question text,\
        description text, author varchar(15), date_added date)"
        self.cursor.execute(query)  
        # self.connection.commit()
        print("table questions created successfully")
        # self.connection.close()  

    #inserts questions into the database
    def insert_questions_database(self,question,description,date_added):
        author = get_jwt_identity()
        query = "INSERT INTO questions(question,description,author,date_added) \
        VALUES (%s,%s,%s,%s)"   
        self.cursor.execute(query,(question,description,author,date_added))
        self.connection.commit()

        questions_object = {
            'question':question,
            'description': description,
            'author': author,
            'date_added':self.date_added
            }
        return questions_object

    #fetches all questions from the database
    def fetch_questions_database(self):
        self.cursor.execute("SELECT * FROM questions")
        rows = self.cursor.fetchall()
        return rows  


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
                return question_object     
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
                return question_object 
        else:
            return {"Error!":"Question deosnt exist in the database"} 
                     

        


    #deletes questions from the database
    def delete_question(self,questionId):
        query = "SELECT * FROM questions where questionId = %s"
        self.cursor.execute(query,[questionId])
        rows = self.cursor.fetchall()
        if rows:
            user = get_jwt_identity()
            query = "SELECT author FROM questions where questionId = %s"
            self.cursor.execute(query,[questionId])
            question_author = self.cursor.fetchall()
            

            if question_author[0][0] == user:
                query = "DELETE FROM questions WHERE questionId = %s" 
                self.cursor.execute(query,[questionId,])
                self.connection.commit()
                return {"message":"question was succesfully deleted"}
            else:
                return {"message":"its only the questions author who can delete a question"}
        return {"message":"Question with the specified QuestionId doesnt exist in the database"}

    #questions asked by the user
    def questions_asked_user_database(self):
        user = get_jwt_identity()
        query = "SELECT questionid,question,description,author,date_added FROM questions WHERE author= %s"
        self.cursor.execute(query,(user,))
        questions = self.cursor.fetchall()
        if questions:

            results = {}
            for question in questions:
                results[question[0]] = {
                    'questionId': question[0],
                    'question' : question[1],
                    'description' : question[2],
                    'userid': question[3],
                    'date_added': question[4]
                    }

            return results
        else:
           return {"message":"No Questions asked by current user"}
           
           
    #creates table answers in the database
    def create_table_answers(self):
        query = "CREATE TABLE answers(answerId serial PRIMARY KEY,questionId int,\
        answer text, author varchar(15), date_added date, status varchar(15),vote int DEFAULT 0, FOREIGN KEY (questionId) REFERENCES questions (questionId))"
        self.cursor.execute(query)  
        # self.connection.commit()
        print("table answers created successfully")
        # self.connection.close() 

    #saves answer into the database
    def save_answer(self,questionId,answer):
        query = "SELECT questionId FROM questions where questionId = %s"
        self.cursor.execute(query,[questionId])
        question_with_id = self.cursor.fetchall()        
        
        if question_with_id:
            author = get_jwt_identity()                
            query = ('''INSERT INTO answers (answer,questionId,author,date_added)VALUES (%s,%s,%s,%s)''')
            self.cursor.execute(query,(answer,questionId,author,self.date_added))
            response = {
                "Answer": answer,
                "Question Id":questionId,
                "Author":author,
                "Message":"Answer successfully added",
                "Date Added": self.date_added
            }
            return response
        return {"message":"No question with the specified Question Id in the database"}

    #update answer in the database
    def update_answer_database(self,questionId,answer,answerId):
        user = get_jwt_identity()
        query = "SELECT author FROM answers where answerId = %s"
        self.cursor.execute(query,[answerId])
        answer_author = self.cursor.fetchall() 
        if answer_author:
            if answer_author[0][0] == user:
                query = ('''UPDATE answers set answer = %s where answerid = %s''')
                self.cursor.execute(query,(answer,answerId))
                return {"Message":"answer successfully updated"}
            else:
                return {"Message":"Only author can update an answer"}
        return {"Message":"please check the question or Answer ID"}

        

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
            return {"message":"Answer up voted"}
        else:
            query = "SELECT vote FROM answers where answerId = %s"
            self.cursor.execute(query,[answerId])
            current_vote = self.cursor.fetchall()  
            new_vote = current_vote[0][0] - 1
            
            query = ('''UPDATE answers set vote = %s where answerid = %s''')
            self.cursor.execute(query,(new_vote,answerId))
            return {"message":"Answer down voted"}



  

  
if __name__ == '__main__':
    my_database = Database()
