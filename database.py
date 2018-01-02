import json

class database():

    def __init__(self, path = "JsonDatabase"):
        self.path = path
        with open(path+'/Quiz') as json_data:
            self.d = json.load(json_data)
            print(self.d)
        with open(path+'/Questions') as json_data:
            self.q = json.load(json_data)
            print(self.q)

    def getQuizNames(self):
        return self.d["QuizDict"].keys()

    def getQuiz(self, name):
        quiz = self.d["QuizDict"][name]
    

d = database()
d.getQuizNames()

