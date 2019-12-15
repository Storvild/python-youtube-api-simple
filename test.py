import unittest
from youtube_api import utils
from youtube_api.youtube_api_v3 import YoutubeApi
from datetime import datetime, timedelta
from pprint import pprint


class TestUtils(unittest.TestCase):
    def test_date_period_into_parts(self):
        fromdate = datetime(2019,1,10,11,30)
        todate = datetime(2019,4,3,22,40)
        datepart = utils.date_period_into_parts(fromdate, todate, partion_by=3)
        self.assertEqual(len(datepart), 3, "Период делится на 3 части")
        self.assertEqual(datepart[0]['fromdate'], fromdate, "Начальная дата не совпадает")

        datepart2 = utils.date_period_into_parts(fromdate, todate, partion_by='month')
        self.assertEqual(len(datepart2), 4, "Период делится на по месяцам")
        self.assertEqual(datepart2[0]['fromdate'], fromdate, "Начальная дата не совпадает")

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

    def test_ytdate_to_str(self):
        self.assertEqual(utils.ytdate_to_str('PT1H24S'), '01:00:24')
        self.assertEqual(utils.ytdate_to_str('PT2H16M36S'), '02:16:36')
        self.assertEqual(utils.ytdate_to_str('P10DT2H16M36S'), '10d 02:16:36')

    def test_ytdate_to_timedelta(self):
        self.assertEqual(utils.ytdate_to_timedelta('PT1H24S'), timedelta(0, 3624))  # 1:00:24
        self.assertEqual(utils.ytdate_to_timedelta('PT2H16M36S'), timedelta(0, 8196))  # 2:16:36
        self.assertEqual(utils.ytdate_to_timedelta('P10DT2H16M36S'), timedelta(10, 8196))  # 10days, 2:16:36


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
        from youtube_api.youtube_api_v3 import _clean_url
        self.assertEqual(_clean_url('http://mysite.com/page?key=123&part=snippet'), 'http://mysite.com/page?part=snippet')
        self.assertEqual(_clean_url('http://mysite.com/page?key=123'), 'http://mysite.com/page?')
        self.assertEqual(_clean_url('http://mysite.com/page?fields=*&key=123'), 'http://mysite.com/page?fields=*')
        self.assertEqual(_clean_url('http://mysite.com/page?fields=*&key=123&part=id'), 'http://mysite.com/page?fields=*&part=id')

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
        self.assertGreaterEqual(len(obj), 1)
        self.assertEqual(obj['kind'], 'youtube#video')

    def _test_get_videos(self):
        obj = self.yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A', limit=50)
        #print(obj)
        self.assertEqual(obj[0]['id']['kind'], 'youtube#video')
        self.assertGreaterEqual(len(obj), 0)

    def _test_get_videos_q(self):
        obj = self.yt.get_videos(q='квн', limit=10, order='relevance')
        self.assertEqual(len(obj), 10)
        self.assertIn('snippet', obj[0])

    def _test_get_videos_fullinfo(self):
        obj = self.yt.get_videos(channelId='UC8lCS8Ubv3t0-Tf4IYLioTA', fullInfo=True,
                                 fields='id,snippet(title,publishedAt),statistics,contentDetails', limit=5)
        self.assertGreaterEqual(len(obj), 1)
        self.assertIn('contentDetails', obj[0])

    def _test_get_videos_partion(self):
        from datetime import datetime
        obj = self.yt.get_videos_partion(fromdate=datetime(2019,1,30,10,30), todate=datetime(2019,2,3), limit=5,
                                         partion_by='day', page_handler=videos_partion_handler)
        self.assertGreaterEqual(len(obj),1)
        self.assertIn('kind', obj[0])

    def _test_get_comments(self):
        obj = self.yt.get_comments(videoId='Dy17RExwe8E')
        self.assertGreaterEqual(len(obj), 1)
        self.assertEqual(obj[0]['snippet']['topLevelComment']['snippet']['videoId'], 'Dy17RExwe8E')


if __name__ == '__main__':
    unittest.main()