import tweepy
import csv

client = tweepy.Client(bearer_token="")

username = 'TheNBACentel'
user = client.get_user(username=username)
user_id = user.data.id
print(user_id)

tweets = client.get_users_tweets(id=user_id, max_results=100)
for tweet in tweets.data:
    print(tweet.text)

# Define the CSV filename
csv_filename = 'nba_centel_tweets.csv'

# Open a CSV file for writing
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet ID', 'Created At', 'Text'])  # Write header

    # Loop through tweets and write to CSV
    for tweet in tweets.data:
        writer.writerow([tweet.id, tweet.created_at, tweet.text])
        
print(f'Tweets saved to {csv_filename}')