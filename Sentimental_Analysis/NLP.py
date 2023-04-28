import os
import pandas as pd
import ssl
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.downloader import download

# bypass SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

def classify_sentiment(text, sia):
    sentiment_score = sia.polarity_scores(text)

    if sentiment_score['compound'] > 0.05:
        return 'positive'
    elif sentiment_score['compound'] < -0.05:
        return 'negative'
    else:
        return 'neutral'


def sentiment_analysis(folder_path):
    download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    sentiment_counts = []
    #asyncio.run(get_comment_info())
    print("--------------------")
    print("Performing sentiment analysis...")

    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            comments = df['text'].tolist()

            sentiment_count = {'positive': 0, 'negative': 0, 'neutral': 0}

            for comment in comments:
                sentiment = classify_sentiment(comment, sia)
                sentiment_count[sentiment] += 1

            sentiment_counts.append(sentiment_count)

    print("Sentiment analysis completed.")
    return sentiment_counts


def save_to_csv(sentiment_counts):
    df = pd.DataFrame(sentiment_counts)

    # Calculate the total number of positive, negative, and neutral values
    total_positive = df['positive'].sum()
    total_negative = df['negative'].sum()
    total_neutral = df['neutral'].sum()

    # Add the total values as a new row at the bottom of the DataFrame using loc

    # Add a new column called "highest" to find the highest number in each row
    # and fill the cell with the column name of the highest number
    df['highest'] = df.idxmax(axis=1)
    custom_order = {'positive': 1, 'neutral': 0, 'negative': -1}
    df['highest_count(pos=1,neu=0,neg=-1)'] = df['highest'].map(custom_order)
    sorted_df = df.sort_values(by='highest_count(pos=1,neu=0,neg=-1)', ascending=False)

    # Save the updated DataFrame to a CSV file
    sorted_df.to_csv('sentiment_counts.csv', index=False)
    print("Sentiment counts saved to 'sentiment_counts.csv'.")

