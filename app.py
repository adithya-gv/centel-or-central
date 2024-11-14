from flask import Flask, render_template_string, request
import tweetParse
import random

app = Flask(__name__)

@app.route('/')
def home():
    central_tweet, centel_tweet, central_url, centel_url = tweetParse.getTweets()
    tweets = [(central_tweet, 'central', central_url), (centel_tweet, 'centel', centel_url)]
    random.shuffle(tweets)
    template = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <title>Central vs. Centel</title>
        <style>
            .tweet-container {
                border: 1px solid #e1e8ed;
                border-radius: 10px;
                padding: 20px;
                margin: 20px;
                background-color: #f5f8fa;
            }
            .username {
                font-weight: bold;
            }
            .timestamp {
                color: #657786;
                font-size: 0.9em;
            }
        </style>
      </head>
      <body>
        <div class="container mt-5">
          <h1 class="mb-4">NBACentral vs. NBACentel</h1>
          <p>One of the tweets below is a news story from NBACentral, and is real. The other is from NBACentel, and is completely made up. Determine which news story is real.</p>
          <form method="post" action="/result">
            {% for tweet in tweets %}
            <div class="tweet-container">
              <div class="content">{{ tweet[0] }}</div>
              <button type="submit" name="selected_tweet" value="{{ tweet[1] }}" class="btn btn-primary mt-3">Select This Tweet</button>
            </div>
            {% endfor %}
          </form>
        </div>
        <footer class="text-left mt-5" style="margin-left: auto; margin-right: auto; width: 80%;">
            <h2>Instructions and credits</h2>
            <p>The twitter account <a href="https://twitter.com/TheDunkCentral" target="_blank">NBACentral</a> is a well-known news source breaking the latest NBA news.</p>
            <p>On the other hand the account <a href="https://twitter.com/TheNBACentel" target="_blank">NBACentel</a> is a well-known parody of this account publishing fake stories that have made their way onto major publications.</p>
            <p>The two accounts are known for catching NBA fans off guard, with the lines between reality and parody blurring, with NBA Superstar Kevin Durant even joining in on the fun.</p>
            <p>Thus, I thought it would be a fun idea to make a game to have people guess which tweet is real, considering it fools everyone online already.</p>
        </footer>
      </body>
    </html>
    """
    return render_template_string(template, tweets=tweets)

@app.route('/result', methods=['POST'])
def result():
    central_tweet, centel_tweet, central_url, centel_url = tweetParse.getTweets()
    if len(central_url) == 0:
        central_url = "Tweet Not Found"
    if len(centel_url) == 0:
        centel_url = "Tweet Not Found"
    tweets = {'central': (central_tweet, central_url), 'centel': (centel_tweet, centel_url)}
    selected_tweet = request.form.get('selected_tweet')
    _, tweet_url = tweets[selected_tweet]

    if selected_tweet == 'central':
        result_message = "Correct! You selected the real tweet from NBACentral."
        copy_message = "I was able to guess the real tweet from NBACentral! Can you?"
    else:
        result_message = "Oops, you got Centeled! You selected the fake tweet from NBACentel."
        copy_message = "I got Centeled! Can you guess the real tweet from between the two?"

    template = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <title>Result</title>
      </head>
      <body>
        <div class="container mt-5">
          <h1 class="mb-4">Result</h1>
          <p>{{ result_message }}</p>
          {% if tweet_url != "Tweet Not Found" %}
          <p>Tweet URL: <a href="{{ tweet_url }}" target="_blank">{{ tweet_url }}</a></p>
          {% else %}
          <p>Tweet URL: {{ tweet_url }}</p>
          {% endif %}
          <a href="{{ url_for('home') }}" class="btn btn-primary mt-3">Try Again</a>
          <button onclick="copyResults()" class="btn btn-secondary mt-3">Share Your Results</button>
          <script>
            function copyResults() {
              const text = '{{ copy_message }} Check it out at: https://centel-or-central.onrender.com/';
              navigator.clipboard.writeText(text).then(function() {
                alert('Results copied to clipboard!');
              }, function(err) {
                alert('Failed to copy results: ', err);
              });
            }
          </script>
        </div>
      </body>
    </html>
    """
    return render_template_string(template, result_message=result_message, copy_message=copy_message, tweet_url=tweet_url)


if __name__ == '__main__':
    app.run(debug=True)
