import time
import datetime
import re
try:
    from . import utils
except:
    import utils


class YoutubeItem():
    def __init__(self, code, type, title, publishedAt, description=''):
        """
        Простой Youtube объект, содержащий только основные поля
          Результат запросов можно преобразовать к списку подобных объектов методом: yt.parse_yt_result(js)
        :param code: ID видео видео | ID канала | ID плейлиста | ID комментария
        :param type: Тип элемента
        :param title: Заголовок видео | Наименование плейлиста | Наименование канала | Автор комментария
        :param publishedAt: Дата публикации
        :param description: Описание видео | Описание канала | Описание плейлиста | Комментарий
        :type code: str
        :type type: str
        :type title:  str
        :type publishedAt: str
        :type description: str
        """
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
        return '{} {:15} {:30} {:20} {}'.format(self.type, utils.truncatechars(self.code, 15), utils.truncatechars(self.title,30), utils.truncatechars(self.description,20), self.publishedAt)


class YoutubeException(Exception):
    """ Класс исключения который вызывается, если получена ошибка Youtube в виде json:
        {'error': {'code': 400,
                   'errors': [{'domain': 'global',
                       'location': 'fields',
                       'locationType': 'parameter',
                       'message': 'Invalid field selection 1*',
                       'reason': 'invalidParameter'}],
                   'message': 'Invalid field selection 1*'}}
    """
    def __init__(self, message, response_url, response_content, page_token=''):
        super().__init__(message)
        self.message = message
        self.response_status = response_content['error']['code']
        self.response_content = response_content
        self.response_url = YoutubeException._clean_url(response_url)
        self.page_token = page_token
        self.error_raw = response_content
        self.domain = ''
        self.location = ''
        self.locationType = ''
        self.error_msg = ''
        self.error_count = len(response_content['error']['errors'])
        self.reason = ''
        if len(response_content['error']['errors'])>0:
            if 'domain' in response_content['error']['errors'][0]:
                self.domain = response_content['error']['errors'][0]['domain']
            if 'location' in response_content['error']['errors'][0]:
                self.location = response_content['error']['errors'][0]['location']
            if 'locationType' in response_content['error']['errors'][0]:
                self.locationType = response_content['error']['errors'][0]['locationType']
            if 'message' in response_content['error']['errors'][0]:
                self.error_msg = response_content['error']['errors'][0]['message']
            if 'reason' in response_content['error']['errors'][0]:
                self.reason = response_content['error']['errors'][0]['reason']
                if self.reason == 'keyInvalid':
                    self.message = 'Не верный ключ API_KEY'
                elif self.reason == 'commentsDisabled':
                    self.message = 'Комментарии отключены к данному видео'

    @staticmethod
    def _clean_url(url):
        """ Очистка URL от API_KEY """
        res = re.sub(r'[&]key=[^&]+', '', url)
        res = re.sub(r'[?]key=[^&]+&?', '?', res)
        return res

    def __str__(self):
        return '{}: {}\nSTATUS: {}\nJSON: {}\nURL: {}\nPageToken: {}'.format(self.message, self.error_msg, self.response_status, self.response_content, self.response_url, self.page_token)

    def __repr__(self):
        return '{}: {}\nSTATUS: {}\nJSON: {}\nURL: {}\nPageToken: {}'.format(self.message, self.error_msg, self.response_status, self.response_content, self.response_url, self.page_token)


