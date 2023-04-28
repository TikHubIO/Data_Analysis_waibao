from NLP import *
from Data_Analysis import *


if __name__ == "__main__":
    sentiment_counts = sentiment_analysis(os.path.join(os.getcwd(), "comments_raw_data"))
    save_to_csv(sentiment_counts)
    combined_csv('NLP_result/product_sold.csv', 'NLP_result/sentiment_counts.csv')
    # visualize_csv_data('combined.csv')
    #statsmodels_linear_regression('combined.csv')
    linear_regression_ML('combined.csv')
