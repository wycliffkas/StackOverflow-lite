from database import Database
my_database = Database()
from datetime import date

class Users(object):
    #add users
    def save_users(self,fullname,username,email,password):
        my_database.save_users_database(fullname,username,email,password)
        return "user successfully registered"
        
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


        # for user in self.users:
        #     self.users[user[0]] = {
        #         'Id': question[1],
        #         'fullname' : question[2],
        #         'username' : question[3],
        #         'email': question[4],
        #         'password': question[5]}

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
        

        # for question in self.questions:
        #     xxx = question
        #     import pdb; pdb.set_trace()
            # if question[0] == questionId:
                # return question

        # for question in self.database_questions:
        #     if question[0] == questionId:
        #         questions_object = {
        #         'questionId':question['questionId'],
        #         'question':question['question'],
        #         'description': question['description'],
        #         'userId':question['userId'],
        #         'answers':question['answers'],
        #         'date_added':question['date_added']}
        #         return questions_object
        #     return False

    #save an answer
    def save_answer(self,questionId,answer,userId):
        
        for question in self.database_questions:
            if question['questionId'] == questionId:
                if not question['answers']:
                    answerId = 1
                    answer = {
                                'answerId': answerId,
                                'questionId': questionId,
                                'answer': answer,
                                'userId': userId,
                                'date_added':  self.date_added
                        }
                    question['answers'].append(answer)
                    return answer
                else:
                    answerId = question['answers'][-1].get('answerId') + 1
                    answer = {
                                'answerId': answerId,
                                'questionId': questionId,
                                'answer': answer,
                                'userId': userId,
                                'date_added':  self.date_added
                        }
                    question['answers'].append(answer)
                return answer
            return "Question with that question id doesnt exist" 

    #delete a question
    def delete_question(self,questionId):
        questionId = int(questionId)
        if questionId:
            for question in self.database_questions:
                if question['questionId'] == questionId:
                    self.database_questions.remove(question)
                    return question
            return "Please specify question id you want to delete"

class Answers(object):
    def __init__(self):
        # self.answers = my_database.fetch_answers_database()
        self.answers = {}





  






    