class YoutubeApi():
    def __init__(self, ApiKey, timeout=0.2):
        """
        Класс для получения данных о видео, видео канала, плейлиста и т.д.
        :param ApiKey: API_KEY от Google
        :type ApiKey: str
        """
        assert ApiKey != '' or len(ApiKey) == 0, 'YoutubeApi: Необходимо указать API_KEY или список API_KEY'

        if type(ApiKey) == list:
            self.ApiKeyList = ApiKey
            self.ApiKey = ApiKey[0]
        else:
            self.ApiKey = ApiKey
            self.ApiKeyList = [ApiKey]
        self.timeout = timeout  # Пауза между запросами

    @staticmethod
    def _clean_url(url):
        """ Очистка URL от API_KEY """
        res = re.sub(r'[&]key=[^&]+', '', url)
        res = re.sub(r'[?]key=[^&]+&?', '?', res)
        return res

    def download_yt_json(self, url, pageToken=''):
        """
        Загрузка json из Youtube API (www.googleapis.com)

        :param url:  Скачивание json по данному URL
        :param pageToken: Токен вызываемой страницы
        :type url: str
        :type pageToken: str
        :return: Объект json
        Преобразует ошибки Youtube из json в исключение YoutubeException
        """

        if pageToken!='':
            url += '&pageToken={}'.format(pageToken)
        
        #res = fake_download(url, pageToken)

        res = utils.download_json(url)
        if 'error' in res:
            raise YoutubeException(message='download_yt_json: Ошибка обработки запроса', response_url=url, response_content=res, page_token=pageToken)
        return res

    def set_next_api_key(self):
        """ Если передан список API_KEY, то установить следующий API_KEY, пока не дойдет до конца списка """
        idx = self.ApiKeyList.index(self.ApiKey)
        idx += 1
        if idx > len(self.ApiKeyList) - 1:
            res = False
        else:
            self.ApiKey = self.ApiKeyList[idx]
            res = True
        return res

    def parse_yt_result(self, js):
        """
        Распарсить результат, выдаваемый Youtube в простую структуру с основными полями
        :param js: json, выдаваемый Youtube
        :return: Список объектов YoutubeItem
        :type js: object
        :rtype: list[YoutubeItem]
        """
        res = []
        for item in js:
            try:
                kind = ''
                if 'topLevelComment' in item['snippet']:
                    kind = 'youtube#commentThread'
                elif 'kind' in item and type(item['kind']) == str: # == 'youtube#comment':
                    kind = item['kind']
                    #kind = 'youtube#comment'
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
                elif kind == 'youtube#video':
                    if 'id' in item and type(item['id'])==str:
                        id = item['id']
                    elif 'id' in item and 'videoId' in item['id']:
                        id = item['id']['videoId']
                    elif 'id' in item and 'playlistId' in item['id']:
                        id = item['id']['playlistId']
                    else:
                        id = ''
                    obj = YoutubeItem(  code=id,
                                        type=item['kind'] if 'kind' in item else '',
                                        title=item['snippet']['title'] if 'snippet' in item and 'title' in item['snippet'] else '',
                                        publishedAt=item['snippet']['publishedAt'] if 'snippet' in item and 'publishedAt' in item['snippet'] else '',
                                        description=item['snippet']['description'] if 'snippet' in item and 'description' in item['snippet'] else '',
                                      )
                else:
                    if 'id' in item and type(item['id'])==str:
                        id = item['id']
                    elif 'id' in item and 'videoId' in item['id']:
                        id = item['id']['videoId']
                    elif 'id' in item and 'playlistId' in item['id']:
                        id = item['id']['playlistId']
                    else:
                        id = ''
                    kind = 'unknown'
                    title = item['snippet']['title'] if 'snippet' in item and 'title' in item['snippet'] else ''
                    publishedAt = item['snippet']['publishedAt'] if 'snippet' in item and 'publishedAt' in item['snippet'] else ''
                    description = item['snippet']['description'] if 'snippet' in item and 'description' in item['snippet'] else ''

                    obj = YoutubeItem(  code=id,
                                        type=kind,
                                        title=title,
                                        publishedAt=publishedAt,
                                        description=description,
                                      )
                if obj:
                    res.append(obj)
            except:
                print('Ошибка парсинга _result_parse !!!!')
            pass
        return res
    
    def _correct_part(self, part, fields):
        """
        Ф-ция убирает из part неиспользуемые поля, которых нет в fields

        :param part: Получаемые данные. Пример: 'id,snippet,statistics,contentDetails'
        :param fields: Поля которые будут содержаться в результ. json: 'id,snippet(title,publishedAt),contentDetails'
        :return: Новый список part Пример: 'id,snippet,contentDetails'
        """
        res = part
        if fields != '*':
            part_list = part.split(',')
            part_new = []
            for p in part_list:
                if p in fields or p == 'id':
                    part_new.append(p)
            res = ','.join(part_new)
        return res

    def get_channels(self, channelName, fields='*', limit=50, order='relevance', page_handler=None):
        """
        Поиск каналов по имени

        :param channelName:
        :param fields: Поля json которые необходимо оставить. В формате 'id,snippet(*)'
        :param limit: Лимит получаемых записей
        :param order: Сортировка 'date','rating','relevance','title','videoCount','viewCount'
        :param page_handler: Ф-ция вызываемая после каждого youtube запроса (постраничного)
        :return: Список каналов
        :type channelName: str
        :type fields: str
        :type limit: int
        :type order: str
        :type page_handler: function
        :rtype: list
        """

        assert order in ('date','rating','relevance','title','videoCount','viewCount'), 'get_playlists: Неправильный параметр order: {}'.format(order)
        assert channelName!='', 'get_playlists: Не задано имя канала (channelName)'
        if fields in ('','*'):
            fields = '*'
        elif 'nextPageToken' not in fields:
            fields = 'nextPageToken,items({})'.format(fields)
        
        maxResults = 50
        q = channelName
        part = 'snippet'
        url = 'https://www.googleapis.com/youtube/v3/search?type=channel&part={part}&fields={fields}' \
              '&maxResults={max_results}&order={order}&q={q}' \
              '&key={API_KEY}'.format(**{'part': part, 'fields': fields, 'max_results': maxResults, 'order':order, 'q': q, 'API_KEY': self.ApiKey})
        
        res = []
        pageToken = ''
        for i in range(0, limit, maxResults):
            obj_json = self.download_yt_json(url, pageToken)
            content =  obj_json
            res.extend(content['items'])

            if page_handler:
                yt_url = '{}&pageToken={}'.format(YoutubeApi._clean_url(url), pageToken)
                yt_params = {'url': yt_url, 'part': snippet, 'fields': fields, 'q': q, 'pageToken': pageToken,
                             'maxResults': maxResults, 'type': 'channel', 'order': order}
                params = {'i': i, 'limit': limit}
                do_continue = page_handler(content=content['items'], content_raw=content, yt_params=yt_params, params=params)
                if do_continue is False:
                    break

            if 'nextPageToken' in content:
                pageToken = content['nextPageToken']
                time.sleep(self.timeout)
            else:
                break        
        res = res[:limit]
        return res

    def get_channels_info(self, channelId='', forUsername='', part='id,snippet,statistics', fields='*', limit=50, order='relevance', page_handler=None):
        """
        Информация о каналах перечисленных в channelId через запятую или нахождение каналов пользователя forUsername

        :param channelId: ID Youtube-канала или список через запятую
        :param forUsername: Имя пользователя для поиска созданных им каналов
        :param part: id,snippet,statistics,status,contentDetails,contentOwnerDetails,localizations,topicDetails,auditDetails,brandingSettings
        :param fields: Поля json которые необходимо оставить. В формате 'id,snippet(*)'
        :param limit: Лимит получаемых записей
        :param order: Сортировка 'date','rating','relevance','title','videoCount','viewCount'
        :param page_handler: Ф-ция вызываемая после каждого youtube запроса (постраничного)
        :return: Список каналов
        :type channelName: str
        :type fields: str
        :type limit: int
        :type order: str
        :type page_handler: function
        :rtype: list
        """
        # part = 'id,snippet,statistics,status,contentDetails,contentOwnerDetails,localizations,topicDetails,auditDetails,brandingSettings'
        if fields in ('', '*'):
            fields = '*'
        elif 'nextPageToken' not in fields:
            fields = 'nextPageToken,items({})'.format(fields)

        maxResults = 50
        channel_ids = channelId
        if channelId:
            url = 'https://www.googleapis.com/youtube/v3/channels?part={part}&fields={fields}' \
                  '&maxResults={max_results}&key={API_KEY}'.format(
                **{'channel_id': channelId, 'part': part, 'fields': fields, 'max_results': maxResults, 'API_KEY': self.ApiKey})
            if type(channelId) == str:
                channel_ids = channelId.split(',')
        elif forUsername:
            url = 'https://www.googleapis.com/youtube/v3/channels?forUsername={for_username}&part={part}&fields={fields}' \
                  '&maxResults={max_results}&key={API_KEY}'.format(
                **{'for_username': forUsername, 'part': part, 'fields': fields, 'max_results': maxResults, 'API_KEY': self.ApiKey})
        else:
            raise Exception('Должно быть заполнено хотя бы одно поле: channelId (ID канала) или forUsername (пользователь)')


        res = []
        pageToken = ''
        for i in range(0, limit, maxResults):
            url_ = url
            if channelId:
                url_ = '{}&id={}'.format(url, ','.join(channel_ids[i:i+maxResults]))
            obj_json = self.download_yt_json(url_, pageToken)
            content = obj_json
            res.extend(content['items'])

            if page_handler:
                yt_url = '{}&pageToken={}'.format(YoutubeApi._clean_url(url), pageToken)
                yt_params = {'url': yt_url, 'part': snippet, 'fields': fields, 'pageToken': pageToken,
                             'maxResults': maxResults }
                params = {'i': i, 'limit': limit}
                do_continue = page_handler(content=content['items'], content_raw=content, yt_params=yt_params,
                                           params=params)
                if do_continue is False:
                    break

            if 'nextPageToken' in content:
                pageToken = content['nextPageToken']
                time.sleep(self.timeout)
            else:
                break
        res = res[:limit]
        return res

    def get_playlists(self, channelId, fields='*', limit=50, order='date', page_handler=None):
        """
        Получить плейлисты определенного канала (cost:100/страницу)

        :param channelId: ID канала
        :param fields: Поля json
        :param limit: Лимит получения записей
        :param order: Сортировка 'date','rating','relevance','title','videoCount','viewCount'
        :param page_handler: Ф-ция вызываемая после каждого youtube запроса (постраничного)
        :return: Список плейлистов
        :type channelId: str
        :type fields: str
        :type limit: int
        :type order: str
        :type page_handler: function
        :rtype: list
        """
        assert order in ('date','rating','relevance','title','videoCount','viewCount'), 'get_playlists: Неправильный параметр order: {}'.format(order)
        assert channelId!='', 'get_playlists: Не задан Id канала (channelId)'
        if fields in ('','*'):
            fields = '*'
        elif 'nextPageToken' not in fields:
            fields = 'nextPageToken,items({})'.format(fields)
            
        maxResults = 50
        part = 'snippet'
        url = 'https://www.googleapis.com/youtube/v3/search?type=playlist&part={part}&fields={fields}' \
              '&channelId={channel_id}&maxResults={max_results}&order={order}' \
              '&key={API_KEY}'.format(**{'part': part, 'fields': fields, 'channel_id': channelId, 'max_results': maxResults, 'order': order, 'API_KEY': self.ApiKey})
        
        res = []
        pageToken = ''
        for i in range(0, limit, maxResults):
            obj_json = self.download_yt_json(url, pageToken)
            content =  obj_json
            res.extend(content['items'])

            if page_handler:
                yt_url = '{}&pageToken={}'.format(YoutubeApi._clean_url(url), pageToken)
                yt_params = {'url': yt_url, 'type': 'playlist', 'channelId': channelId, 'part': part,
                             'fields': fields, 'pageToken': pageToken, 'maxResults': maxResults, 'order': order}
                params = {'i': i, 'limit': limit}
                do_continue = page_handler(content=content['items'], content_raw=content, yt_params=yt_params, params=params)
                if do_continue is False:
                    break

            if 'nextPageToken' in content:
                pageToken = content['nextPageToken']
                time.sleep(self.timeout)
            else:
                break

        res = res[:limit]
        return res

    def get_comments(self, videoId='', id='', parentId='', fields='*', limit=100, order='relevance', textFormat='html', page_handler=None):
        """ Получение комментариев к видео, комментария по id или ответы на указанный комментарий

            Обязательно заполнить один из параметров videoId или id или parentId
            :params videoId:  Комментарии к видео
            :params id:       id комментария или список id через запятую
            :params parentId: Ответы на комментарий (id)
            :params order:    Сортировка relevance или date
            :params textFormat: Формат текста в textDisplay - plainText или html (В поле textOriginal только текст)
            :params page_handler: Ф-ция вызываемая при получении порции данных
        """

        assert videoId!='' or id!='' or parentId!='', 'Должен быть заполнен один из параметров videoId, id или parentId'

        if fields in ('', '*'):
            fields = '*'
        elif 'nextPageToken' not in fields: # Если не передано обязательное поле nextPageToken, значит перечисляются только поля в items
            fields = 'nextPageToken,items({})'.format(fields)

        maxResults = 100  # По умолчанию 100
        if limit<100:
            maxResults = limit

        url = ''
        part = 'snippet'
        if videoId:
            url = 'https://www.googleapis.com/youtube/v3/commentThreads?part={part}&fields={fields}' \
                '&maxResults={maxResults}&videoId={videoId}&textFormat={textFormat}&order={order}' \
                '&key={API_KEY}'.format(**{'part': part, 'fields': fields, 'videoId': videoId,
                                           'maxResults': maxResults, 'textFormat': textFormat, 'order': order,
                                           'API_KEY': self.ApiKey})
        elif id:
            url = 'https://www.googleapis.com/youtube/v3/comments?part={part}&fields={fields}' \
                  '&maxResults={maxResults}&id={id}&textFormat={textFormat}&order={order}' \
                  '&key={API_KEY}'.format(**{'part': part, 'fields': fields, 'id': id, 'maxResults':maxResults,
                                             'textFormat':textFormat, 'order':order,
                                             'API_KEY': self.ApiKey})
        elif parentId:
            url = 'https://www.googleapis.com/youtube/v3/comments?part={part}&fields={fields}' \
                  '&maxResults={maxResults}&parentId={parentId}&textFormat={textFormat}&order={order}' \
                  '&key={API_KEY}'.format(**{'part': part, 'fields': fields, 'parentId': parentId,
                                             'maxResults': maxResults, 'textFormat': textFormat, 'order': order,
                                             'API_KEY': self.ApiKey})

        res = []
        errors = []
        pageToken = ''
        try:
            for i in range(0, limit, maxResults):
                obj_json = self.download_yt_json(url, pageToken)
                content = obj_json
                res.extend(content['items'])

                if page_handler:
                    yt_url = '{}&pageToken={}'.format(YoutubeApi._clean_url(url), pageToken)
                    yt_params = {'url': yt_url, 'id': id, 'videoId': videoId, 'parentId': parentId,
                                 'part': part, 'fields': fields, 'pageToken': pageToken, 'maxResults': maxResults,
                                 'order': order, 'textFormat': textFormat}
                    params = {'i': i, 'limit': limit}
                    do_continue = page_handler(content=content['items'], content_raw=content, yt_params=yt_params, params=params)

                    if do_continue is False:
                        break

                if 'nextPageToken' in content:
                    pageToken = content['nextPageToken']
                    time.sleep(self.timeout)
                else:
                    break
        except Exception as e:
            errors.append(e)
            print('Ошибка при получении комментариев')
        res = res[:limit]
        res = {'items': res, 'errors': errors}
        return res

    def get_videos_info(self, videoIDs, fields='*', part='id,snippet,statistics,contentDetails', limit=50, page_handler=None, add_comments=False, comments_limit=100, add_timecodes=False):
        """
        Получение расширенной информации о видео или списке видео

        :param videoIDs: ID получаемого видео или список ID через запятую в виде строки или списка python
        :param fields: Какие поля оставить в результирующем json. fields='*' - все поля. Пример
                    fields='items(id,contentDetails,snippet(title,publishedAt,channelId,channelTitle,description),statistics'
        :param part: получение информации о видео (snippet), лайки/дизлайки (statistics), длительность видео (contentDetails)
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
        :param limit: Лимит количества получаемых записей
        :param page_handler: Ф-ция вызываемая после каждого youtube запроса (постраничного)
        :param add_comments: Получать комментарии
        :param comments_limit: Максимальное кол-во получаемых комментариев. Поддерживается максимум 100
        :param add_timecodes: Искать таймкоды в комментариях. Ищется первый комментарий в котором хотябы 2 раза
            повторяется время "8:12 любой текст \n20:25"
        :return: Список видео в виде структуры json с подробной информацией
        :type videoIDs: str|list
        :type fields:  str
        :type part:  str
        :type limit: int
        :type page_handler: function(content: list, content_raw: dict, yt_params: dict, params: dict)
        :type add_comments: bool
        :type comments_limit: int
        :type add_timecodes: bool
        :rtype: dict
        """

        assert type(videoIDs) in (list, tuple, set, str)
        assert comments_limit <= 100

        maxResults = 50
        res = []
        deleted = []
        errors = []

        if fields in ('', '*'):
            fields = '*'
        elif 'nextPageToken' not in fields: # Если не передано обязательное поле nextPageToken, значит перечисляются только поля в items
            fields = 'nextPageToken,items({})'.format(fields)
            # Если в fields переданы поля, убираем из part неиспользуемые
            part = self._correct_part(part, fields)

        # Если videoIDs не является списком, преобразуем в список
        if type(videoIDs) == str:
            videoIDs = videoIDs.split(',')

        done = False
        for i in range(0, len(videoIDs), maxResults):
            error_get_content = True  # Для повторного получения, если произошла ошибка
            if done:
                break
            while error_get_content:
                try:

                    ids = ','.join(videoIDs[i:i+maxResults])
                    url = 'https://www.googleapis.com/youtube/v3/videos?part={part}&fields={fields}&id={ids}' \
                          '&maxResults={maxResults}&key={API_KEY}'.format(**{'part': part, 'fields': fields, 'ids': ids,'maxResults': maxResults, 'API_KEY': self.ApiKey})
                    content = self.download_yt_json(url)

                    # ЗДЕСЬ ДОЛЖЕН БЫТЬ КОД ДЛЯ ПОМЕТКИ УДАЛЕННЫХ. Сравниваем videoIDs[i:i+maxResults] и content
                    query_codes = videoIDs[i:i+maxResults]
                    response_codes = [x['id'] for x in content['items']]
                    deleted_page = set(query_codes) - set(response_codes)
                    deleted.extend(deleted_page)

                    #from pprint import pprint
                    #pprint(query_codes)
                    #pprint(response_codes)
                    #pprint(deleted_page)

                    if add_comments or add_timecodes:
                        for item in content['items']:
                            videoId = item['id']
                            # Иниациализация полей комментариев и таймкодов
                            if add_comments:
                                item['comments'] = []
                            if add_timecodes:
                                item['timecodes'] = ''
                            try:
                                comments = self.get_comments(videoId=videoId, limit=comments_limit)
                                errors.extend(comments['errors'])
                                if add_comments:
                                    item['comments'] = comments['items']
                                if add_timecodes:
                                    for comment in comments['items']:
                                        comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
                                        item['timecodes'] = ''
                                        if re.search('\d{1,2}:\d{2}.*\d{1,2}:\d{2}', comment_text, re.MULTILINE | re.DOTALL):
                                            item['timecodes'] = utils.clean_text(comment_text)
                                            break
                            except Exception as e:
                                errors.append(e)

                    res.extend(content['items'])
                    if page_handler:
                        yt_url = '{}'.format(YoutubeApi._clean_url(url))
                        yt_params = {'url': yt_url, 'id': ids, 'part': part, 'fields': fields, 'pageToken': '',
                                     'maxResults': maxResults}
                        params = {'i': i, 'limit': limit}
                        do_continue = page_handler(content=content['items'], content_raw=content, yt_params=yt_params, params=params)
                        if do_continue is False:
                            done = True
                            break

                    if (i+maxResults)>limit and limit>0:
                        done = True
                        break

                    error_get_content = False  # Завершено без ошибок
                except YoutubeException as e:
                    error_get_content = False  # По умолчанию повторно не перезапрашивать данные
                    if e.reason in ('quotaExceeded', 'dailyLimitExceeded'):
                        if self.set_next_api_key():  # Если получен следующий API_KEY, то установить его
                            error_get_content = True     # Повторно получить данные
                            print('Квота превышена, переключение на следующий API_KEY и перезапрос...')
                    else:
                        print('Ошибка:', str(e))
                    errors.append(e)
                except Exception as e:
                    errors.append(e)


        res = res[:limit]
        res = {'items': res, 'deleted': deleted, 'errors': errors}
        return res

    def get_videos(self, q='', channelId='', playlistId='', videoId='', fromdate=None, todate=None, limit=50, partion_by='1',
                   part='id,snippet,contentDetails,statistics', fields='*', order='date', fullInfo=False,
                   page_handler=None, video_handler=None,
                   add_comments=False, comments_limit=100, add_timecodes=False):
        """
        Получение списка видео с канала (channelId), плейлиста (playlistId) или по поиску (q)
        (cost=100/страницу + при fullInfo=True 3*каждый параметр)

        Формат ф-ции обратного вызова:
            def my_page_handler(content, content_raw, yt_params, params)

        :param q: Поисковая строка
        :param channelId: ID канала
        :param playlistId: ID плейлиста
        :param fromdate: Начальная дата (может быть None)
        :param todate: Конечная дата (может быть None)
        :param limit: Лимит записей (Максимум 1000 (Ограничение Youtube 50 записей на странице, всего 20 страниц)
        :param part: показываемая информация
        :param fields: поля в резултирующем json
        :param order: Сортировка 'date','rating','relevance','title','videoCount','viewCount'
        :param fullInfo: Получать ли полную информацию (
        :param page_handler: Ф-ция вызываемая после каждого youtube запроса (постраничного)
            Параметры:  content - Список словарей с данными Youtube
                        content_raw - Полученный из Youtube необработанный json (словарь с вложенным списком видео)
                        yt_params - Словарь с параметрами передаваемыми в запросе youtube + url
                        params - Параметры i, limit с внутренними данными (индекс итерации и лимит получения)
        :param video_handler: Ф-ция вызываемая после каждого запроса подробной информации по видео или набору видео
            Параметры:  content - Список словарей с данными Youtube
                        content_raw - Полученный из Youtube необработанный json (словарь с вложенным списком видео)
                        yt_params - Словарь с параметрами передаваемыми в запросе youtube + url
                        params - Параметры i, limit с внутренними данными (индекс итерации и лимит получения)
        :param add_comments: Получать комментарии (работает только если включен параметр fullInfo) По умолчанию False
        :param comments_limit: Максимальное кол-во получаемых комментариев. Поддерживается максимум 100
        :param add_timecodes: Искать таймкоды в комментариях. Ищется первый комментарий в котором хотябы 2 раза
            повторяется время. Пример: "8:12 любой текст \n20:25"
            (работает только если включен параметр fullInfo)
        :return: Список видео в json структуре: {'items': [], 'errors': [], 'deleted': []}
        :type q: str
        :type channelId: str
        :type playlistId: str
        :type fromdate: datetime.datetime|str
        :type todate: datetime.datetime|str
        :type limit: int
        :type part: str
        :type fields: str
        :type order: str
        :type fullInfo: bool
        :type page_handler: function(list, dict, dict, dict)
        :type video_handler: function(list, dict, dict, dict)
        :type add_comments: bool
        :type comments_limit: int
        :type add_timecodes: bool
        :rtype: dict
        """

        # Если передан videoId с одним или несколькими кодами, то выполнить метод get_videos_info и вернуть результат
        if videoId:
            if not fullInfo:
                part = 'id,snippet'
            res = self.get_videos_info(videoIDs=videoId, fields=fields, part=part, limit=limit,
                                       page_handler=video_handler,
                                       add_comments=add_comments, comments_limit=comments_limit, add_timecodes=add_timecodes)
            if page_handler:
                if type(videoId) == list:
                    videoId = ','.join(videoId)
                yt_url = 'https://www.googleapis.com/youtube/v3/videos?part={part}&fields={fields}&id={ids}' \
                          '&maxResults={maxResults}'.format(**{'part': part, 'fields': fields, 'ids': videoId,
                                                               'maxResults': 50})
                yt_params = {'url': yt_url, 'q': '', 'channelId': '', 'playlistId': '', 'videoId': videoId,
                             'fromdate': fromdate, 'todate': todate, 'part': part, 'fields': fields, 'pageToken': '',
                             'maxResults': 50}
                page_handler(content=res, content_raw=res, yt_params=yt_params, params={})
            return res


        part_main = 'id,snippet'
        if fullInfo:
            #fields = 'nextPageToken,pageInfo,items(id,snippet(title,publishedAt,channelTitle,channelId))'
            fields_main = 'nextPageToken,pageInfo,items(id)'
        else:
            fields_temp = fields.replace(',contentDetails', '').replace(',statistics', '')
            if fields in ('', '*'):
                fields_main = '*'
            elif 'nextPageToken' not in fields_temp:  # Если не передано обязательное поле nextPageToken, значит перечисляются только поля в items
                fields_main = 'nextPageToken,pageInfo,items({})'.format(fields_temp)
            else:
                fields_main = fields_temp  # Если передали nextPageToken, то вставляем без изменений

        maxResults = 50  # Количество объектов на 1 запрос. Максимум = 50

        res = []
        errors = []
        deleted = []  # В данном случае удаленных видео быть не может, т.к. это поиск видео, но оставлено для совместимости

        datepart_list = [{'fromdate': fromdate, 'todate': todate}]
        if partion_by not in ('', '1', 1, 0):
            datepart_list = utils.date_period_into_parts(fromdate, todate, partion_by=partion_by)

        for datepart in datepart_list:

            published = ''
            if datepart['fromdate']:
                if type(datepart['fromdate']) == str:
                    published += '&publishedAfter={}'.format(datepart['fromdate']) #2019-01-01T00:00:00Z
                elif type(datepart['fromdate']) == datetime.date:
                    published += '&publishedAfter={}Z'.format(datetime.datetime.fromordinal(datepart['fromdate'].toordinal()).replace(microsecond=0).isoformat(sep='T'))  # 2019-01-01T00:00:00Z
                else:
                    published += '&publishedAfter={}Z'.format(datepart['fromdate'].replace(microsecond=0).isoformat(sep='T'))
            if datepart['todate']:
                if type(datepart['todate']) == str:
                    published += '&publishedBefore={}'.format(datepart['todate']) #2019-12-31T23:59:59Z
                elif type(datepart['todate']) == datetime.date:
                    published += '&publishedAfter={}Z'.format(datetime.datetime.fromordinal(datepart['todate'].toordinal()).replace(microsecond=0).isoformat(sep='T'))  # 2019-01-01T00:00:00Z
                else:
                    published += '&publishedBefore={}Z'.format(datepart['todate'].replace(microsecond=0).isoformat(sep='T'))

            try:
                pageToken = ''
                done = False # Для выхода из вложенных циклов
                for i in range(0, limit, maxResults):
                    if done:
                        break
                    error_get_content = True  # Для повторного получения, если произошла ошибка
                    while error_get_content:
                        try:
                            if playlistId:
                                url = 'https://www.googleapis.com/youtube/v3/playlistItems?part={part}' \
                                      '&fields=nextPageToken,pageInfo,items(id,snippet)&playlistId={playlistId}&maxResults={maxResults}' \
                                      '&key={API_KEY}'.format(
                                       **{'part': part_main, 'fields': fields_main, 'playlistId': playlistId,
                                       'maxResults': maxResults, 'API_KEY': self.ApiKey})
                            elif channelId:
                                url = 'https://www.googleapis.com/youtube/v3/search?type=video&part={part}&fields={fields}' \
                                      '&channelId={channelId}&maxResults={maxResults}&order={order}{published}' \
                                      '&key={API_KEY}'.format(
                                       **{'part': part_main, 'fields': fields_main, 'channelId': channelId,
                                       'maxResults': maxResults, 'order': order, 'published': published,
                                       'API_KEY': self.ApiKey})
                            else:
                                url = 'https://www.googleapis.com/youtube/v3/search?type=video&part={part}&fields={fields}' \
                                      '&q={q}&maxResults={maxResults}&order={order}{published}' \
                                      '&key={API_KEY}'.format(
                                       **{'part': part_main, 'fields': fields_main, 'q': q, 'maxResults': maxResults,
                                       'order': order, 'published': published, 'API_KEY': self.ApiKey})

                            content = self.download_yt_json(url, pageToken)
                            if fullInfo:
                                fields_full = fields
                                if fields in ('', '*'):
                                    fields_full = '*'
                                elif 'nextPageToken' not in fields:  # Если не передано обязательное поле nextPageToken, значит перечисляются только поля в items
                                    fields_full = 'nextPageToken,pageInfo,items({})'.format(fields)

                                # Если в fields переданы поля, убираем из part неиспользуемые
                                part_new = self._correct_part(part, fields_full)

                                if playlistId:
                                    ids = [x['snippet']['resourceId']['videoId'] for x in content['items']]
                                else:
                                    ids = [x['id']['videoId'] for x in content['items']]
                                videos = self.get_videos_info(ids, fields=fields_full, part=part_new, add_comments=add_comments,
                                                              comments_limit=comments_limit, add_timecodes=add_timecodes,
                                                              page_handler=video_handler)
                                res.extend(videos['items'])
                                deleted.extend(videos['deleted'])
                                errors.extend(videos['errors'])
                            else:
                                res.extend(content['items'])

                            if page_handler:
                                yt_url = '{}&pageToken={}'.format(YoutubeApi._clean_url(url), pageToken)
                                yt_params = {'url': yt_url, 'q': q, 'channelId': channelId, 'playlistId': playlistId,
                                             'fromdate': datepart['fromdate'], 'todate':datepart['todate'], 'part': part, 'fields': fields, 'pageToken': pageToken, 'maxResults': maxResults}
                                params = {'i': i, 'limit': limit}
                                do_continue = page_handler(content=content['items'], content_raw=content, yt_params=yt_params, params=params)
                                if do_continue is False:
                                    done = True
                                    break

                            if 'nextPageToken' in content:
                                pageToken = content['nextPageToken']
                                time.sleep(self.timeout)
                            else:
                                done = True
                                break

                            error_get_content = False  # Ошибок не произошло
                        except YoutubeException as e:
                            error_get_content = False  # По умолчанию повторно не перезапрашивать данные
                            if e.reason in ('quotaExceeded', 'dailyLimitExceeded'):
                                if self.set_next_api_key():  # Если получен следующий API_KEY, то установить его
                                    error_get_content = True     # Повторно получить данные
                                    print('Квота превышена, переключение на следующий API_KEY и перезапрос...')
                            else:
                                print('Ошибка:', str(e))
                            errors.append(e)

                        except Exception as e:
                            errors.append(e)

            except Exception as e:
                errors.append(e)
                print('Ошибка:', str(e))

        res = res[:limit]
        res = {'items': res, 'deleted': deleted, 'errors': errors}
        return res


