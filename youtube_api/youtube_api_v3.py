import requests
import json
from pprint import pprint
from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta
import re
import utils

def print_log(*args, **kwargs):
    print(*args, **kwargs)

def fake_download(url, pageToken):
    res = {}
    if pageToken=='':
        res = {'items':[789], 'nextPageToken':'AAA'}
    elif pageToken=='AAA':
        res = {'items':[123], 'nextPageToken':'BBB'}
    elif pageToken=='BBB':
        res = {'items':[456], 'nextPageToken':'CCC'}
    elif pageToken=='CCC':
        res = {'items':[456]}    
    print_log(url)
    return res

class YoutubeItem():
    def __init__(self, code, type, title, publishedAt, description=''):
        self.type = type
        self.code = code
        self.title  = title
        self.publishedAt = publishedAt
        #self.channelId
        #self.channelTitle
        self.description = description
        #self.raw = None
    def __str__(self):
        return '{} {} {} {} {}'.format(self.type, self.code, self.title, self.description, self.publishedAt)
    def __repr__(self):
        return '{} {:15} {:30} {:20} {}'.format(self.type, truncatechars(self.code,15), truncatechars(self.title,30), truncatechars(self.description,20), self.publishedAt)


class YoutubeApi():
    def __init__(self, ApiKey):
        assert ApiKey != '', 'YoutubeApi: Необходимо указать KEY_API'
        self.ApiKey = ApiKey
        self.result_raw = None


    def download_yt_json(self, url, pageToken=''):
        """ Загрузка json"""
        if pageToken!='':
            url += '&pageToken={}'.format(pageToken)
        
        #res = fake_download(url, pageToken)
        obj = requests.get(url)
        try:
            res = obj.json()
        except:
            pprint(obj)
            raise
        #pprint(res)
        return res

       
    
    def _result_parse(self, js):
        res = []
        for item in js:
            if 'topLevelComment' in item['snippet']:
                kind = 'youtube#commentThread'
            elif 'kind' in item and item['kind'] == 'youtube#comment':
                kind = 'youtube#comment'
            elif 'kind' in item['id']:
                kind = item['id']['kind']
            #code, type, title, publishedAt   
            #print(kind)            
            obj = None
            if kind == 'youtube#channel':
                obj = YoutubeItem(  code=item['id']['channelId'], 
                                    type=item['id']['kind'], 
                                    title=item['snippet']['title'], 
                                    publishedAt=item['snippet']['publishedAt'],
                                    description=item['snippet']['description'],
                                  )
            elif kind == 'youtube#playlist':
                obj = YoutubeItem(  code=item['id']['playlistId'], 
                                    type=item['id']['kind'], 
                                    title=item['snippet']['title'], 
                                    publishedAt=item['snippet']['publishedAt'],
                                    description=item['snippet']['description'],
                                  )
            elif kind == 'youtube#commentThread':
                obj = YoutubeItem(  code=item['id'], 
                                    type=item['snippet']['topLevelComment']['kind'], 
                                    title=item['snippet']['topLevelComment']['snippet']['authorDisplayName'], 
                                    publishedAt=item['snippet']['topLevelComment']['snippet']['publishedAt'], 
                                    description=item['snippet']['topLevelComment']['snippet']['textOriginal'],
                                  )
            elif kind == 'youtube#comment':
                obj = YoutubeItem(  code=item['id'], 
                                    type=item['kind'], 
                                    title=item['snippet']['authorDisplayName'], 
                                    publishedAt=item['snippet']['publishedAt'],
                                    description=item['snippet']['textOriginal'],
                                  )
            if obj:
                res.append(obj)
        return res
    
        
    def get_channels(self, channelName, fields='*', limit=1000, order='relevance'):
        """ Поиск каналов по имени """
        assert order in ('date','rating','relevance','title','videoCount','viewCount'), 'get_playlists: Неправильный параметр order: {}'.format(order)
        assert channelName!='', 'get_playlists: Не задано имя канала (channelName)'
        if fields in ('','*'):
            fields = '*'
        elif 'nextPageToken' not in fields:
            fields = 'nextPageToken,items({})'.format(fields)
        
        maxResults = 50
        q = channelName
        url = 'https://www.googleapis.com/youtube/v3/search?type=channel&part=snippet&fields={fields}&maxResults={max_results}&order={order}&q={q}&key={API_KEY}'.format(**{'fields':fields,'max_results':maxResults,'order':order,'q':q,'API_KEY':self.ApiKey})
        
        res = []
        pageToken = ''
        for i in range(0, limit, maxResults):
            #print_log(i, i+maxResults)
            obj_json = self.download_yt_json(url, pageToken)
            content =  obj_json
            #print_log(content)
            res.extend(content['items'])
            if 'nextPageToken' in content:
                pageToken = content['nextPageToken']
            else:
                break        
        self.result_raw = res
        res = res[:limit]
        return res

    
    def get_playlists(self, channelId, fields='*', limit=1000, order='date'):
        """ Скачать плейлисты определенного канала
            channelId - id канала
            fields - поля
            cost:100/страницу """
        assert order in ('date','rating','relevance','title','videoCount','viewCount'), 'get_playlists: Неправильный параметр order: {}'.format(order)
        assert channelId!='', 'get_playlists: Не задан Id канала (channelId)'
        if fields in ('','*'):
            fields = '*'
        elif 'nextPageToken' not in fields:
            fields = 'nextPageToken,items({})'.format(fields)
            
        maxResults = 50
        url = 'https://www.googleapis.com/youtube/v3/search?type=playlist&part=snippet&fields={fields}&channelId={channel_id}&maxResults={max_results}&order={order}&key={API_KEY}'.format(**{'fields':fields,'channel_id':channelId,'max_results':maxResults,'order':order,'API_KEY':self.ApiKey})
        
        res = []
        pageToken = ''
        for i in range(0, limit, maxResults):
            #print_log(i, i+maxResults)
            obj_json = self.download_yt_json(url, pageToken)
            content =  obj_json
            #pprint(content)
            #print_log(content)
            res.extend(content['items'])
            if 'nextPageToken' in content:
                pageToken = content['nextPageToken']
            else:
                break
        self.result_raw = res
        res = res[:limit]
        return res
        
    
    def get_videos_info(self, videoIDs, fields='*', part='id,snippet,statistics,contentDetails', limit=1000):
        """ Получение подробной информации о видео или списке видео
            videoIDs - код видео, список видео через запятую в виде строки или списка
            part - получение информации о видео (snippet), лайки/дизлайки (statistics), длительность видео (contentDetails)
                (cost=3+2*part, например получение одной страницы с part='snippet,contentDetails' cost=7)
                part='snippet,statistics,contentDetails'
                Варианты данных указываемых в параметре part с указанием затрат на один запрос (всего на один проект выдается 10000 в день)
                contentDetails: 2
                fileDetails: 1
                id: 0
                liveStreamingDetails: 2
                localizations: 2
                player: 0
                processingDetails: 1
                recordingDetails: 2
                snippet: 2
                statistics: 2
                status: 2
                suggestions: 1
                topicDetails: 2
            fields - какие поля оставить в результирующем запросе. fields='*' - все поля
                fields='items(id,contentDetails,snippet(title,publishedAt,channelId,channelTitle,description),statistics'
        """
        assert type(videoIDs) in (list, tuple, set, str)
        
        if fields in ('','*'):
            fields = '*'
        elif 'nextPageToken' not in fields: # Если не передано обязательное поле nextPageToken, значит перечисляются только поля в items
            fields = 'nextPageToken,items({})'.format(fields)
            # Если в fields переданы поля, убираем из part неиспользуемые
            part_list = part.split(',')
            part_new = []
            for p in part_list:
                if p in fields:
                    part_new.append(p)
            part = ','.join(part_new)
            
        # Если videoIDs не является списком, преобразуем в список
        if type(videoIDs) == str:
            videoIDs = videoIDs.split(',')
        
        maxResults = 50
        res = []
        for i in range(0, len(videoIDs), maxResults):
            #print(i, i+maxResults)
            ids = ','.join(videoIDs[i:i+maxResults])
            #print(ids)
            url = 'https://www.googleapis.com/youtube/v3/videos?part={part}&fields={fields}&id={ids}&maxResults={maxResults}&key={API_KEY}'.format(**{'part':part,'fields':fields,'ids':ids,'maxResults':maxResults,'API_KEY':self.ApiKey})
            obj = self.download_yt_json(url)
            #pprint(obj)
            res.extend(obj['items'])
            if (i+maxResults)>limit and limit>0:
                break
        self.result_raw = res
        res = res[:limit]           
        
        return res
    
    def get_comments(self, videoId='', id='', parentId='', fields='*', limit=1000, order='relevance', textFormat='html'):
        """ Получить комментарии к видео 
            Обязательно заполнить один из параметров:
                videoId - комментарии к видео
                id - id комментария или список id через запятую
                parentId - ответы на комментарий (id)
            order - сортировка relevance или date
            textFormat - plainText или html
        """
        assert videoId!='' or id!='' or parentId!='', 'Должен быть заполнен один из параметров videoId, id или parentId'
        
        if fields in ('','*'):
            fields = '*'
        elif 'nextPageToken' not in fields: # Если не передано обязательное поле nextPageToken, значит перечисляются только поля в items
            fields = 'nextPageToken,items({})'.format(fields)
        
        maxResults = 100
        if limit<100:
            maxResults = limit
        #fields = '*'
        url = ''
        if videoId:
            url='https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&fields={fields}&maxResults={maxResults}&videoId={videoId}&textFormat={textFormat}&order={order}&key={API_KEY}'.format(**{'fields':fields, 'videoId':videoId, 'maxResults':maxResults, 'textFormat':textFormat, 'order':order, 'API_KEY':self.ApiKey})
        elif id:
            url='https://www.googleapis.com/youtube/v3/comments?part=snippet&fields={fields}&maxResults={maxResults}&id={id}&textFormat={textFormat}&order={order}&key={API_KEY}'.format(**{'fields':fields, 'id':id, 'maxResults':maxResults, 'textFormat':textFormat, 'order':order, 'API_KEY':self.ApiKey})
        elif parentId:
            url='https://www.googleapis.com/youtube/v3/comments?part=snippet&fields={fields}&maxResults={maxResults}&parentId={parentId}&textFormat={textFormat}&order={order}&key={API_KEY}'.format(**{'fields':fields, 'parentId':parentId, 'maxResults':maxResults, 'textFormat':textFormat, 'order':order, 'API_KEY':self.ApiKey})
            
        res = []
        pageToken = ''
        for i in range(0, limit, maxResults):
            obj_json = self.download_yt_json(url, pageToken)
            content =  obj_json
            res.extend(content['items'])
            if 'nextPageToken' in content:
                pageToken = content['nextPageToken']
            else:
                break
        self.result_raw = res
        res = res[:limit]        
        return res

    def get_videos(self, q='', channelId='', playlistId='', fromdate=None, todate=None, limit=1000, part='id,snippet,contentDetails', fields='*', order='date', fullInfo=False):
        # maxResults>=1 and maxResults<=50
        assert channelId!=0 or playlistId!=0
    
        # channelId = 'UCSZ69a-0I1RRdNssyttBFcA'
        # fields = '*'
        # fields = 'nextPageToken,pageInfo,items(id,snippet(title,publishedAt,channelTitle,channelId))'
        if not fields:
            fields = 'nextPageToken,pageInfo,items(id,snippet(title,publishedAt))'
        maxResults = 50 # Количество объектов на 1 запрос. Максимум = 50
        # maxIteration = 20 # Максимальное количество итераций для получения данных по 50 объектов. Максимум 20.

        published = ''
        if fromdate:
            if type(fromdate)==str:
                published += f'&publishedAfter={fromdate}' #2019-01-01T00:00:00Z
            else:
                published += '&publishedAfter={}Z'.format(fromdate.replace(microsecond=0).isoformat(sep='T'))
        if todate:
            if type(todate)==str:
                published += f'&publishedBefore={todate}' #2019-12-31T23:59:59Z
            else:
                published += '&publishedBefore={}Z'.format(todate.replace(microsecond=0).isoformat(sep='T'))

        url = ''
        if playlistId:
            # part = 'id,contentDetails,snippet' #contentDetails: 2; id: 0; snippet: 2; status: 2 (+1)
            url = 'https://www.googleapis.com/youtube/v3/playlistItems?part={part}&fields={fields}' \
                  '&playlistId={playlistId}&maxResults={maxResults}&key={API_KEY}'.format(**{'part': part, 'fields': fields, 'playlistId': playlistId, 'maxResults': maxResults, 'API_KEY': self.ApiKey})

            # Параметр videoId в playlistItems?????????????????????
        elif channelId:
            url = 'https://www.googleapis.com/youtube/v3/search?type=video&part=id,snippet&fields={fields}' \
                  '&channelId={channelId}&maxResults={maxResults}&order={order}{published}&key={API_KEY}'.format(**{'fields': fields, 'channelId': channelId, 'maxResults': maxResults, 'order': order, 'published': published, 'API_KEY': self.ApiKey})

        res = []
        pageToken = ''
        
        for i in range(0, limit, maxResults):
            content = self.download_yt_json(url, pageToken)
            #url_token = '{}&pageToken={}'.format(url, pageToken)
            #print(i)
            #print(url_token)
            #obj = requests.get(url_token)
            #content =  obj.json()
            if fullInfo:
                ids = [x['id']['videoId'] for x in content['items']]
                videos = self.get_videos_info(ids, fields=fields, part=part)
                #pprint(ids)
                pprint(videos)
                res.extend(videos)
            else:
                res.extend(content['items'])

            if 'nextPageToken' in content:
                pageToken = content['nextPageToken']
                time.sleep(1)
            else:
                break
        self.result_raw = res
        res = res[:limit]
        return res
    

        
