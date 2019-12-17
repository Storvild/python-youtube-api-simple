from youtube_api.youtube_api_v3 import YoutubeApi
from youtube_api import utils
#import youtube_api.utils

try:
    from settings import API_KEY
except:
    print("Внимание!!!\n  Создайте файл settings.py рядом с sample.py и запишите туда строку:\nAPI_KEY = '<Ваш API_KEY>'\n")
    print("API_KEY от Google можно получить здесь: https://console.developers.google.com/project\n")
from pprint import pprint
import os
import json

os.chdir(os.path.dirname(__file__)) # Работаем в текущем каталоге

yt = YoutubeApi(API_KEY)

def save_json(filename, content, format=True):
    """ Сохранение json данных в файл """
    with open(filename, 'w', encoding='utf-8') as fw:
        if format:
            json.dump(content, fw, sort_keys=True, ensure_ascii=False, indent=4)
        else:    
            json.dump(content, fw, sort_keys=True, ensure_ascii=False)
 
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_channels_test():
    # Получение каналов по названию
    # Может потребоваться для получения id канала
    # Id канала будет в item['id']['channelId']
    channels = yt.get_channels('StandUpCommunity', limit=30)
    # Получить каналы в которых будут указаны определенные поля
    #channels = yt.get_channels('квн', fields='nextPageToken,items(id,snippet(title,channelId,channelTitle,description,publishedAt))', limit=3)
    #channels = yt.get_channels('квн', fields='id,snippet(title,channelId,channelTitle,description,publishedAt)', limit=3)
    #channels = yt.get_channels('квн', fields='id', limit=3)
    #print('Найденные каналы:')
    #save_json('channels.json', channels)
    pprint(channels)
    #pprint(yt.result_simple)
    

#get_channels_test()

def get_playlists_test():
    # Получение плейлистов с канала:
    #playlists = yt.get_playlists('UC4iAuuvx9hJilx4QOcd8V6A1')
    playlists = yt.get_playlists('UC8lCS8Ubv3t0-Tf4IYLioTA')
    pprint(playlists)
    pprint(yt.result_simple)
    #save_json('playlists.json',playlists)

#get_playlists()


#videos = yt.get_videos_info(['7lqVYoKiMfw','7LeO_r8_L3k'])
#videos = yt.get_videos_info('7lqVYoKiMfw,7LeO_r8_L3k,_-pPLzyplS0,4ZMv35U9oYw,MHebByfQ_nc,lBcAmL8jX-Y,psDAuK8TduQ', fields='id,snippet(title,publishedAt),contentDetails,statistics')
#videos = yt.get_videos_info('7lqVYoKiMfw,7LeO_r8_L3k,_-pPLzyplS0,4ZMv35U9oYw,MHebByfQ_nc,lBcAmL8jX-Y,psDAuK8TduQ', fields='id,snippet(title,publishedAt)')
#videos = yt.get_videos_info(['7lqVYoKiMfw','7LeO_r8_L3k','_-pPLzyplS0','4ZMv35U9oYw','MHebByfQ_nc','lBcAmL8jX-Y','psDAuK8TduQ'], part='id', fields='id')
#videos = yt.get_videos_info(['7lqVYoKiMfw','7LeO_r8_L3k','_-pPLzyplS0','4ZMv35U9oYw','MHebByfQ_nc','lBcAmL8jX-Y','psDAuK8TduQ'], part='id', fields='id', limit=5)
#pprint(videos)

def comments_page_handler(content, content_raw, yt_params, params):
    print('\n\n')
    print(params['i'], '/', params['limit'], 'pageToken=', yt_params['pageToken'], 'maxResults=', yt_params['maxResults'])
    pprint(content)
    pprint(content_raw)
    print('\n\n')
    res = True
    return res

