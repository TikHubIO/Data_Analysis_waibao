import asyncio
from tikhub import TikTokAPI, DouyinAPI
import pandas as pd
import json


# 读取标签文件，根据标签搜索最多点赞视频
def fetch_tag(tag_filepath, order, douyin_api):
    # Create an empty DataFrame with the specified columns
    columns = ['标签', '用户ID', '头像下载url', '评论数量', '粉丝数量', '视频播放量']
    df = pd.DataFrame(columns=columns)

    # Read the tags file line by line
    with open(tag_filepath, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            print("正在采集 标签【"+ line+"】 的数据")
            # 参数可以自行修改；sort_type=1表示按照点赞数排序，publish_time="7"表示最近7天，content_type=0表示视频）
            r = asyncio.run(
                douyin_api.get_douyin_search_data_videos(keyword=line, count=30, sort_type='1', publish_time='7',
                                                         content_type='0'))
            for key in r["data_list"]:
                try:
                    df = df._append({'标签': line, '用户ID': key['aweme_info']['author']['uid'],
                                     '头像下载url': key['aweme_info']['author']['avatar_larger']['url_list'][0],
                                     '评论数量': key['aweme_info']['statistics']['comment_count'],
                                     '粉丝数量': key['aweme_info']['author']['follower_count'],
                                     '视频播放量': key['aweme_info']['statistics']['digg_count']}, ignore_index=True)
                    print("用户 [" + key['aweme_info']['author']['uid'] + "] 信息已保存")
                except:
                    print('Error：用户不存在或信息不完整')
                    continue
            print("标签 【" + line + "】 已完成采集")
            print("=====================================")
    if order == 1:  # Sort the DataFrame by 'tag' and 'comment_count' in descending order
        df = df.sort_values(by=['标签', '评论数量'], ascending=[True, False])
        df.to_csv('tag_comment_sorted.csv', index=False, encoding='utf-8-sig')  # Save the DataFrame to a CSV file
        print("评论数排序已完成")
    elif order == 2:  # Sort the DataFrame by 'tag' and 'follower_count' in descending order
        df = df.sort_values(by=['标签', '粉丝数量'], ascending=[True, False])
        df.to_csv('tag_follower_sorted.csv', index=False, encoding='utf-8-sig')  # Save the DataFrame to a CSV
        print("粉丝数排序已完成")
    elif order == 3:  # Sort the DataFrame by 'tag' and 'view_count' in descending order
        df = df.sort_values(by=['标签', '视频播放量'], ascending=[True, False])
        df.to_csv('tag_view_sorted.csv', index=False, encoding='utf-8-sig')  # Save the DataFrame to a CSV file
        print("播放量排序已完成")


if __name__ == '__main__':
    token = input('请输入TikHub账户秘钥: ')
    douyin_api = DouyinAPI(token)
    fetch_tag('tags.txt', 1, douyin_api)
