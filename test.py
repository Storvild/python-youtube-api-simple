import unittest
from youtube_api import utils
from youtube_api.youtube_api_v3 import YoutubeApi, YoutubeException
#from datetime import datetime, timedelta
import datetime
from pprint import pprint


class TestUtils(unittest.TestCase):
    def test_date_period_into_parts(self):
        fromdate = datetime.datetime(2019,1,10,11,30)
        todate = datetime.datetime(2019,4,3,22,40)
        datepart = utils.date_period_into_parts(fromdate, todate, partion_by=3)
        self.assertEqual(len(datepart), 3, "Период делится на 3 части")
        self.assertEqual(datepart[0]['fromdate'], fromdate, "Начальная дата не совпадает")

        datepart2 = utils.date_period_into_parts(fromdate, todate, partion_by='month')
        self.assertEqual(len(datepart2), 4, "Период делится на по месяцам")
        self.assertEqual(datepart2[0]['fromdate'], fromdate, "Начальная дата не совпадает")

        fromdate = datetime.datetime(2018,10,10,11,30)
        todate = datetime.datetime(2019,3,3,22,40)
        datepart3 = utils.date_period_into_parts(fromdate, todate, partion_by='month')
        self.assertEqual(len(datepart3), 6, "Период делится по месяцам")
        datepart3 = utils.date_period_into_parts(fromdate, todate, partion_by='day')
        self.assertEqual(len(datepart3), 145, "Период делится по дням")
        datepart4 = utils.date_period_into_parts(datetime.datetime(2019,2,27, 20,30), datetime.datetime(2019,3,3,10), partion_by='day')
        self.assertEqual(len(datepart4), 5, "Разбивка по дням. Не високосный год.")
        datepart5 = utils.date_period_into_parts(datetime.date(2018,12,28), datetime.date(2019,1,3), partion_by='day')
        self.assertEqual(len(datepart5), 7, "Разбивка по дням с переходом между годами")
        datepart6 = utils.date_period_into_parts(datetime.datetime(2019,2,1, 20,30), datetime.datetime(2019,5,10), partion_by='month')
        self.assertEqual(len(datepart6), 4, "Разбивка по месяцам")
        datepart7 = utils.date_period_into_parts(datetime.datetime(2016,2,1, 20,30), datetime.datetime(2016,5,10), partion_by='month')
        self.assertEqual(datepart7[0]['todate'], datetime.datetime(2016,2,29,23,59,59), "Разбивка по месяцам. Високосный год")
        datepart8 = utils.date_period_into_parts(datetime.datetime(2015,11,10), datetime.date(2016,4,5), partion_by='month')
        self.assertEqual(len(datepart8), 6, "Разбивка по месяцам с переходом между годами")
        datepart9 = utils.date_period_into_parts(datetime.date(2015,2,1), datetime.date(2019,5,10), partion_by='year')
        self.assertEqual(len(datepart9), 5, "Разбивка по годам. Тип datetime.date")
        datepart10 = utils.date_period_into_parts(datetime.datetime(2016,12,31), datetime.datetime(2018,1,1), partion_by='year')
        self.assertEqual(len(datepart10), 3, "Разбивка по годам. Тип datetime.datetime")
        
        #datepart11 = utils.date_period_into_parts(datetime.datetime(2016,5,31), datetime.datetime(2016,2,1), partion_by='month')
        #self.assertEqual(len(datepart11), 3, "Разбивка по годам. Тип datetime.datetime")
        

    def test_truncatechars(self):
        self.assertEqual(utils.truncatechars('Длинный текст', 8, onestring=True), 'Длинн...', 'Текст не совпадает')
        self.assertEqual(utils.truncatechars('Длинный', 7, onestring=True), 'Длинный', 'Текст не совпадает')
        self.assertEqual(utils.truncatechars('Длинный', 6, onestring=True), 'Дли...', 'Текст не совпадает')

    def test_ytdate_to_sec(self):
        self.assertEqual(utils.ytdate_to_sec('PT1H24S'), 3624)
        self.assertEqual(utils.ytdate_to_sec('PT2H16M36S'), 8196)
        self.assertEqual(utils.ytdate_to_sec('P10DT2H16M36S'), 872196)

    def test_ytdate_to_str(self):
        self.assertEqual(utils.ytdate_to_str('PT1H24S'), '01:00:24')
        self.assertEqual(utils.ytdate_to_str('PT2H16M36S'), '02:16:36')
        self.assertEqual(utils.ytdate_to_str('P10DT2H16M36S'), '10d 02:16:36')

    def test_ytdate_to_timedelta(self):
        self.assertEqual(utils.ytdate_to_timedelta('PT1H24S'), datetime.timedelta(0, 3624))  # 1:00:24
        self.assertEqual(utils.ytdate_to_timedelta('PT2H16M36S'), datetime.timedelta(0, 8196))  # 2:16:36
        self.assertEqual(utils.ytdate_to_timedelta('P10DT2H16M36S'), datetime.timedelta(10, 8196))  # 10days, 2:16:36

    def _test_download_exception(self):
        self.assertRaises(utils.DownloadException, utils.download_json, 'http://ya.ru/')
        try:
            utils.download_json('http://ya.ru')
        except utils.DownloadException as e:
            self.assertEqual(e.response_status, 200)
            self.assertNotEqual(e.response_content, '')

    def _test_download_json(self):
        obj = utils.download_json('http://storvild.ru/yt.php?videoId=4rbauSBo8kY');
        self.assertIn('items', obj)

    def test_clean_text(self):
        self.assertEqual(utils.clean_text('Лайк,\nкак всегда! 👍😊, Another text!'), 'Лайк,\nкак всегда! , Another text!')
        self.assertEqual(utils.clean_text('Лайк,\nкак всегда! 👍😊, Another text!', replace_newline=' '), 'Лайк, как всегда! , Another text!')

    def test_sec_to_str(self):
        self.assertEqual(utils.sec_to_str(70), '01:10')
        self.assertEqual(utils.sec_to_str(3685), '1:01:25')
        self.assertEqual(utils.sec_to_str(83685), '23:14:45')
    
    def test_date_to_datetime(self):
        self.assertEqual(utils.date_to_datetime(datetime.date(2019,12,3)), datetime.datetime(2019,12,3,0,0,0))
        
    def test_datetime_to_date(self):
        self.assertEqual(utils.datetime_to_date(datetime.datetime(2019,12,3,12,30,59)), datetime.date(2019,12,3))
        self.assertEqual(utils.datetime_to_date(datetime.datetime(2019,12,3,12,30,59)), datetime.date(2019,12,3))
        
    def test_datetime_end_of_month(self):
        self.assertEqual(utils.datetime_end_of_month(datetime.datetime(2019,12,3,12,30,59)), datetime.datetime(2019,12,31,23,59,59))
        self.assertEqual(utils.datetime_end_of_month(datetime.datetime(2019,2,3,12,30,59)), datetime.datetime(2019,2,28,23,59,59))
        self.assertEqual(utils.datetime_end_of_month(datetime.datetime(2016,2,3,12,30,59)), datetime.datetime(2016,2,29,23,59,59))
        self.assertEqual(utils.datetime_end_of_month(datetime.datetime(2019,11,3,12,30,59)), datetime.datetime(2019,11,30,23,59,59))
        self.assertEqual(utils.datetime_end_of_month(datetime.date(2019,12,3)), datetime.datetime(2019,12,31,23,59,59))
        self.assertEqual(utils.datetime_end_of_month(datetime.date(2019,12,31)), datetime.datetime(2019,12,31,23,59,59))
        self.assertEqual(utils.datetime_end_of_month(datetime.date(2019,1,1)), datetime.datetime(2019,1,31,23,59,59))
        self.assertEqual(utils.datetime_end_of_month(datetime.date(2019,2,28)), datetime.datetime(2019,2,28,23,59,59))
        self.assertEqual(utils.datetime_end_of_month(datetime.date(2016,2,28)), datetime.datetime(2016,2,29,23,59,59))
        self.assertEqual(utils.datetime_end_of_month(datetime.date(2016,11,3)), datetime.datetime(2016,11,30,23,59,59))

    def test_datetime_start_of_month(self):
        self.assertEqual(utils.datetime_start_of_month(datetime.datetime(2019,12,3,12,30,59)), datetime.datetime(2019,12,1,0,0,0))
        self.assertEqual(utils.datetime_start_of_month(datetime.date(2019,12,3)), datetime.datetime(2019,12,1,0,0,0))
        


