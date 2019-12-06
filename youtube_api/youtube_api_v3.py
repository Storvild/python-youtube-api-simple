import requests
import json
from pprint import pprint
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def print_log(*args, **kwargs):
    print(*args, **kwargs)

def fake_download(url, pageToken):

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

class YoutubeApi():
    def __init__(self, ApiKey):
        assert ApiKey != '', 'YoutubeApi: Необходимо указать KEY_API'
        self.ApiKey = ApiKey
        self.result_raw = None


    def download_json(self, url, pageToken=''):
        """ Загрузка json"""
        if pageToken!='':
            url += '&pageToken={}'.format(pageToken)
        
        #res = fake_download(url, pageToken)
        
        obj = requests.get(url)
        res = obj.json()
        #pprint(res)
        return res

    def _get_delta_list(self, fromdate, todate, part=1, part_by=None):
        """ Получить разбивку дат по периодам
            part=10 - Равномерное разбитие на 10 частей
            part_by_day=True - Разбитие по дням
            part_by_month - Разбитие по месяцам
        """
        assert part_by in (None, '', 'day', 'month', 'year')
        #print(fromdate,todate)
        delta_list = []
        if part_by=='day':
            delta = todate - fromdate
            days = delta.days if delta.seconds==0 else delta.days+1
            for i in range(days):
                fromdate_part = fromdate.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=i)
                todate_part = fromdate.replace(hour=23, minute=59, second=59, microsecond=0) + timedelta(days=i)
                delta_list.append({'fromdate':fromdate_part, 'todate':todate_part})
                #print(i, fromdate_part, '-', todate_part )
        elif part_by=='month':
            # Первый месяц
            fromdate_part_begin = fromdate # + relativedelta(hour=0, minute=0, second=0)
            todate_part_begin = min(fromdate + relativedelta(day=31, hour=23, minute=59, second=59, microsecond=0), todate)
            delta_list.append({'fromdate':fromdate_part_begin, 'todate':todate_part_begin})
            #print(fromdate_part_begin, '-', todate_part_begin, 'BEGIN')
            for i in range(fromdate.month+1, todate.month):
                fromdate_part = fromdate + relativedelta(month=i, day=1, hour=0, minute=0, second=0, microsecond=0) #.replace(month=i,day=1,hour=0,minute=0,second=0,microsecond=0)
                todate_part = fromdate + relativedelta(month=i, day=31, hour=23, minute=59, second=59, microsecond=0)
                delta_list.append({'fromdate':fromdate_part, 'todate':todate_part})
                #print(fromdate_part, '-', todate_part)
            # Последний месяц
            if delta_list[-1]['todate']  < todate.replace(microsecond=0):
                fromdate_part_end = (todate + relativedelta(day=1, hour=0, minute=0, second=0)).replace(microsecond=0)
                todate_part_end = todate.replace(microsecond=0) #+ relativedelta(day=31, hour=23, minute=59, second=59, microsecond=0)
                delta_list.append({'fromdate':fromdate_part_end, 'todate':todate_part_end})
                #print(fromdate_part_end, '-', todate_part_end, 'END')
        elif part_by=='year':
            # Первый год
            fromdate_part_begin = fromdate # + relativedelta(hour=0, minute=0, second=0)
            todate_part_begin = min(fromdate + relativedelta(month=12, day=31, hour=23, minute=59, second=59, microsecond=0), todate)
            delta_list.append({'fromdate':fromdate_part_begin, 'todate':todate_part_begin})
            #print(fromdate_part_begin, '-', todate_part_begin, 'BEGIN')
            for i in range(fromdate.year+1, todate.year):
                fromdate_part = fromdate + relativedelta(year=i, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) 
                todate_part = fromdate + relativedelta(year=i, month=12, day=31, hour=23, minute=59, second=59, microsecond=0)
                delta_list.append({'fromdate':fromdate_part, 'todate':todate_part})
                #print(fromdate_part, '-', todate_part)
            # Последний год
            if delta_list[-1]['todate']  < todate.replace(microsecond=0):
                fromdate_part_end = (todate + relativedelta(month=1, day=1, hour=0, minute=0, second=0)).replace(microsecond=0)
                todate_part_end = todate.replace(microsecond=0)
                delta_list.append({'fromdate':fromdate_part_end, 'todate':todate_part_end})
                #print(fromdate_part_end, '-', todate_part_end, 'END')
        else:
            delta = todate - fromdate
            delta_by_part = delta/part
            #print('Кол-во часте:', part)
            #print('Всего дней:', delta)
            #print('Дней на часть:', delta_by_part)
            for i in range(part):
                fromdate_part = (fromdate + i*delta_by_part).replace(microsecond=0)
                todate_part = (fromdate.replace(microsecond=0) + i*delta_by_part + delta_by_part - timedelta(seconds=1)).replace(microsecond=0)
                delta_list.append({'fromdate':fromdate_part, 'todate':todate_part})
                #print(i, fromdate_part, '-', todate_part)
        
        for i in delta_list:
            print(i['fromdate'], '-', i['todate'])
        
        return delta_list
        
        
        
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
            obj_json = self.download_json(url, pageToken)
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
            obj_json = self.download_json(url, pageToken)
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
            obj = self.download_json(url)
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
        if videoId:
            url='https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&fields={fields}&maxResults={maxResults}&videoId={videoId}&textFormat={textFormat}&key={API_KEY}'.format(**{'fields':fields, 'videoId':videoId, 'maxResults':maxResults, 'textFormat':textFormat, 'API_KEY':self.ApiKey})
        elif id:
            url='https://www.googleapis.com/youtube/v3/comments?part=snippet&fields={fields}&maxResults={maxResults}&id={id}&textFormat={textFormat}&key={API_KEY}'.format(**{'fields':fields, 'id':id, 'maxResults':maxResults, 'textFormat':textFormat, 'API_KEY':self.ApiKey})
        else:
            url='https://www.googleapis.com/youtube/v3/comments?part=snippet&fields={fields}&maxResults={maxResults}&parentId={parentId}&textFormat={textFormat}&key={API_KEY}'.format(**{'fields':fields, 'parentId':parentId, 'maxResults':maxResults, 'textFormat':textFormat, 'API_KEY':self.ApiKey})
            
        res = []
        pageToken = ''
        for i in range(0, limit, maxResults):
            obj_json = self.download_json(url, pageToken)
            content =  obj_json
            res.extend(content['items'])
            if 'nextPageToken' in content:
                pageToken = content['nextPageToken']
            else:
                break
        self.result_raw = res
        res = res[:limit]        
        return res


    def get_search(self, q='', channelId='', playlistId='', order='date'):
        res = []
        url = ''
        pprint(url)
        return res
    

        
if __name__ == '__main__':
    yt = YoutubeApi('123')
    
    #yt._get_delta_list(dt1,dt2,part_by_day=True, part_by_month=False)
    #yt._get_delta_list(dt1,dt2, part=10, part_by_day=False, part_by_month=False)
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

    