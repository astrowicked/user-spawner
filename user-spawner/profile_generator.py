from datetime import datetime as dt
import random
import firstnames
import lastnames
import hobbies


class ProfileGenerator(object):

    def __init__(self):
        self.first_name_list = firstnames.FIRST_NAMES

        self.last_name_list = lastnames.LAST_NAMES

        self.hobby_list = hobbies.HOBBIES

    def generate_random_date(self):
        #Stole from StackOverflow:
        #questions/4759223/python-select-random-date-in-current-year
        start_date = dt.now().replace(day=1, month=1).toordinal()
        end_date = dt.now().toordinal()
        random_date = dt.fromordinal(random.randint(start_date, end_date))
        return random_date

    def generate_user_doc(self):
        doc = {
            'first_name': random.choice(self.first_name_list),
            'last_name': random.choice(self.last_name_list),
            'age': random.randint(18, 48),
            'date_joined': self.generate_random_date(),
            'hobbies': random.sample(self.hobby_list, random.randint(0, 5))
        }
        return doc
