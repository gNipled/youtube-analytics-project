import os
from googleapiclient.discovery import build
from src.exceptions import VideoIdError

API_KEY = os.getenv('YT_API_KEY')


class Video:
    """
    Class for YouTube videos
    """
    def __init__(self, video_id: str):
        self.__video_id = video_id
        try:
            self.id_check()
        except VideoIdError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            data = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=self.__video_id
                                                     ).execute()
            self.title = data["items"][0]["snippet"]["title"]
            self.url = f'https://www.youtube.com/watch?v={self.__video_id}'
            self.view_count = data["items"][0]["statistics"]["viewCount"]
            self.like_count = data["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return str(self.title)

    def id_check(self):
        data = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                 id=self.__video_id
                                                 ).execute()
        if len(data["items"]) <= 0:
            raise VideoIdError
        else:
            return True


    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)


class PLVideo(Video):
    """
    Class for YouTube video from Playlist
    """
    def __init__(self, video_id: str, plist_id: str):
        super().__init__(video_id)
        self.__plist_id = plist_id
