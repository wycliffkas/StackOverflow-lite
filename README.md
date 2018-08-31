 
[![Build Status](https://travis-ci.org/wycliffkas/StackOverflow-lite.svg?branch=develop)](https://travis-ci.org/wycliffkas/StackOverflow-lite)
[![Coverage Status](https://coveralls.io/repos/github/wycliffkas/StackOverflow-lite/badge.svg?branch=develop)](https://coveralls.io/github/wycliffkas/StackOverflow-lite?branch=develop)
<a href="https://codeclimate.com/github/wycliffkas/StackOverflow-lite/maintainability"><img src="https://api.codeclimate.com/v1/badges/b424ab8cb9ea956652d1/maintainability" /></a>



# StackOverflow-lite
StackOverflow-lite is a platform where people can ask questions and provide answers.
StackOverflow is a platform where students and professionals post queries and answer questions about programming. It is a platform to showcase their knowledge. The answers are upvoted based on its usefulness to the community. 

What can you do on it?

1. Users can create an account and log in.
2. Users can post questions.
3. Users can delete the questions they post.
4. Users can post answers.
5. Users can view the answers to questions.
6. Users can accept an answer out of all the answers to his/her question as the preferred answers.
7. Users can upvote or downvote an answer.
8. Users can comment on an answer.
9. Users can fetch all questions he/she has ever asked on the platform
10. Users can search for questions on the platform
11. Users can view questions with the most answers.

API Endpoints

| Endpoint                                   |      Functionality               | 
|--------------------------------------------|:--------------------------------:|
| GET /questions                             |Fetch all questions               | 
| GET /questions/<questionId>                |Fetch a specific question         |  
| POST /questions                            |Add a question                    |   
| POST /questions/<questionId>/answers       |Answers Add an answer             | 
 
     

How to Run
Step 1: install Postman on your machine
Step 2: Go to this app's directory and run python app.py
step 3: Run the API above in postman

