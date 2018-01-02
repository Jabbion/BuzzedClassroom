from Database.database import database

d = database()
print(d.getQuizNames())
print(d.getQuiz(d.getQuizNames()[0]))