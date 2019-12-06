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

