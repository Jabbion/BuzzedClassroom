import csv
import datetime

def dump_csv(answers_list):
    with open(str(datetime.datetime)+'.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for answer in answers_list:
            spamwriter.writerow(answer)