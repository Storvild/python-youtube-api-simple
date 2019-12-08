from youtube_api.youtube_api_v3 import YoutubeApi
try:
    from settings import API_KEY
except:
    print("Внимание!!!\n  Создайте файл settings.py рядом с sample.py и запишите туда строку:\nAPI_KEY = '<Ваш API_KEY>'\n")
    print("API_KEY от Google можно получить здесь: https://console.developers.google.com/project\n")
from pprint import pprint
import os
import json

os.chdir(os.path.dirname(__file__)) # Работаем в текущем каталоге

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



yt = YoutubeApi(API_KEY)

def get_channels_test():
    # Получение каналов по названию
    # Может потребоваться для получения id канала
    # Id канала будет в item['id']['channelId']
    channels = yt.get_channels('квн', limit=3)
    # Получить каналы в которых будут указаны определенные поля
    #channels = yt.get_channels('квн', fields='nextPageToken,items(id,snippet(title,channelId,channelTitle,description,publishedAt))', limit=3)
    #channels = yt.get_channels('квн', fields='id,snippet(title,channelId,channelTitle,description,publishedAt)', limit=3)
    #channels = yt.get_channels('квн', fields='id', limit=3)
    #print('Найденные каналы:')
    #save_json('channels.json', channels)
    pprint(channels)
    

#get_channels_test()

def get_playlists():
    # Получение плейлистов с канала:
    #playlists = yt.get_playlists('UC4iAuuvx9hJilx4QOcd8V6A1')
    playlists = yt.get_playlists('UC8lCS8Ubv3t0-Tf4IYLioTA')
    pprint(playlists)
    #save_json('playlists.json',playlists)

#get_playlists()


#videos = yt.get_videos_info(['7lqVYoKiMfw','7LeO_r8_L3k'])
#videos = yt.get_videos_info('7lqVYoKiMfw,7LeO_r8_L3k,_-pPLzyplS0,4ZMv35U9oYw,MHebByfQ_nc,lBcAmL8jX-Y,psDAuK8TduQ', fields='id,snippet(title,publishedAt),contentDetails,statistics')
#videos = yt.get_videos_info('7lqVYoKiMfw,7LeO_r8_L3k,_-pPLzyplS0,4ZMv35U9oYw,MHebByfQ_nc,lBcAmL8jX-Y,psDAuK8TduQ', fields='id,snippet(title,publishedAt)')
#videos = yt.get_videos_info(['7lqVYoKiMfw','7LeO_r8_L3k','_-pPLzyplS0','4ZMv35U9oYw','MHebByfQ_nc','lBcAmL8jX-Y','psDAuK8TduQ'], part='id', fields='id')
#videos = yt.get_videos_info(['7lqVYoKiMfw','7LeO_r8_L3k','_-pPLzyplS0','4ZMv35U9oYw','MHebByfQ_nc','lBcAmL8jX-Y','psDAuK8TduQ'], part='id', fields='id', limit=5)
#pprint(videos)

def get_comments_test():
    #comments = yt.get_comments('7lqVYoKiMfw')
    #save_json('comments.json', comments)
    #pprint(comments)
    #comments = yt.get_comments('7lqVYoKiMfw', fields='nextPageToken,items(id,snippet(videoId,topLevelComment(id,snippet(authorDisplayName,textDisplay,textOriginal,publishedAt,updatedAt,viewerRating))))')
    #comments = yt.get_comments(id='Uggb3EPddGJet3gCoAEC')
    #comments = yt.get_comments(parentId='Uggb3EPddGJet3gCoAEC')
    #comments = yt.get_comments('268a2Gyq-fc')
    #comments = yt.get_comments(id='UgyteV0exQnVVEnh7dh4AaABAg')
    #comments = yt.get_comments(id='UgyteV0exQnVVEnh7dh4AaABAg', textFormat='plainText')
    comments = yt.get_comments(parentId='UgyteV0exQnVVEnh7dh4AaABAg')
    #comments = yt.get_comments(parentId='UgwdSoJQp6IIJIaarER4AaABAg')
    #save_json('commentId.json', comments)
    #pprint(yt.result_raw)
    pprint(comments)
    

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

if __name__ == '__main__':
    # _get_delta_list_test()
    #get_comments_test()    

    _result_parse_test()    