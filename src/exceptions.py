class VideoIdError(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else 'Неверный ID видео'

    def __str__(self):
        return self.message
