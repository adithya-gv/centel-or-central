import csv
import random
import re

# Define the CSV filename
central_file = 'nba_central_tweets.csv'
centel_file = 'nba_centel_tweets.csv'


# Open a CSV file for reading
def readCentral():
    with open(central_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        # Randomly select a tweet from the file
        random_tweet = random.choice(list(reader))
        text = random_tweet[2]
        pattern = r'http[s]?://t\.co/\w+'
        urls = re.findall(pattern, text)
        url = ""
        if (len(urls) > 0):
            url = urls[0]
        pure_text = re.sub(pattern, '', text).strip()
        return pure_text, url

def readCentel():
    with open(centel_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        # Randomly select a tweet from the file
        random_tweet = random.choice(list(reader))
        text = random_tweet[2]
        pattern = r'http[s]?://t\.co/\w+'
        urls = re.findall(pattern, text)
        url = ""
        if (len(urls) > 0):
            url = urls[0]
        pure_text = re.sub(pattern, '', text).strip()
        return pure_text, url

def getTweets():
    central_text, central_urls = readCentral()
    centel_text, centel_urls = readCentel()
    return central_text, centel_text, central_urls, centel_urls
