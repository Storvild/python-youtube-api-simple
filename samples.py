from youtube_api.youtube_api_v3 import YoutubeApi
from settings import API_KEY
from pprint import pprint

yt = YoutubeApi(API_KEY)

# Получение плейлистов с канала:
#playlists = yt.get_playlists('UC4iAuuvx9hJilx4QOcd8V6A1')
#print('\nПлейлисты:')
#pprint(playlists)

# Получение каналов по названию
# Может потребоваться для получения id канала
# Id канала будет в item['id']['channelId']
#channels = yt.get_channels('квн', limit=3)
# Получить каналы в которых будут указаны определенные поля
#channels = yt.get_channels('квн', fields='nextPageToken,items(id,snippet(title,channelId,channelTitle,description,publishedAt))', limit=3)
#channels = yt.get_channels('квн', fields='id,snippet(title,channelId,channelTitle,description,publishedAt)', limit=3)
#channels = yt.get_channels('квн', fields='id', limit=3)
#print('Найденные каналы:')
#pprint(channels)

#videos = yt.get_videos_info(['7lqVYoKiMfw','7LeO_r8_L3k'])
#videos = yt.get_videos_info('7lqVYoKiMfw,7LeO_r8_L3k,_-pPLzyplS0,4ZMv35U9oYw,MHebByfQ_nc,lBcAmL8jX-Y,psDAuK8TduQ', fields='id,snippet(title,publishedAt),contentDetails,statistics')
#videos = yt.get_videos_info('7lqVYoKiMfw,7LeO_r8_L3k,_-pPLzyplS0,4ZMv35U9oYw,MHebByfQ_nc,lBcAmL8jX-Y,psDAuK8TduQ', fields='id,snippet(title,publishedAt)')
#videos = yt.get_videos_info(['7lqVYoKiMfw','7LeO_r8_L3k','_-pPLzyplS0','4ZMv35U9oYw','MHebByfQ_nc','lBcAmL8jX-Y','psDAuK8TduQ'], part='id', fields='id')
#videos = yt.get_videos_info(['7lqVYoKiMfw','7LeO_r8_L3k','_-pPLzyplS0','4ZMv35U9oYw','MHebByfQ_nc','lBcAmL8jX-Y','psDAuK8TduQ'], part='id', fields='id', limit=5)
#pprint(videos)

#comments = yt.get_comments('7lqVYoKiMfw')
#comments = yt.get_comments(id='Uggb3EPddGJet3gCoAEC')
#comments = yt.get_comments(parentId='Uggb3EPddGJet3gCoAEC')
#comments = yt.get_comments('268a2Gyq-fc')
#comments = yt.get_comments(id='UgyteV0exQnVVEnh7dh4AaABAg')
#comments = yt.get_comments(id='UgyteV0exQnVVEnh7dh4AaABAg', textFormat='plainText')
comments = yt.get_comments(parentId='UgyteV0exQnVVEnh7dh4AaABAg')
pprint(comments)