def get_comments_test():
    #comments = yt.get_comments('7lqVYoKiMfw')
    #save_json('comments.json', comments)
    #pprint(comments)
    # comments = yt.get_comments(videoId='7lqVYoKiMfw', fields='nextPageToken,items(id,snippet(videoId,topLevelComment(id,snippet(authorDisplayName,textDisplay,textOriginal,publishedAt,updatedAt,viewerRating))))')

    #comments = yt.get_comments(videoId='7lqVYoKiMfw', fields='id,snippet', limit=150, page_handler=comments_page_handler)
    #comments = yt.get_comments(videoId='SMnI97CI-G8', fields='id,*', limit=10, page_handler=comments_page_handler, textFormat='html')

    #comments = yt.get_comments(id='Uggb3EPddGJet3gCoAEC')
    #comments = yt.get_comments(parentId='Uggb3EPddGJet3gCoAEC')
    #comments = yt.get_comments('268a2Gyq-fc')
    #comments = yt.get_comments(id='UgyteV0exQnVVEnh7dh4AaABAg')
    #comments = yt.get_comments(id='UgyteV0exQnVVEnh7dh4AaABAg', textFormat='plainText')
    #comments = yt.get_comments(parentId='UgyteV0exQnVVEnh7dh4AaABAg')
    #comments = yt.get_comments(parentId='UgwdSoJQp6IIJIaarER4AaABAg')
    #save_json('commentId.json', comments)
    #pprint(yt.result_raw)
    pprint(comments)
    pprint(yt.result_simple)


def _get_delta_list_test():
    from datetime import datetime
    dt1 = datetime(2019,3,6,10,30,0)
    dt2 = datetime.now()
    #dt2 = datetime(2019,12,6)
    #yt._get_delta_list(dt1,dt2,part=5)
    #yt.test(dt1,dt2,part_by_day=False, part_by_month=True)
    #yt._get_delta_list(datetime(2019,6,15,10,20,0),datetime(2019,8,3,22,40,0),part_by='day')
    #yt._get_delta_list(datetime(2019,7,15,10,20,0),datetime(2019,8,3,22,40,0),part_by='day')
    #yt._get_delta_list(datetime(2018,8,31,10,20,0),datetime(2019,4,1,22,40,0),part_by='month')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,4,1,22,40,0),part_by='month')
    #yt._get_delta_list(datetime(2019,3,10,10,20,0),datetime(2019,3,13,22,40,0),part_by='month')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,6,1,22,40,0),part_by='month')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,6,30,23,59,59),part_by='month')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,6,1,0,0,0),part_by='month')
    #yt._get_delta_list(datetime(2018,8,31,10,20,0),datetime(2019,4,1,22,40,0),part_by='month')
    #yt._get_delta_list(datetime(2018,8,31,10,20,0),datetime(2019,4,1,0,0,0),part_by='month')

    #yt._get_delta_list(datetime(2015,3,31,10,20,0),datetime(2019,6,1,0,0,0),part_by='year')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,6,10,10,31,0),part_by='year')
    #yt._get_delta_list(datetime(2018,12,31,23,59,59),datetime(2019,6,10,10,31,0),part_by='year')
    #yt._get_delta_list(datetime(2018,1,1,0,0,0),datetime(2019,6,10,10,31,0),part_by='year')
    #yt._get_delta_list(datetime(2018,1,1,0,0,0),datetime(2018,1,1,0,0,0),part_by='year')


def _result_parse_test():
    js = load_json('channels.json')
    #js =  load_json('playlists.json')
    #js =  load_json('comments.json')
    #js =  load_json('commentId.json')
    #js =  load_json('commentsParent.json')
    res = yt._result_parse(js)
    #for i in res:
    #    print(i)
    #print(res)
    pprint(res)


def utils_truncatechars_test():
    res = utils.truncatechars('Большой текст', 9)
    print("utils.truncatechars('Большой текст', 9) => ", res)
    assert utils.truncatechars('Большой текст', 9) == 'Большо...'
    res = utils.truncatechars('Большой текст', 5)
    print("utils.truncatechars('Большой текст', 5) => ", res)
    assert utils.truncatechars('Большой текст', 5) == 'Бо...'
    res = utils.truncatechars('Текст', 10)
    print("utils.truncatechars('Текст', 10) => ", res)
    assert utils.truncatechars('Текст', 10) == 'Текст' \
                                               ''
