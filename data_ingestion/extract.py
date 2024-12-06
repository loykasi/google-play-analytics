import datetime
import json
import time
import feedparser
import pandas as pd
import urllib.parse
import requests
from unidecode import unidecode
from google_play_scraper import app as appCrawler
from functools import wraps

update_rss_url = "https://apkcombo.com/latest-updates/feed"
crawl_data = []

def rate_limited(max_per_sec):
    min_interval = 1.0 / float(max_per_sec)
    def decorate(func):
        last_time_called = [0.0]
        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            elapsed = time.time() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_time_called[0] = time.time()
            return func(*args, **kwargs)
        return rate_limited_function
    return decorate

@rate_limited(10)
def crawl(id):
    print(f'crawling {id}')
    try:
        result = appCrawler(
            id,
            lang="vi",
            country="vn"
        )
        crawl_data.append(result)
    except:
        print("failed")

def crawl_new_updates():
    print(datetime.datetime.now(), "| start crawl task")
    update_rss = feedparser.parse(update_rss_url)
    update_apps = update_rss.entries
    start_time = time.time()
    for app in update_apps:
        crawl(app.id)
    end_time = time.time()
    print(f'Crawling took {end_time - start_time} seconds')
    with open('crawled_data.json', 'w', encoding='utf-8') as file:
        json.dump(crawl_data, file, indent=2, ensure_ascii=False)

def transform_data():
    df = pd.read_json('./crawled_data.json')

    developers = df[["developerId", "developer"]].drop_duplicates(subset=["developerId"])
    developers = developers.rename(columns={"developerId": "id"})
    developers["id"] = developers["id"].apply(lambda x: urllib.parse.unquote(x))

    categories_flat = pd.json_normalize(df["categories"].explode())
    categories_flat['id'] = categories_flat['id'].fillna(categories_flat['name'].apply(lambda x: unidecode(x).upper().replace(' ', '_')))
    categories = categories_flat[['id', 'name']].drop_duplicates(subset=['id'])

    appCategory = pd.concat([
            df.explode("categories")["appId"].reset_index(drop=True),
            categories_flat["id"]
        ], axis=1)
    appCategory = appCategory.rename(columns={"appId": "app_id", "id": "category_id"})

    apps = df[["appId", "developerId", "released"]]
    apps = apps.rename(columns={"appId": "id", "developerId": "developer_id"})
    apps["developer_id"] = apps["developer_id"].apply(lambda x: urllib.parse.unquote(x))

    versions = df[["appId", "updated", "title", "version", "icon", "realInstalls", "score", "ratings", "reviews", "price", "currency"]]
    histogram = pd.DataFrame(df.histogram.tolist(), columns=['rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5'])
    versions = pd.concat([versions, histogram], axis=1)
    versions = versions.rename(columns={"appId": "app_id", "realInstalls": "installs"})
    versions = versions.fillna(0)

    return (developers, categories, appCategory, apps, versions)

def load_to_db(developers, categories, appCategory, apps, versions):
    requests.post("http://database_api:8000/developers", 
        json=developers.to_dict('records'),
        headers={"Content-Type": "application/json"},
    )

    requests.post("http://database_api:8000/categories", 
        json=categories.to_dict('records'),
        headers={"Content-Type": "application/json"},
    )

    requests.post("http://database_api:8000/apps", 
        json=apps.to_dict('records'),
        headers={"Content-Type": "application/json"},
    )

    requests.post("http://database_api:8000/app-category", 
        json=appCategory.to_dict('records'),
        headers={"Content-Type": "application/json"},
    )

    requests.post("http://database_api:8000/versions", 
        json=versions.to_dict('records'),
        headers={"Content-Type": "application/json"},
    )


crawl_new_updates()
if len(crawl_data) != 0:
    (developers, categories, appCategory, apps, versions) = transform_data()
    load_to_db(developers, categories, appCategory, apps, versions)