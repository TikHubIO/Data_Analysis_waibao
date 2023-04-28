import os
import json
import pandas as pd
import requests
import asyncio
from googletrans import Translator

# 从CSV导出视频url，并且调用tikhub的api获取视频信息（Export video url from CSV and get video information from tikhub api）
# 选取comment并保存于CSV文件中（Select comment and save in CSV file）
async def get_comment_info(data_category) -> None:
    payload = {}
    headers = {
        'Authorization': 'Bearer 填写自己的token'
    }
    df = pd.read_csv('video_list.csv')
    video_url_list = df['Video_URL'].tolist()

    # 可以改动最后一个数字，以测试更多视频（Can change the last number to test more videos）
    # 比如：【0：10】获取前10个视频评论（For example: [0:10] test the first 10 videos）
    # 比如：【0：20】获取前20个视频评论（For example: [0:] test the first 20 videos）
    video_url_list = video_url_list[0:50]

    print("Getting Comment Data From API.get_tiktok_video_comments()...")

    # Create a new folder called "comments_raw_data"
    os.makedirs('comments_raw_data', exist_ok=True)

    for video_url in video_url_list:
        url = "https://api.tikhub.io/douyin/video_comments/?douyin_video_url=" + video_url + "&cursor=0&count=20&region=US&language=en"
        response = requests.request("GET", url, headers=headers, data=payload)
        translator = Translator()

        # Extract the "text" data from the response
        response_data = json.loads(response.text)
        comments = response_data.get('comments_list', [])

        # Select the "text" data from the comments List, if the comments List is empty, continue
        try:
            comment_texts = [comment['text'] for comment in comments]
        except:
            print(f'No comments in video {video_url}')
            continue

        # 翻译评论（Translate comments）

        # Filter out NoneType values from comment_texts
        filtered_comment_texts = [text for text in comment_texts if text != '']

        # Translate the filtered texts
        translated_texts = [translator.translate(text, src='zh-CN', dest='en').text for text in filtered_comment_texts]


        df_comments = pd.DataFrame(translated_texts, columns=['text'])
        video_id = video_url.split('/')[-1]  # Get the video id from the URL
        csv_filename = f"comments_raw_data/comments_{video_id}.csv"

        # Save the comments in a CSV file
        df_comments.to_csv(csv_filename, index=False)
        print(f'Get {len(comments)} comments from video {video_url}, saved data in {csv_filename}')

        await asyncio.sleep(0.2)  # Sleep for 0.2 second

