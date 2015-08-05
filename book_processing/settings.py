import os
from django.conf import settings


LOCAL_BOOKS_PATH = getattr(
    settings, 'LOCAL_BOOKS_PATH', os.path.join(settings.MEDIA_ROOT, 'books'))


DOWNLOAD_CHUNK_SIZE = getattr(
    settings, 'DOWNLOAD_CHUNK_SIZE', 4194304) # 4 Mb
