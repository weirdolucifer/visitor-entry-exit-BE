# fampay-video-service

### Basic Requirements:

- [x] Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.

- [x] A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.

- [x] A basic search API to search the stored videos using their title and description.

- [x] Dockerize the project.

- [x] It should be scalable and optimised.

### Bonus Points:

- [x] Add support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.

- [ ] Make a dashboard to view the stored videos with filters and sorting options (optional)

- [x] Optimise search api, so that it's able to search videos containing partial match for the search query in either video title or description.


## Architecture:

![img](./architecture.png)


## Setup:

### Using Docker:

```bash
  # Clone the repository
  $ cd fampay-video-service/
  # Update .env file (NUM_KEYS, GOOGLE_API_KEYS) with multiple keys.
  $ docker-compose up -d --build
  # The Applicaton server is runnning at localhost:8000 with supporting servers.
```

### Using VirtualEnv:


  ```bash
  # Clone the repository
  $ cd fampay-video-service/
  # Create a virtual env and install rquirements
  $ pip install -r requirements/requirements.txt 
  # Install Redis, Postgres on system and run them.
  # Update .env file (NUM_KEYS, GOOGLE_API_KEYS) with multiple keys and update postgres and redis server details as well.
  $ python manage.py migrate
  $ python manage.py runserver
  # Open two more termianl windows and run follwing commands
  $ celery --app fampay_video_service worker -Q fampay_task_queue --loglevel=info
  $ celery -A fampay_video_service beat -l info --loglevel=info
  ```
 
 ### Application Health/Readiness/liveliness API:
  ```bash
  curl --location --request GET 'http://127.0.0.1:8000/fampay-video-service/health/
  curl --location --request GET 'http://127.0.0.1:8000/fampay-video-service/ready/
  curl --location --request GET 'http://127.0.0.1:8000/fampay-video-service/live/
  ```
  
 ### Video Listing API:
 
  ```bash
  curl --location --request GET 'http://127.0.0.1:8000/fampay-video-service/youtube-panel/video/list/?page_size=<PAGE_SIZE>&page=<PAGE_NUMBER>&search=<ANY_TEXT>'
  # Query Params are optional.
  # Sample Response:
  
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 89,
            "video_url": "https://www.youtube.com/watch?v=4HJ6PXIiZRg",
            "video_id": "4HJ6PXIiZRg",
            "title": "Official LEGO The Incredibles Crimewaves Gameplay Trailer 2",
            "description": "BREAKING NEWS* Syndrome is on the loose! In order to stop him, the Parr family needs to work together and take back the city.",
            "published_datetime": "2022-08-27T20:03:44Z",
            "thumbnails": [
                "https://i.ytimg.com/vi/4HJ6PXIiZRg/default_live.jpg",
                "https://i.ytimg.com/vi/4HJ6PXIiZRg/mqdefault_live.jpg",
                "https://i.ytimg.com/vi/4HJ6PXIiZRg/hqdefault_live.jpg"
            ]
        }
    ]
}
  ```