if __name__ == '__main__':
    from pprint import pprint
    yt = YoutubeApi('123')
    #yt._result_parse()
    #dt1 = datetime(2019,11,3,10,54)
    #dt2 = datetime.now()
    #d1 = utils.date_period_into_parts(dt1, dt2, part_by='day')
    #pprint(d1)
    #d2 = utils.date_period_into_parts(dt1, dt2, part=10, part_by='month')
    #pprint(d2)
    #d3 = utils.date_period_into_parts(dt1, dt2, part=5)
    #pprint(d3)
    #yt.get_playlists('')
    #playlists = yt.get_playlists('UCSZ69a-0I1RRdNssyttBFcA')
    #playlists = yt.get_playlists(channelId='UC4iAuuvx9hJilx4QOcd8V6A')
    #print_log(playlists)
    #yt.get_video_info(['1','3'])
    #videos = yt.get_videos('7lqVYoKiMfw,7LeO_r8_L3k')
    #ids = ','.join([str(x) for x in range(0,121,1)])
    #ids = [x for x in range(0,121,1)]
    #print(ids)
    
    #videos = yt.get_videos(ids)
    #videos = yt.get_videos([str(x) for x in range(0,125,1)])
    #print(utils.ytdate_to_str('PT1H24S'))
    #print(utils.ytdate_to_sec('PT1H24S'))
    #print(utils.ytdate_to_timedelta('P10DT2H24S'))
    #yt.get_videos(playlistId='123ABC')
    #yt.get_videos(channelId='123ABC')
    #videos = yt.get_videos(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, fromdate=datetime(2019,12,1), todate=datetime(2019,12,8))
    #videos = yt.get_videos(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=3, fullInfo=True)
    #pprint(videos)
