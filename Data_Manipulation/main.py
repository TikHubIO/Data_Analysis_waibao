import sys
from dataSelector import *

if __name__ == "__main__":
    # 输入指令 python dataSelector.py JSON文件夹名 数据接口名  即可
    # 需注意： 不同数据接口生成出来的数据需要分装在不同的JSON文件夹，
    # 假如/TikTok/search_data_videos/生成出来的JSON 和 /TikTok/video_comments/ 生成出来的JSON在同一个文件夹会有报错
    # test_json_files只是用来测试，可以删掉，或者在里面替换您的所有JSON文件

    # 数据接口名：
    # /TikTok/video_comments/
    # /TikTok/search_data_videos/

    # 例子   python main.py test_json_files /TikTok/video_comments/
    if len(sys.argv) != 3:
        print("\nUsage: python main.py <JSON文件夹名> <数据接口名>\n")
    else:
        input_folder = sys.argv[1]
        data_category = sys.argv[2]
        process_csv_files(input_folder, data_category)