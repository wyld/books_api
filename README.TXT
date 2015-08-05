
1. Install requirements from requirements.txt.

2. Start the server:

./manage.py runserver

3. Send test request (this is just an example, as the application serves the file directly from this url,
you should better use your browser to navigate http://localhost:8000/api/v1/books/watermark/ and send json from there using django rest framework helper form):

$ curl -H "Content-Type: application/json"
-X POST -d '{"book_url": "https://s3.eu-central-1.amazonaws.com/saxo-static/ebooks/line-vindernovelle-i-krimidysten.epub", "order_hash": "test"}'
http://localhost:8000/api/v1/books/watermark/



The following things were not done in 2-hours timeframe:

1. Proper tests with good coverage.
2. Filesystem cleanup process (depending on amount of similar requests which
reuse local data we should either delete used files outright or keep them for
some time as local cache and delete after specified timeframe via celery task with eta/countdown param).
3. I was not able to find correct schema for comment in META-INF/container.xml, so current one is just an example that needs correction
(also it keeps adding comments each time file is accessed, so this needs to be addressed too).
4. Error handling for all possible url retrieval and local filesystem exceptions.
5. Nginx config to test production-ready sendfile backend instead of simple one used when application is started via runserver.
