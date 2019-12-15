# Youtube-python-v3-simple
## Простой API для получения данных о контенте Youtube 

Используется: YouTube Data API v3    
Тестировалось на: Python 3.6.6

#### Для работы с Youtube API необходимо получить API_KEY в Google    
1. Зарегистрироваться на сайте [console.developers.google.com/project](https://console.developers.google.com/project)   
2. Создать новый проект    
3. Активировать Youtube Data API на странице [console.developers.google.com/apis/library/youtube.googleapis.com](https://console.developers.google.com/apis/library/youtube.googleapis.com)    
4. Ключ будет виден в разделе "Учетные данные" [console.developers.google.com/apis/credentials](https://console.developers.google.com/apis/credentials)    

### Использование:

```python    
from youtube_api.youtube_api_v3 import YoutubeApi    
yt = YoutubeApi('<API_KEY>')    
playlists = yt.get_playlists('<channelId>')    
```

#### Получение плейлистов с канала:    
```python    
playlists = yt.get_playlists('UC4iAuuvx9hJilx4QOcd8V6A1')    
```

#### Получение каналов по названию    
```python    
channels = yt.get_channels('квн', limit=3)    
```

#### Получить каналы по названию в которых будут указаны определенные поля    
```python    
fields = 'id,snippet(title,channelId,channelTitle,description,publishedAt)'
channels = yt.get_channels('квн', fields=fields, limit=3)    
```

#### Получить комментарии    
```python    
# Получить комментарии к видео    
comments = yt.get_comments(videoId='268a2Gyq-fc')    
# Получить комментарий с определенным id или несколькими id через запятую    
comments = yt.get_comments(id='Uggb3EPddGJet3gCoAEC')    
# Получить ответы на комментарии    
comments = yt.get_comments(parentId='Uggb3EPddGJet3gCoAEC')    
```

#### Получить список видео с определенного плейлиста
```python    
videos = yt.get_videos(playlistId='PLnP4EuRGIgUHuJ0wWST3aFzx0DsThs9Cm')
```

#### Получить список видео с определенного канала по ID-канала c 01.11.2019 по 15.11.2019
```python    
from datetime import datetime
videos = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A1', 
                       fromdate=datetime(2019,11,1), todate=datetime(2019,11,15))
```

#### Получить список видео по поисковой строке "квн" с лимитом записей 10 отсортированный по дате
```python    
videos = yt.get_videos(q='квн', limit=10, order='date')
```

#### Получить список видео с полной информацией о видео
```python    
videos = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A1', fullInfo=True)
```

#### Получить список видео с полной информацией о видео с определенными полями
```python    
videos = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A1', fullInfo=True,
                       fields='id,snippet(title,publishedAt),statistics,contentDetails')
```

#### Максимальное кол-во информации выдаваемой Youtube до 1000 записей (максимальное кол-во на странице 50 * максимально кол-во страниц 20)
Для обхода данного ограничения можно воспользоваться методом get_videos_partion
Пример получения видео с канала UCSZ69a-0I1RRdNssyttBFcA, максимальное кол-во записей 100, период с 1.12.2019 10:30 по 8.12.2019 00:00 по одному дню на запрос
```python
from datetime import datetime
videos = yt.get_videos_partion(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, 
        fromdate=datetime(2019,12,1,10,30), todate=datetime(2019,12,8), partion_by='day')
```
Здесь limit - это лимит записей на каждый запрошенный день

Пример получения видео с разбивкой на 5 запросов (если на один запрос приходит более 50 записей, дополнительно запрашивается следующая страница)
```python
from datetime import datetime
videos = yt.get_videos_partion(channelId='UCSZ69a-0I1RRdNssyttBFcA', limit=100, 
        fromdate=datetime(2019,12,1,10,30), todate=datetime(2019,12,8), partion_by=5)
```        
Здесь limit - это лимит записей на каждую запрашиваемую часть

#### Вмешательство в постраничное получение данных
Если необходимо обрабатывать получение каждой страницы которое вызывается внутри методов, то можно воспользоваться ф-цией обратного вызова page_handler
Пример:
```python
def videos_partion_handler(content, content_raw, yt_params, params):
    print('i =', params['i'], 'limit=', params['limit'], 'pageToken=', yt_params['pageToken'], 'maxResults=',
          yt_params['maxResults'], 'fromdate=', yt_params['fromdate'], 'todate=', yt_params['todate'])
    return True

from datetime import datetime
obj = self.yt.get_videos_partion(fromdate=datetime(2019,1,30,10,30), todate=datetime(2019,2,3), limit=50,
                                 partion_by='day', page_handler=videos_partion_handler)
```
Ф-ция videos_partion_handler будет вызываться каждый раз после получения новой порции записей из youtube. В yt_params указан запрашиваемый url, и отдельно параметры.
Если при каких то условиях вам необходимо прервать процедуру получения данных, то возвращайте return False


#### Регулирование квот
При получении данных через Youtube API, действуют ограничения (квоты), которые установил Youtube
Например, c 2019 года, при создании приложения, квота составляет 10 000 единиц 
Один вызов videos с максимальным кол-вом видео = 50 занимает 1 единицу + несколько единиц в зависимости от того, что написано в part
Пример: yt.get_videos_info(videoIDs='<videoCode1,videoCode2...>', limit=50, part='id,snippet,contentDetais') в данном API) занимает 5 единиц
Если в part находятся другие поля, то затраты изменятся исходя из того какие из них в нем находятся:
* contentDetails: 2
* fileDetails: 1
* id: 0
* liveStreamingDetails: 2
* localizations: 2
* player: 0
* processingDetails: 1
* recordingDetails: 2
* snippet: 2
* statistics: 2
* status: 2
* suggestions: 1
* topicDetails: 2

Метод yt.get_videos затрачивает 100 единиц на одну страницу, если это поиск видео на канале или по поисковой строке.
Если это поиск видео в плейлисте, то затрачивается 3 единицы на 1 страницу
При параметре fullInfo=True в get_videos_info, изначальные затраты в 100 единиц еще увеличиваются согласно тому какие поля перечислены в part
Получение комментариев (get_comments) затрачивает около 3 единиц на 1 страницу
Получение каналов или плейлистов get_channels, get_playlists затрачивают 100 единиц на одну страницу

#### Калькулятор квот:
[https://developers.google.com/youtube/v3/determine_quota_cost](https://developers.google.com/youtube/v3/determine_quota_cost)

