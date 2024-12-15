import os
import time
import tweepy
from anthropic import Anthropic

# Twitter API Credentials (ALL REQUIRED)
TWITTER_API_KEY = ''  # Consumer Key
TWITTER_API_KEY_SECRET = ''  # Consumer Secret
TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''
TWITTER_BEARER_TOKEN = ''

# Anthropic API Credentials
ANTHROPIC_API_KEY = ''


class RandomTweetBot:
    def __init__(self):
        # Twitter Authentication
        self.auth = tweepy.OAuthHandler(
            TWITTER_API_KEY,
            TWITTER_API_KEY_SECRET
        )
        self.auth.set_access_token(
            TWITTER_ACCESS_TOKEN,
            TWITTER_ACCESS_TOKEN_SECRET
        )

        # Initialize Twitter API clients (REST and v2)
        self.twitter_rest_api = tweepy.API(self.auth)
        self.twitter_client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_KEY_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
            bearer_token=TWITTER_BEARER_TOKEN
        )

        # Initialize Anthropic client
        self.anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

    def generate_random_tweet(self):
        """Generate a random tweet using Claude"""
        try:
            # Generate tweet using Claude
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=280,  # Twitter character limit
                messages=[
                    {
                        "role": "user",
                        "content": "Generate an interesting, unique tweet that is insightful, witty, or thought-provoking. Ensure it's original and fits within Twitter's 280-character limit."
                    }
                ]
            )

            # Extract and return the generated tweet
            return response.content[0].text

        except Exception as e:
            print(f"Error generating tweet: {e}")
            # Fallback tweet if generation fails
            return "Exploring ideas, one tweet at a time. #RandomThoughts"

    def post_tweet(self):
        """Post a randomly generated tweet"""
        try:
            # Generate tweet
            tweet_text = self.generate_random_tweet()

            # Post tweet
            response = self.twitter_client.create_tweet(text=tweet_text)
            print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")

        except Exception as e:
            print(f"Error posting tweet: {e}")

    def start_bot(self):
        """Start the bot to tweet randomly every minute"""
        print("Random Tweet Bot Started!")
        while True:
            # Post a tweet
            self.post_tweet()

            # Wait for 1 minute before next tweet
            time.sleep(60)


# Initialize and run the bot
if __name__ == "__main__":
    bot = RandomTweetBot()
    bot.start_bot()