def download_json_test():
    yt = YoutubeApi(API_KEY)
    fields = '*'
    maxResults = 5
    order = 'date'
    q = 'квн'
    # Ошибок нет
    # url = 'https://www.googleapis.com/youtube/v3/search?type=channel&part=id&fields={fields}&maxResults={max_results}&order={order}&q={q}&key={API_KEY}'.format(**{'fields':fields,'max_results':maxResults,'order':order,'q':q,'API_KEY':API_KEY})
    # Ошибка при передачи part
    # url = 'https://www.googleapis.com/youtube/v3/search?type=channel&part=@@@id&fields={fields}&maxResults={max_results}&order={order}&q={q}&key={API_KEY}'.format(**{'fields':fields,'max_results':maxResults,'order':order,'q':q,'API_KEY':API_KEY})
    # Ошибка при передачи полей fields
    # url = 'https://www.googleapis.com/youtube/v3/search?type=channel&part=id&fields=@@@{fields}&maxResults={max_results}&order={order}&q={q}&key={API_KEY}'.format(**{'fields':fields,'max_results':maxResults,'order':order,'q':q,'API_KEY':API_KEY})
    # Ошибка при передаче ключа API_KEY
    # url = 'https://www.googleapis.com/youtube/v3/search?type=channel&part=id&fields={fields}&maxResults={max_results}&order={order}&q={q}&key=@@@{API_KEY}'.format(**{'fields':fields,'max_results':maxResults,'order':order,'q':q,'API_KEY':API_KEY})
    # Не передан параметр part
    # url = 'https://www.googleapis.com/youtube/v3/search?key={API_KEY}'.format(**{'fields':fields,'max_results':maxResults,'order':order,'q':q,'API_KEY':API_KEY})
    # Нет страницы search111 404
    #url = 'https://www.googleapis.com/youtube/v3/search111key={API_KEY}'.format(**{'fields':fields,'max_results':maxResults,'order':order,'q':q,'API_KEY':API_KEY})
    # Ошибка в имени сайта
    # url = 'https://www.googleapis1.com/youtube/v3/search?type=channel&part=id&fields={fields}&maxResults={max_results}&order={order}&q={q}&key={API_KEY}'.format(**{'fields':fields,'max_results':maxResults,'order':order,'q':q,'API_KEY':API_KEY})

    obj = yt.download_yt_json(url)

    pprint(obj)

    # Возможные Ошибки:
    # fields='1*'
    err = {'error': {'code': 400,
           'errors': [{'domain': 'global',
                       'location': 'fields',
                       'locationType': 'parameter',
                       'message': 'Invalid field selection 1*',
                       'reason': 'invalidParameter'}],
           'message': 'Invalid field selection 1*'}}
    # maxResults = 100
    err2 = {'error': {'code': 400,
               'errors': [{'domain': 'global',
                       'location': 'maxResults',
                       'locationType': 'parameter',
                       'message': "Invalid value '100'. Values must be within "
                                  'the range: [0, 50]',
                       'reason': 'invalidParameter'}],
                'message': "Invalid value '100'. Values must be within the range: "
                      '[0, 50]'}}
    # order = 'date,max'            
    err3 = {'error': {'code': 400,
                'errors': [{'domain': 'global',
                       'location': 'order',
                       'locationType': 'parameter',
                       'message': "Invalid string value: 'date,max'. Allowed "
                                  'values: [date, rating, relevance, title, '
                                  'videocount, viewcount]',
                       'reason': 'invalidParameter'}],
                'message': "Invalid string value: 'date,max'. Allowed values: "
                      '[date, rating, relevance, title, videocount, '
                      'viewcount]'}}  
    # Неправильный ключ API_KEY
    err4 = {'error': {'code': 400,
                      'errors': [{'domain': 'usageLimits',
                                  'message': 'Bad Request',
                                  'reason': 'keyInvalid'}],
                      'message': 'Bad Request'}}
    # Превышена квота
    err5 = {
        'error': {
            'errors': [{
                'domain': 'youtube.quota',
                'reason': 'quotaExceeded',
                'message': 'The request cannot be completed because you have exceeded your <a href="/youtube/v3/getting-started#quota">quota</a>.'
            }
            ],
            'code': 403,
            'message': 'The request cannot be completed because you have exceeded your <a href="/youtube/v3/getting-started#quota">quota</a>.'
        }
    }

def page_handler(content, content_raw, yt_params, params):
    print(yt_params['url'])
    pass
    #fn = 'log/{}_{}_{}.json'.format(url.replace('https://','').replace('www.googleapis.com/youtube/v3/','').replace('?','_'), page_num, page_token)
    #save_json(fn, content_raw)

def ytdate_test():
    print(utils.ytdate_to_str('PT1H24S'))
    print(utils.ytdate_to_sec('PT1H24S'))
    print(utils.ytdate_to_timedelta('P10DT2H24S'))

