# -*- encoding: utf-8 -*-
# @Author: https://github.com/TikHubIO
# @Time: 2023/04/20
# @Update: 2023/04/20
# @Version: 1.0
# @Function:
# 将接口数据从JSON转成CSV形式，并且可以进行数据选取
# @Change: 目前只有两个接口的数据可以进行选取
# @To-Do: 1. 优化数据选取的方式
#         2. 用户可输入存取需要数据列的文档名称，进行数据选取


import os
import pandas as pd
import sys
from json_to_csv import process_folder_to_csv
import shutil


# 用于将CSV文件中的数据进行筛选
def process_csv_files(input_folder, data_category, selected_data_folder="Output_Selected_Data"):
    cvs_folder = process_folder_to_csv(input_folder)  # json转csv
    if not os.path.exists(selected_data_folder):
        os.makedirs(selected_data_folder)  # 创建处理后数据文件夹

    for filename in os.listdir(cvs_folder):
        if filename.endswith(".csv"):
            filepath = os.path.join(cvs_folder, filename)
            df = pd.read_csv(filepath)  # 使用panda dataFrame进行选取数据
            if data_category == "/TikTok/video_comments/":
                columns = [
                    "video_id",
                    "has_more",
                    "cursor",
                    "count",
                    "comments_list_create_time",
                    "comments_list_user_region",
                    "comments_list_user_signature",
                    "comments_list_user_unique_id",
                    "comments_list_user_language",
                    "comments_list_user_nickname",
                    "comments_list_comment_language",
                    "comments_list_text",
                    "comments_list_digg_count",
                    "comments_list_is_author_digged",
                    "comments_list_author_pin",
                    "comments_list_share_info_desc",
                    "comments_list_share_info_title",
                    "comments_list_reply_comment_total",
                ]
            elif data_category == "/TikTok/search_data_videos/":
                columns = [
                    "has_more",
                    "cursor",
                    "count",
                    "data_list_desc",
                    "data_list_added_sound_music_info_title",
                    "data_list_added_sound_music_info_user_count",
                    "data_list_added_sound_music_info_author",
                    "data_list_added_sound_music_info_duration_high_precision_video_duration_precision",
                    "data_list_added_sound_music_info_video_duration",
                    "data_list_author_follower_count",
                    "data_list_author_unique_id",
                    "data_list_author_following_count",
                    "data_list_author_uid",
                    "data_list_author_search_user_desc",
                    "data_list_author_search_user_name",
                    "data_list_video_play_addr_url_list_2",
                    "data_list_video_download_addr_url_list_2",
                    "data_list_music_selected_from",
                    "data_list_cha_list_0_cha_name",
                    "data_list_cha_list_0_share_info_share_url",
                    "data_list_cha_list_0_share_info_share_desc_info",
                    "data_list_share_info_share_url",
                    "data_list_statistics_play_count",
                    "data_list_statistics_share_count",
                    "data_list_statistics_forward_count",
                    "data_list_statistics_whatsapp_share_count",
                    "data_list_statistics_collect_count",
                    "data_list_statistics_comment_count",
                    "data_list_statistics_digg_count",
                    "data_list_statistics_download_count",
                    "data_list_region",
                    "data_list_search_desc",
                    "data_list_text_extra_0_hashtag_name",
                    "data_list_text_extra_1_hashtag_name",
                    "data_list_text_extra_2_hashtag_name",
                    "data_list_text_extra_3_hashtag_name",
                    "data_list_text_extra_4_hashtag_name",
                    "data_list_text_extra_5_hashtag_name",
                    "data_list_text_extra_6_hashtag_name",
                    "data_list_text_extra_7_hashtag_name",
                    "data_list_text_extra_8_hashtag_name",
                    "data_list_text_extra_9_hashtag_name",
                    "data_list_text_extra_10_hashtag_name",
                    "data_list_desc_language",
                ]

            try:
                file_name = filename.strip().split(os.path.sep)
                print("Selecting Data from " + file_name[-1] + " Right Now...")
                selected_data = df[columns].dropna(how='all')  # 选取需要数据，去除空值
                output_filepath = os.path.join(selected_data_folder, "Selected_Data_" + file_name[-1])
                selected_data.to_csv(output_filepath, index=False)  # 保存数据
                output_path_parts = output_filepath.strip().split(os.path.sep)
                print("Just completed selecting data, Saved in  " + output_path_parts[-1])
            except KeyError:
                print("Invalid key, May be wrong data category, try a different one")
            except Exception as e:
                raise e
    try:
        shutil.rmtree(cvs_folder)  # 删除中间文件
    except OSError as e:
        raise e



