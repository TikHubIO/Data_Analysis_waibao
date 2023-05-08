import os
import json
import pandas as pd
import requests
import asyncio
from googletrans import Translator
import time

# 从CSV导出视频url，并且调用tikhub的api获取视频信息（Export video url from CSV and get video information from tikhub api）
# 选取comment并保存于CSV文件中（Select comment and save in CSV file）
async def get_comment_info() -> None:
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTUwNDIzOTAsInVzZXJuYW1lIjoibGVxaXVAdWNzYy5lZHUiLCJlbWFpbCI6ImxlcWl1QHVjc2MuZWR1IiwiZXZpbDEiOiIkMmIkMTIkS0RIOHlsSjk4ZGVSSWM1ZmguVzFULmJXMWJMZVdhR0lOLi5uVlpxNlcuTzhzcEEzQTFjMTYifQ.CFDKuop1wfDLcyOnhySOQPDEhPN8HDbpnXw6a1CVcY0'
    }
    df = pd.read_csv('video_list.csv')
    video_url_list = df['Video_URL'].tolist()

    # 可以改动最后一个数字，以测试更多视频（Can change the last number to test more videos）
    # 比如：【0：10】获取前10个视频评论（For example: [0:10] test the first 10 videos）
    # 比如：【0：20】获取前20个视频评论（For example: [0:] test the first 20 videos）
    video_url_list = video_url_list[0:1]

    print("Getting Comment Data From API.get_tiktok_video_comments()...")

    # Create a new folder called "comments_raw_data"
    os.makedirs('comments_raw_data', exist_ok=True)

    for video_url in video_url_list:
        video_id = video_url.split('/')[-1]  # Get the video id from the URL
        csv_filename = f"comments_raw_data/comments_{video_id}.csv"
        df_comments = pd.DataFrame(columns=['comment'])

        has_more=True
        cursor=0
        while has_more:
            try:
                url= "https://api.tikhub.io/douyin/video_comments/?douyin_video_url=" + video_url+"&cursor="+str(cursor)+"&count=20&region=US&language=en"
                response = requests.request("GET", url, headers=headers, data=payload)
                cursor=cursor+1;
                if response != None:
                    print("response is not none")
                    print(url)
            except:
                print("All comments from this video have been fetched.")
                break;

            translator = Translator()
            # Extract the "text" data from the response
            response_data = json.loads(response.text)
            if(response_data['has_more']==False):
                print("no more comments!")
                break;
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
            try:
                translated_texts = [translator.translate(text, src='zh-CN', dest='en').text for text in
                                    filtered_comment_texts]
            except:
                print('Translation Error')
                continue
            # Save the comments in a CSV file

            for translated_text in translated_texts:
                next_index = len(df_comments)
                df_comments.loc[next_index, 'comment'] = translated_text
                # Save the comments in a CSV file
        df_comments.to_csv(csv_filename, index=False)
        print(f'Get {len(df_comments)} comments from video {video_url}, saved data in {csv_filename}')

        await asyncio.sleep(0.2)  # Sleep for 0.2 second


def convert_w_to_number(input_string):
    input_string = input_string.replace("W", "w")
    if "w" not in input_string:
        return str(input_string)

    number_parts = input_string.split("w")
    if "." in number_parts[0]:
        base_number = float(number_parts[0])
    else:
        base_number = int(number_parts[0])

    result = int(base_number * 10000)
    return str(result)

async def get_product_info() -> None:
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InplbnRoaWFhQGdtYWlsLmNvbSIsImV4cCI6MTcxMzQyMTcyMiwiZW1haWwiOiJ6ZW50aGlhYUBnbWFpbC5jb20iLCJldmlsMSI6IiQyYiQxMiRiU1BNZ2RhbUFmZ09FTVY3VlMxSlAua2dnZVkweWl5N3prQUM1cjd5Zzl6akkuL1dIVHhSYSJ9.E32gugbADhSAlLNR0MkwIkr_sbfnArXA5i2Sov_4RCY'
    }
    df = pd.read_csv('product_list.csv')
    Product_List = df['Product_Name'].tolist()
    print("Getting product Data price From API.get_douyin_search_data_products()...")

    product_prices = []
    for product in Product_List:
        product_converted = product.replace(" ", "%20")
        url = "https://api.tikhub.io/douyin/search_data_products/?keyword=" + product_converted + "&cursor=0&count=20&region=US&language=en"
        response = requests.request("GET", url, headers=headers, data=payload)

        # Extract the "text" data from the response
        response_data = json.loads(response.text)

        def _search_recursive(response_data):
            if isinstance(response_data, dict):
                if "extra_info" in response_data :
                    if response_data["extra_info"]!= "{}":
                        product_prices.append(convert_w_to_number(response_data["extra_info"][2:]))
                for value in response_data.values():
                    _search_recursive(value)
            elif isinstance(response_data, list):
                for item in response_data:
                    _search_recursive(item)
        _search_recursive(response_data)
        await asyncio.sleep(0.2)  # Sleep for 0.2 second


    product_prices_df = pd.DataFrame(product_prices, columns=['Product_Sold_Count($) '])
    sorted_product_prices_df = product_prices_df.sort_values(by=['Product_Sold_Count($) '], ascending=False)
    sorted_product_prices_df.to_csv('product_sold.csv', index=False)
    print("Successfully saved product sold count to product_prices.csv")


async def main() -> None:
    await get_comment_info()

start_time = time.time()
asyncio.run(main())
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