def videos_partion_handler(content, content_raw, yt_params, params):
    print('i =', params['i'], 'limit=', params['limit'], 'pageToken=', yt_params['pageToken'], 'maxResults=',
          yt_params['maxResults'], 'fromdate=', yt_params['fromdate'], 'todate=', yt_params['todate'])
    return True


class TestYoutubeApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestYoutubeApi, self).__init__(*args, **kwargs)
        from settings import API_KEY
        self.yt = YoutubeApi(API_KEY)


    def test__clean_url(self):
        #from youtube_api.youtube_api_v3 import _clean_url
        self.assertEqual(YoutubeApi._clean_url('http://mysite.com/page?key=123&part=snippet'), 'http://mysite.com/page?part=snippet')
        self.assertEqual(YoutubeApi._clean_url('http://mysite.com/page?key=123'), 'http://mysite.com/page?')
        self.assertEqual(YoutubeApi._clean_url('http://mysite.com/page?fields=*&key=123'), 'http://mysite.com/page?fields=*')
        self.assertEqual(YoutubeApi._clean_url('http://mysite.com/page?fields=*&key=123&part=id'), 'http://mysite.com/page?fields=*&part=id')

    #def test_fail(self):
    #    self.fail('Ошибка теста')

    def test__correct_part(self):
        self.assertEqual(self.yt._correct_part('id,statistics,snippet,contentDetails', 'id,snippet(*),contentDetails'), 'id,snippet,contentDetails')
        self.assertEqual(self.yt._correct_part('id,snippet', 'id,snippet(*),contentDetails'), 'id,snippet')
        self.assertEqual(self.yt._correct_part('id,snippet', 'snippet'), 'id,snippet')

    def _test_download_yt_json(self):
        from settings import API_KEY
        obj = utils.download_json('https://www.googleapis.com/youtube/v3/videos?part=id&id=Dy17RExwe8E&key={}'.format(API_KEY))
        self.assertEqual(obj['kind'], 'youtube#videoListResponse')
        self.assertRaises(utils.DownloadException, utils.download_json, 'https://www.googleapis.com/youtube/v3/')

    def _test_get_channels_playlists(self):
        obj = self.yt.get_channels('квн', limit=5)
        self.assertGreater(len(obj), 0, 'Список каналов пуст')
        channelId = obj[0]['id']['channelId']
        self.assertNotEqual(channelId, '')

        obj = self.yt.get_playlists(channelId, limit=5)
        playlistId = obj[0]['id']['playlistId']
        self.assertNotEqual(playlistId, '')

    def _test_get_videos_info(self):
        obj = self.yt.get_videos_info('BWysOdCSz0k')
        #pprint(obj)
        self.assertGreaterEqual(len(obj['items']), 1)
        self.assertEqual(obj['items'][0]['kind'], 'youtube#video')

    def _test_get_videos(self):
        obj = self.yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A', limit=50)
        #print(obj)
        self.assertEqual(obj['items'][0]['id']['kind'], 'youtube#video')
        self.assertGreaterEqual(len(obj['items']), 0)

    def _test_get_videos_q(self):
        obj = self.yt.get_videos(q='квн', limit=10, order='relevance')
        self.assertEqual(len(obj['items']), 10)
        self.assertIn('snippet', obj['items'][0])

    def _test_get_videos_fullinfo(self):
        obj = self.yt.get_videos(channelId='UC8lCS8Ubv3t0-Tf4IYLioTA', fullInfo=True,
                                 fields='id,snippet(title,publishedAt),statistics,contentDetails', limit=5)
        self.assertGreaterEqual(len(obj['items']), 1)
        self.assertIn('contentDetails', obj['items'][0])

    def _test_get_videos_partion(self):
        from datetime import datetime
        obj = self.yt.get_videos(fromdate=datetime(2019,1,30,10,30), todate=datetime(2019,2,3), limit=5,
                                         partion_by=2, page_handler=videos_partion_handler)
        self.assertGreaterEqual(len(obj['items']),1)
        self.assertIn('kind', obj['items'][0])
        
        obj = self.yt.get_videos(fromdate=datetime(2018,11,29,10,30), todate=datetime(2019,2,3), limit=20,
                                         partion_by='month', page_handler=videos_partion_handler)
        self.assertGreaterEqual(len(obj['items']),1)
        self.assertIn('kind', obj['items'][0])
        
        obj = self.yt.get_videos(fromdate=datetime(2018,11,29,10,30), todate=datetime(2019,2,3), limit=20,
                                         partion_by='3', page_handler=videos_partion_handler)
        self.assertGreaterEqual(len(obj['items']),1)
        self.assertIn('kind', obj['items'][0])
        
        obj = self.yt.get_videos(fromdate=datetime(2016,2,27,10,30), todate=datetime(2016,3,2), limit=20,
                                         partion_by='day', page_handler=videos_partion_handler)
        self.assertGreaterEqual(len(obj['items']),1)
        self.assertIn('kind', obj['items'][0])

    def _test_get_comments(self):
        obj = self.yt.get_comments(videoId='Dy17RExwe8E')
        self.assertGreaterEqual(len(obj['items']), 1)
        self.assertEqual(obj['items'][0]['snippet']['topLevelComment']['snippet']['videoId'], 'Dy17RExwe8E')

    def _test_get_comments_off(self):
        """ Тест получения комментариев к видео, у которых они отключены """
        try:
            obj = self.yt.get_comments(videoId='mg7OTHfdDMc')
        except YoutubeException as e:
            self.assertEqual(e.response_status, 403)


if __name__ == '__main__':
    unittest.main()