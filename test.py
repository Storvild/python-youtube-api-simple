import unittest
from youtube_api import utils
from datetime import datetime, timedelta

class TestUtils(unittest.TestCase):
    def test_date_period_into_parts(self):
        fromdate = datetime(2019,1,10,11,30)
        todate = datetime(2019,4,3,22,40)
        datepart = utils.date_period_into_parts(fromdate, todate, partion_by=3)
        #print(datepart)
        self.assertEqual(len(datepart), 3, "Период делится на 3 части")
        self.assertEqual(datepart[0]['fromdate'], fromdate, "Начальная дата не совпадает")
        
        datepart2 = utils.date_period_into_parts(fromdate, todate, partion_by='month')
        self.assertEqual(len(datepart2), 4, "Период делится на по месяцам")
        self.assertEqual(datepart2[0]['fromdate'], fromdate, "Начальная дата не совпадает")
        #print(datepart2)

        fromdate = datetime(2018,10,10,11,30)
        todate = datetime(2019,3,3,22,40)
        datepart3 = utils.date_period_into_parts(fromdate, todate, partion_by='month')
        self.assertEqual(len(datepart3), 6, "Период делится по месяцам")
        
        datepart3 = utils.date_period_into_parts(fromdate, todate, partion_by='day')
        self.assertEqual(len(datepart3), 145, "Период делится по дням")
        
    def test_truncatechars(self):
        self.assertEqual(utils.truncatechars('Длинный текст', 8, onestring=True), 'Длинн...', 'Текст не совпадает')
        self.assertEqual(utils.truncatechars('Длинный', 7, onestring=True), 'Длинный', 'Текст не совпадает')
        self.assertEqual(utils.truncatechars('Длинный', 6, onestring=True), 'Дли...', 'Текст не совпадает')

    
    def test_ytdate_to_sec(self):
        self.assertEqual(utils.ytdate_to_sec('PT1H24S'), 3624)
        self.assertEqual(utils.ytdate_to_sec('PT2H16M36S'), 8196)
        self.assertEqual(utils.ytdate_to_sec('P10DT2H16M36S'), 872196)

    def test_ytdate_to_timedelta(self):
        self.assertEqual(utils.ytdate_to_timedelta('PT1H24S'), timedelta(0, 3624))  # 1:00:24
        self.assertEqual(utils.ytdate_to_timedelta('PT2H16M36S'), timedelta(0, 8196))  # 2:16:36
        self.assertEqual(utils.ytdate_to_timedelta('P10DT2H16M36S'), timedelta(10, 8196))  # 10days, 2:16:36


if __name__ == '__main__':
    unittest.main()