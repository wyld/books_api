import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from sendfile import sendfile

from book_processing import api


class WatermarkBook(APIView):
    """
    Watermarks provided book
    """

    def validate_input(self):
        book_url = self.request.data.get('book_url')
        order_hash = self.request.data.get('order_hash')

        errors = {}

        if not book_url or not isinstance(book_url, basestring):
            errors.update({'book_url': u'should be non-empty string'})
        if not order_hash or not isinstance(order_hash, basestring) \
                or len(order_hash) > 32:
            errors.update(
                {'order_hash':
                     u'should be non-empty string up to 32 characters'})

        return {'book_url': book_url, 'order_hash': order_hash}, errors

    def post(self, request, format=None):
        data, errors = self.validate_input()
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        local_path = api.download_book(data.get('book_url'))
        watermarked_path = api.watermark_file(
            local_path, data.get('order_hash'))

        return sendfile(request, watermarked_path, attachment=True,
            attachment_filename=os.path.basename(data.get('book_url')),
            mimetype='application/epub+zip')
