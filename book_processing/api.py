import datetime
import hashlib
import os
import requests
import zipfile

from lxml import etree


from book_processing import settings as books_settings


def _local_path_from_url(url):
    """
    Returns local path to store book from the specified url
    """
    filename = '{}.epub'.format(hashlib.sha224(url).hexdigest())
    return os.path.join(books_settings.LOCAL_BOOKS_PATH, filename)


def _extract_book(local_path, order_hash):
    """
    Extracts book content from zipped file (epub)
    """
    unzipped_directory = '.'.join((local_path, order_hash, 'uncompressed'))

    if not os.path.exists(unzipped_directory):
        os.makedirs(unzipped_directory)

        with open(local_path, 'rb') as f:
            zip_file = zipfile.ZipFile(f)
            for name in zip_file.namelist():
                zip_file.extract(name, unzipped_directory)

    return unzipped_directory


def download_book(url):
    """
    Retrieves book from the provided url and returns local path to it
    """
    local_path = _local_path_from_url(url)

    if not os.path.exists(local_path):
        response = requests.get(url, stream=True)
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(
                    chunk_size=books_settings.DOWNLOAD_CHUNK_SIZE):
                f.write(chunk)

    return local_path


def watermark_file(local_path, order_hash):
    """
    Applies order_hash watermark to epub located at local_path
    """

    unzipped_directory = _extract_book(local_path, order_hash)
    container_xml = os.path.join(unzipped_directory, 'META-INF/container.xml')

    with open(container_xml, 'rb') as input:
        root = etree.fromstring(input.read())
        comment = etree.Element('comment')
        comment.set('timestamp', datetime.datetime.now().isoformat())
        comment.set('order_hash', order_hash)
        root.insert(0, comment)
        corrected_xml = etree.tostring(root)

    with open(container_xml, 'wb') as output:
        output.write(corrected_xml)

    watermarked_path = '.'.join((local_path, order_hash, 'epub'))
    with zipfile.ZipFile(watermarked_path, 'w') as watermarked_epub:
        for root, dirs, files in os.walk(unzipped_directory):
            for file_ in files:
                absolute_path = os.path.join(root, file_)
                watermarked_epub.write(
                    absolute_path,
                    absolute_path.replace(unzipped_directory, ''))
    return watermarked_path