if __name__ == '__main__':
    from pprint import pprint
    #from datetime import datetime
    #yt = YoutubeApi('123')
    yt = YoutubeApi('AIzaSyBuGHA5Ibmqk-ipJPLgrzgTGYk9VBhGlBA')
    #res = yt.get_videos_info('T1MjZZM7wOo,dse6AlZROY0,vZ9fWqNYLVE,KL2AiTb2UnQ', fields='id,snippet(title, channelTitle, channelId, publishedAt)', add_timecodes=True, add_comments=False, comments_limit=3)
    #res = yt.get_videos(videoId='T1MjZZM7wOo,dse6AlZROY0,vZ9fWqNYLVE,KL2AiTb2UnQ', fields='id,snippet(title, channelTitle, channelId, publishedAt)', add_timecodes=True, add_comments=False, comments_limit=3)
    def ph_func(content, content_raw, yt_params, params):
        print(yt_params['url'])
    res = yt.get_videos(partion_by='month', channelId='UCudnwGsIfsKmrkb2YKgW1CA', fields='id,snippet(title, channelTitle, channelId, publishedAt)', fromdate=datetime.datetime(2019,10,6), todate=datetime.datetime.now(), add_timecodes=True, add_comments=False, comments_limit=3, page_handler=ph_func)
    #pprint(res)

    #help(YoutubeApi)


# WISH
# Пометка удаленных видео. Если был запрос с id, а в результатах запроса его нет, то помечать видео как deleted
# + Пропуск ошибок
# str_to_datetime
# datetime_to_str
# + Сделать список API_KEY, по которому в случае ошибки менять на следующий и попытаться снова получить данные
# Сделать get_videos_info внутренним методом и использовать только get_videos
# + Ошибки складывать в errors
# + Результат метода get_videos_info - {'items'=[], errors=[], deleted=[]}