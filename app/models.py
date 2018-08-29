from database import Database
my_database = Database()
from datetime import date

class Questions:
    questions = []
    answers = []
    date_added = date.today().strftime("%d/%m/%Y")

    #add questions
    def save_questions(self,question,description,userId):
        questionId = len(self.questions) + 1
        questions_object = {
        'questionId':questionId,
        'question':question,
        'description': description,
        'userId':userId,
        'answers':[],
        'date_added':self.date_added}

        my_database.insert_questions_database(question,description, userId , self.date_added)
        # self.questions.append(questions_object)
        return questions_object
  
    #fetch all questions
    def fetch_all_questions(self):
        questions = my_database.fetch_questions_database()
        return questions

    #fetch a question
    def fetch_a_question(self,questionId):
        questionId = int(questionId)
        for question in self.questions:
            if question['questionId'] == questionId:
                questions_object = {
                'questionId':question['questionId'],
                'question':question['question'],
                'description': question['description'],
                'userId':question['userId'],
                'answers':question['answers'],
                'date_added':question['date_added']}
                return questions_object
            return False

    #save an answer
    def save_answer(self,questionId,answer,userId):
        
        for question in self.questions:
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
            for question in self.questions:
                if question['questionId'] == questionId:
                    self.questions.remove(question)
                    return question
            return "Please specify question id you want to delete"







  






    
