import os
from googleapiclient.discovery import build

API_KEY = os.getenv('YT_API_KEY')


class Video:
    """
    Class for YouTube videos
    """
    def __init__(self, video_id: str):
        self.video_id = video_id
        data = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.video_id
                                       ).execute()
        self.name = data["items"][0]["snippet"]["title"]
        self.url = f'https://www.youtube.com/watch?v={video_id}'
        self.view_count = data["items"][0]["statistics"]["viewCount"]
        self.like_count = data["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return str(self.name)

    @classmethod
    def get_service(self):
        return build('youtube', 'v3', developerKey=API_KEY)


class PLVideo(Video):
    """
    Class for YouTube video from Playlist
    """
    def __init__(self, video_id: str, plist_id: str):
        super().__init__(video_id)
        self.plist_id = plist_id
