

# import os
# from urllib.parse import urlparse
# # from database import Database
# # my_database = Database()

# db_url = os.environ.get('DATABASE_URL')
# parsed_url = urlparse(db_url)
# dbname = parsed_url.path[1:]
# username = parsed_url.username
# hostname = parsed_url.hostname
# password = parsed_url.password
# port = parsed_url.port

# import pdb; pdb.set_trace()

# print(db_url)

# my_database.create_table_users()
# my_database.create_table_questions()
# my_database.create_table_answers()
# my_database.create_table_comments()

# my_database.insert_users_database('wycliff','wyco','w4wycliff@gmail.com','wyco123')
# my_database.insert_questions_database('starting computer','how do i start a computer', 1 , "2018/08/29")
# users = my_database.fetch_users_database()
# questions = my_database.fetch_questions_database()


# # (1,'wycliff','wyco','wyco123')

# for row in users:
#    print("ID = ", row[0])
#    print("NAME = ", row[1])
#    print("USERNAME = ", row[2])
#    print("EMAIL = ", row[3], "\n")



# for row in questions:
#    print("questionId = ", row[0])
#    print("question = ", row[1])
#    print("description = ", row[2])
#    print("userid = ", row[3])
#    print("answers = ", row[4])
#    print("date_added = ", row[5]) 


# questions = my_database.fetch_a_question_database(1)
# answers = []
# for row in questions:
#     answers.append(row[2])

# question_object = {
#                    "question id": row[0],
#                    "question": row[1],
#                    "answers":answers
# }
   
# import pdb; pdb.set_trace()


        # self.cursor.execute(query,[questionId])
        # results = self.cursor.fetchall()
         
        # questions = results
        # answers = []
        # for row in questions:
        #     answers.append(row[2])

        # question_object = {
        #            "question id": row[0],
        #            "question": row[1],
        #            "answers":answers
        # }



