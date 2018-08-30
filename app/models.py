from database import Database
my_database = Database()
from datetime import date


class Users(object):
    #add users
    def save_users(self,fullname,username,email,password):
        return my_database.save_users_database(fullname,username,email,password)
        
    #verify users   
    def login_user(self,username,password):
        msg = my_database.verify_login(username,password)
        return msg
        
        

class Questions(object):
    def __init__(self):
        self.database_questions = my_database.fetch_questions_database()
        self.questions = {}



        for question in self.database_questions:
            self.questions[question[0]] = {
                'questionId': question[0],
                'question' : question[1],
                'description' : question[2],
                'userid': question[3],
                'date_added': question[4]
                }


    date_added = date.today().strftime("%d/%m/%Y")


    #add questions
    def save_questions(self,question,description,userId):
        questions_object = {
            'question':question,
            'description': description,
            'userId':userId,
            'date_added':self.date_added}
        my_database.insert_questions_database(question,description,userId,self.date_added)
        return questions_object
            
    #fetch all questions
    def fetch_all_questions(self):
        return self.questions


    #fetch a question
    def fetch_a_question(self,questionId):
        questionId = int(questionId)
        question = my_database.fetch_a_question_database(questionId)
        return question

    #delete a question
    def delete_question(self,questionId):
        message = my_database.delete_question(questionId)
        return message


class Answers(object):

    #save an answer
    def save_answer(self,questionId,answer,userId):
        message = my_database.save_answer(questionId,answer,userId)
        return message

    #update answer
    def update_answer(self, questionId,answer,answerId):
        message = my_database.update_answer_database(questionId,answer,answerId)
        return message


       





  






    
