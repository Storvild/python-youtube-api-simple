# Youtube-python-v3-simple
## Простой API для получения данных о контенте Youtube 

Используется: YouTube Data API v3    
Тестировалось на: Python 3.6.6

Для работы с Youtube API необходимо получить API_KEY в Google    
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
videos = yt.get_videos(playlistId='PLnP4EuRGIgUHuJ0wWST3aFzx0DsThs9Cm')

#### Получить список видео с определенного канала по ID-канала c 01.11.2019 по 15.11.2019
from datetime import datetime
videos = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A1', fromdate=datetime(2019,11,1), todate=datetime(2019,11,15))

#### Получить список видео по поисковой строке "квн" с лимитом записей 10 отсортированный по дате
videos = yt.get_videos(q='квн', limit=10, order='date')

#### Получить список видео с полной информацией о видео
videos = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A1', fullInfo=True)

#### Получить список видео с полной информацией о видео с определенными полями
videos = yt.get_videos(channelId='UC4iAuuvx9hJilx4QOcd8V6A1', fullInfo=True, fields='id,snippet(title,publishedAt),statistics,contentDetails')



#### Калькулятор квот:
[https://developers.google.com/youtube/v3/determine_quota_cost](https://developers.google.com/youtube/v3/determine_quota_cost)

