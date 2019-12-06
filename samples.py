from youtube_api.youtube_api_v3 import YoutubeApi
try:
    from settings import API_KEY
except:
    print("Внимание!!!\n  Создайте файл settings.py рядом с sample.py и запишите туда строку:\nAPI_KEY = '<Ваш API_KEY>'\n")
    print("API_KEY от Google можно получить здесь: https://console.developers.google.com/project\n")
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
#comments = yt.get_comments('7lqVYoKiMfw', fields='nextPageToken,items(id,snippet(videoId,topLevelComment(id,snippet(authorDisplayName,textDisplay,textOriginal,publishedAt,updatedAt,viewerRating))))')
#comments = yt.get_comments(id='Uggb3EPddGJet3gCoAEC')
#comments = yt.get_comments(parentId='Uggb3EPddGJet3gCoAEC')
#comments = yt.get_comments('268a2Gyq-fc')
#comments = yt.get_comments(id='UgyteV0exQnVVEnh7dh4AaABAg')
#comments = yt.get_comments(id='UgyteV0exQnVVEnh7dh4AaABAg', textFormat='plainText')
#comments = yt.get_comments(parentId='UgyteV0exQnVVEnh7dh4AaABAg')
#pprint(yt.result_raw)
#pprint(comments)

def _get_delta_list_test():
    from datetime import datetime
    dt1 = datetime(2019,3,6,10,30,0)
    dt2 = datetime.now()
    #dt2 = datetime(2019,12,6)
    #yt._get_delta_list(dt1,dt2,part=5)
    #yt.test(dt1,dt2,part_by_day=False, part_by_month=True)
    yt._get_delta_list(datetime(2019,3,15,10,20,0),datetime(2019,8,3,22,40,0),part_by='day')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,4,1,22,40,0),part_by='month')
    #yt._get_delta_list(datetime(2019,3,10,10,20,0),datetime(2019,3,13,22,40,0),part_by='month')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,6,1,22,40,0),part_by='month')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,6,30,23,59,59),part_by='month')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,6,1,0,0,0),part_by='month')
    #yt._get_delta_list(datetime(2015,3,31,10,20,0),datetime(2019,6,1,0,0,0),part_by='year')
    #yt._get_delta_list(datetime(2019,3,31,10,20,0),datetime(2019,6,10,10,31,0),part_by='year')
    #yt._get_delta_list(datetime(2018,12,31,23,59,59),datetime(2019,6,10,10,31,0),part_by='year')
    #yt._get_delta_list(datetime(2018,1,1,0,0,0),datetime(2019,6,10,10,31,0),part_by='year')
    #yt._get_delta_list(datetime(2018,1,1,0,0,0),datetime(2018,1,1,0,0,0),part_by='year')

_get_delta_list_test()

