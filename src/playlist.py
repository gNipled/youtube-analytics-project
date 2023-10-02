import os
from googleapiclient.discovery import build
import isodate
import datetime

API_KEY = os.getenv('YT_API_KEY')


class PlayList:
    def __init__(self, plist_id: str):
        self.__plist_id = plist_id
        data = PlayList.get_service().playlists().list(id=self.__plist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        self.title = data["items"][0]["snippet"]["title"]
        self.url = f'https://www.youtube.com/playlist?list={self.__plist_id}'
        self.total_duration = self.total_duration()

    def get_videos(self):
        return PlayList.get_service().playlistItems().list(playlistId=self.__plist_id,
                                                           part='contentDetails',
                                                           maxResults=50,
                                                           ).execute()

    def get_video_ids(self):
        return [video['contentDetails']['videoId'] for video in self.get_videos()['items']]

    def get_videos_info(self):
        return PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(self.get_video_ids())
                                                              ).execute()

    def total_duration(self):
        duration = datetime.timedelta(hours=0)
        video_response = self.get_videos_info()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += (isodate.parse_duration(iso_8601_duration))
        return duration

    def show_best_video(self):
        likes = 0
        best_video = ''
        video_response = self.get_videos_info()
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > likes:
                likes = int(video['statistics']['likeCount'])
                best_video = str(video['id'])
        return f'https://youtu.be/{best_video}'

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)
