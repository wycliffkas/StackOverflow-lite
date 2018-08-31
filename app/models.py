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
        
    def add_user_account(self, fullname,username,email,password):
        return my_database.save_users_database(fullname,username,email,password)

        

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
    def save_questions(self,question,description):
        return my_database.insert_questions_database(question,description,self.date_added)

        
            
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

    #questions asked by a user
    def questions_asked_user(self): 
        return my_database.questions_asked_user_database()      



class Answers(object):

    #save an answer
    def save_answer(self,questionId,answer):
        message = my_database.save_answer(questionId,answer)
        return message

    #update answer
    def update_answer(self, questionId,answer,answerId):
        message = my_database.update_answer_database(questionId,answer,answerId)
        return message

    #mark answer prefered 
    def mark_prefered(self,answerId):
        message = my_database.mark_prefered(answerId)
        return message


    #vote answer
    def vote_answer(self,answerId,vote):
        return my_database.vote_answer(answerId,vote)
        



       





  






    