def _correct_part_test():
    print(yt._correct_part('id,snippet,statistics,contentDetails','statistics,snippet(*)'))

def get_videos_test():
    from datetime import datetime

    #res = yt.get_videos(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, fromdate=datetime(2019,12,1), todate=datetime(2019,12,8))
    #res = yt.get_videos(fields='id,kind,snippet(title,publishedAt)', channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=3, fullInfo=True)
    #res = yt.get_videos_partion(channelId='UCSZ69a-0I1RRdNssyttBFcA', fromdate=datetime(2012,12,1), todate=datetime(2013,1,9), partion_by='month', fullInfo=True, page_handler=page_handler) #kvn
    #res = yt.get_videos_partion(fields='id,kind,snippet(title,publishedAt)', limit=60, channelId='UCSZ69a-0I1RRdNssyttBFcA', fromdate=datetime(2012,12,1), todate=datetime(2013,1,9), partion_by='month', fullInfo=True, page_handler=page_handler) #kvn
    #res = yt.get_videos_partion(fields='id,snippet(title,publishedAt)', limit=60, channelId='UCSZ69a-0I1RRdNssyttBFcA', fromdate=datetime(2012,12,1), todate=datetime(2013,1,9), partion_by='month', fullInfo=True, page_handler=page_handler) #kvn
    #res = yt.get_videos_partion(fields='*', limit=60, channelId='UCSZ69a-0I1RRdNssyttBFcA', fromdate=datetime(2012,12,1), todate=datetime(2013,1,9), partion_by='month', fullInfo=True, page_handler=page_handler) #kvn

    #res = yt.get_videos_partion(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, fromdate=datetime(2019,11,29,8,30), todate=datetime(2019,12,2,21,0), partion_by='day')
    #res = yt.get_videos_partion(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, fromdate=datetime(2018,10,29,8,30), todate=datetime(2019,2,2,21,0), partion_by='month')

    # fields = 'id,snippet(title,publishedAt)'
    # fields = '*'
    # res = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A', fromdate=None, todate=None, limit=5,
    #                    part='id,snippet', fields=fields, order='date', fullInfo=False, page_handler=None)
    #fields = 'id,snippet(title,publishedAt),statistics,contentDetails'
    #fields='*'
    fields = 'id,snippet(title,publishedAt),contentDetails'
    #res = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A', limit=100, part='id,snippet,statistics,contentDetails', fields=fields, order='date', fullInfo=False, page_handler=page_handler)
    #res = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A', limit=100, part='id,snippet,statistics,contentDetails', fields=fields, order='date', fullInfo=True, page_handler=page_handler)
    #res = yt.get_videos(q='', channelId='UC4iAuuvx9hJilx4QOcd8V6A', playlistId='', fromdate=None, todate=None, limit=5, part='id,snippet,contentDetails,statistics', fields='*', order='date', fullInfo=False, page_handler=None)
    #res = yt.get_videos(q='', channelId='', playlistId='PLK-qRho50lIsxy-8B3FeAdKjtajY6XB06', fromdate=None, todate=None, limit=5, part='id,snippet,contentDetails,statistics', fields='*', order='date', fullInfo=True, page_handler=None)
    #res = yt.get_videos_partion(fromdate=datetime(2019,10,1), todate=datetime(2019,12,1), q='квн', playlistId='', limit=5, part='id,snippet,contentDetails', fields=fields, order='date', fullInfo=True, page_handler=None, partion_by=3)

    pprint(res)
    pprint(yt.result_simple)
    pass

