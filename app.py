from flask import Flask, render_template_string, request, redirect, url_for
import tweetParse
import random

app = Flask(__name__)

@app.route('/')
def home():
    central_tweet, centel_tweet, central_url, centel_url = tweetParse.getTweets()
    if len(central_url) == 0:
        central_url = "Tweet Not Found"
    if len(centel_url) == 0:
        centel_url = "Tweet Not Found"
    tweets = [(central_tweet, 'NBACentral', central_url), (centel_tweet, 'NBACentel', centel_url)]
    selected_tweet = random.choice(tweets)
    tweet_content, tweet_source, tweet_url = selected_tweet
    template = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
         <title>NBACentral vs. NBACentel</title>
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
          <p>The tweet below is either from NBACentral (and is real), or from NBACentel (and is completely made up). Determine the source of the tweet below.</p>
          <div class="tweet-container">
            <div class="content">{{ tweet_content }}</div>
          </div>
          <form method="post" action="/result" class="text-center">
            <button type="submit" name="selected_source" value="NBACentral" class="btn btn-primary mt-3 px-4 py-2">NBACentral</button>
            <button type="submit" name="selected_source" value="NBACentel" class="btn btn-secondary mt-3 px-4 py-2">NBACentel</button>
            <input type="hidden" name="actual_source" value="{{ tweet_source }}">
            <input type="hidden" name="tweet_url" value="{{ tweet_url }}">
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
    return render_template_string(template, tweet_content=tweet_content, tweet_source=tweet_source, tweet_url=tweet_url)

@app.route('/result', methods=['POST'])
def result():
    selected_source = request.form.get('selected_source')
    actual_source = request.form.get('actual_source')
    tweet_url = request.form.get('tweet_url')

    if selected_source == actual_source:
        result_message = f"Correct! You guessed the tweet's source."
        copy_message = f"I correctly guessed that the source of this tweet! Can you do it too?"
    else:
        result_message = f"Oops, you got Centeled! The tweet was actually from {actual_source}."
        copy_message = "I got Centeled! Can you guess correctly?"

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
          <p>Tweet URL: <a href="{{ tweet_url }}" target="_blank">{{ tweet_url }}</a></p>
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
