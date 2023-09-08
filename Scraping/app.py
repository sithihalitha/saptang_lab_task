import os
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

gist_url = "https://gist.github.com/shrayasr/b317293e9ab5de3718bf"
response = requests.get(gist_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Scrape Author and Author Details
        author = soup.find("span", class_="author")
        print(author)
        if author:
            author_name = author.text.strip()
            author_link = author.find("a")["href"]
            author_url = "https://gist.github.com" + author_link
            author_response = requests.get(author_url)
            print(author_response)
            description = soup.find("div", class_="d-flex flex-column")
            print(description)
            if description:
                gist_description = description.text.strip()
            else:
                gist_description = "Description not found"
            print(author_name)
            print(author_link)

        gist_link= gist_url
        create_date = soup.find("div", class_="relative-time")
        if create_date:
            created_date = create_date.text.strip()
        else:
            created_date = "Created date not found"

        last_pushed_date= soup.find("div", class_="note m-0")
        if last_pushed_date:
            pushed_date = last_pushed_date.text.strip()
        else:
            pushed_date = "Last pushed date not found"

        
        download_link_item = soup.find("div", class_="ml-2")
        if download_link_item:
            download_link = download_link_item["href"]
        else:
            download_link = "Download link not found"

        # Store data in MongoDB
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["*******"]
        collection = db["*******"]

        gist_data = {
            "author": author_name,
            "author_link": author_link,
            "gist_description": gist_description,
            "gist_link": gist_url,
            "created_date": created_date,
            "last_pushed_date": pushed_date,
            "download_link": download_link,
        }

        collection.insert_one(gist_data)

    except Exception as e:
        print("Error:", str(e))

else:
    print("Failed to fetch the page. Status code:", response.status_code)
