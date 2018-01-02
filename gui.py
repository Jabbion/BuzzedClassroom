from guiElements.question_overview import question_overview, Quiz
from guiElements.main_window import MainWindows
from connect.network import Network

window = MainWindows(1280, 1024)

net = Network()
while True:
    net.start_network()