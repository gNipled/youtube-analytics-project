import os
import json
from googleapiclient.discovery import build

API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        data = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = data['items'][0]['snippet']['title']
        self.description = data['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.sub_count = data['items'][0]['statistics']['subscriberCount']
        self.video_count = data['items'][0]['statistics']['videoCount']
        self.view_count = data['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.sub_count) + int(other.sub_count)

    def __sub__(self, other):
        return int(self.sub_count) - int(other.sub_count)

    def __lt__(self, other):
        return int(self.sub_count) < int(other.sub_count)

    def __le__(self, other):
        return int(self.sub_count) <= int(other.sub_count)

    def __gt__(self, other):
        return int(self.sub_count) > int(other.sub_count)

    def __ge__(self, other):
        return int(self.sub_count) >= int(other.sub_count)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        print(json.dumps(youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute(),
                         indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)

    def to_json(self, file_name: str):
        with open(file_name, 'w', encoding='utf-8') as file:
            data = {'id': self.__channel_id,
                    'title': self.title,
                    'description': self.description,
                    'url': self.url,
                    'subscriberCount': self.sub_count,
                    'videoCount': self.video_count,
                    'viewCount': self.view_count
                    }
            json.dump(data, file, indent=2, ensure_ascii=False)
