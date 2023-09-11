import os
import json
from googleapiclient.discovery import build


API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        print(json.dumps(youtube.channels().list(id=self.channel_id, part ='snippet,statistics').execute(), indent=2, ensure_ascii=False))