def from_main():
    pass

    # data = yt.get_comments(videoId='SMnI97CI-G8', fields='*', limit=10, order='relevance', textFormat='html')
    # pprint(data)

    # obj = yt.download_yt_json('http://yandex.ru'); pprint(obj)
    # yt._result_parse()
    # dt1 = datetime(2019,11,3,10,54)
    # dt2 = datetime.now()
    # d1 = utils.date_period_into_parts(dt1, dt2, part_by='day')
    # pprint(d1)
    # d2 = utils.date_period_into_parts(dt1, dt2, part=10, part_by='month')
    # pprint(d2)
    # d3 = utils.date_period_into_parts(dt1, dt2, part=5)
    # pprint(d3)
    # yt.get_playlists('')
    # playlists = yt.get_playlists('UCSZ69a-0I1RRdNssyttBFcA')
    # playlists = yt.get_playlists(channelId='UC4iAuuvx9hJilx4QOcd8V6A')
    # yt.get_video_info(['1','3'])
    # videos = yt.get_videos('7lqVYoKiMfw,7LeO_r8_L3k')
    # ids = ','.join([str(x) for x in range(0,121,1)])
    # ids = [x for x in range(0,121,1)]
    # print(ids)

    # videos = yt.get_videos(ids)
    # videos = yt.get_videos([str(x) for x in range(0,125,1)])
    # print(utils.ytdate_to_str('PT1H24S'))
    # print(utils.ytdate_to_sec('PT1H24S'))
    # print(utils.ytdate_to_timedelta('P10DT2H24S'))
    # yt.get_videos(playlistId='123ABC')
    # yt.get_videos(channelId='123ABC')
    # videos = yt.get_videos(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, fromdate=datetime(2019,12,1), todate=datetime(2019,12,8))
    # videos = yt.get_videos(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=3, fullInfo=True)
    # pprint(videos)
    # res = yt.get_videos_partion(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, fromdate=datetime(2019,10,8), todate=datetime(2019,12,2), partion_by='month')
    # res = yt.get_videos_partion(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, fromdate=datetime(2019,11,29,8,30), todate=datetime(2019,12,2,21,0), partion_by='day')
    # res = yt.get_videos_partion(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, fromdate=datetime(2018,10,29,8,30), todate=datetime(2019,2,2,21,0), partion_by='month')
    # res = yt.get_videos_partion(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, fromdate=datetime(2018,12,29,8,30), todate=datetime(2019,1,2,21,0), partion_by='day')
    # print(res)

    # fields = 'id,snippet(title,publishedAt)'
    # fields = '*'
    # res = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A', fromdate=None, todate=None, limit=5,
    #                    part='id,snippet', fields=fields, order='date', fullInfo=False, page_handler=None)
    # fields = 'id,snippet(title,publishedAt),statistics,contentDetails'
    # res = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A', fromdate=None, todate=None, limit=5,
    #                    part='id,snippet,statistics,contentDetails', fields=fields, order='date', fullInfo=True, page_handler=None)

    # res = yt.get_videos(q='', channelId='UC4iAuuvx9hJilx4QOcd8V6A', playlistId='', fromdate=None, todate=None, limit=5,
    #                   part='id,snippet,contentDetails,statistics', fields='*', order='date', fullInfo=False, page_handler=None)
    # res = yt.get_videos(q='', channelId='', playlistId='PLK-qRho50lIsxy-8B3FeAdKjtajY6XB06', fromdate=None, todate=None, limit=5,
    #                   part='id,snippet,contentDetails,statistics', fields='*', order='date', fullInfo=True, page_handler=None)
    # res = yt.get_videos_partion(fromdate=datetime(2019,10,1), todate=datetime(2019,12,1), q='', channelId='UC4iAuuvx9hJilx4QOcd8V6A', playlistId='', limit=5,
    #                   part='id,snippet,contentDetails', fields='*', order='date', fullInfo=True, page_handler=None,
    #                   partion_by=3)
    # pprint(res)
    # res = yt.get_videos(fromdate=datetime(2019,10,1), todate=datetime(2019,12,1), q='', channelId='UC4iAuuvx9hJilx4QOcd8V6A', playlistId='', limit=5,
    #                   part='id,snippet,statistics,contentDetails', fields='id,contentDetails,snippet(title)', order='date', fullInfo=True, page_handler=None
    #                   )
    # pprint(res)
    # print(yt._correct_part('id,snippet,statistics,contentDetails','statistics,snippet(*)'))
    # print(_safe_url('http://googleapi.com/search?my=2&maxResults=3&key=123&pageToken=qqq'))
    # print(_clean_url('http://googleapi.com/search?my=2&maxResults=3&key=123'))

    # mytest('first', 20, p='param1')
    # import inspect
    # sig = inspect.signature(mytest)
    # print(dir(sig))
    # pprint(sig.parameters)
    # pprint(mytest.__code__)
    # pprint(mytest.__defaults__)


if __name__ == '__main__':

    # _get_delta_list_test()
    #get_comments_test()
    #_result_parse_test()
    #utils_truncatechars_test()
    #download_json_test()
    #get_videos_test()
    #ytdate_test()
    #_correct_part_test()
    get_channels_test()
    #get_playlists_test()

    pass