from NLP import *
from data_crawling import *
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


def combined_csv(product_filename, sentiment_filename):
    print(f"combining csv files from {product_filename} and {sentiment_filename}...")
    product_df = pd.read_csv(product_filename)
    sorted_product_df = product_df.sort_values(by=['Product_Sold_Count($)'], ascending=False)
    sentiment_df = pd.read_csv(sentiment_filename)

    # Map the 'highest' column in sentiment_df to the desired numeric values

    # Reset index for both DataFrames to concatenate them properly
    sorted_product_df.reset_index(drop=True, inplace=True)
    sentiment_df.reset_index(drop=False, inplace=True)

    # Concatenate the DataFrames
    combined_df = pd.concat([sorted_product_df, sentiment_df], axis=1)

    # Remove rows with any empty cells
    cleaned_df = combined_df.dropna()
    del  cleaned_df['index']

    # Save the cleaned DataFrame to a CSV file
    cleaned_df.to_csv('combined.csv', index=False)

    print("Combined csv saved to 'combined.csv'.")




def statsmodels_linear_regression(data_file):
    # Load the CSV data
    df = pd.read_csv(data_file)

    # Add a constant to the DataFrame for the intercept term (β0)
    df = sm.add_constant(df)

    # Define the dependent variable (y) and the independent variables (X)
    y = df['Product_Sold_Count($)']
    X = df[['positive', 'negative', 'neutral']]

    # Create a linear regression model using statsmodels
    X = sm.add_constant(X)

    # Fit the multiple linear regression model
    model = sm.OLS(y, X).fit()

    # Get the results
    results_summary = model.summary()

    # print the model summary
    print(model.summary())

    # Analyze the estimated coefficients, p-values, and model fit
    coefficients = model.params
    p_values = model.pvalues
    rsquared = model.rsquared
    adj_rsquared = model.rsquared_adj

    # Save the results in a JSON file
    results = {
        'coefficients': coefficients.to_dict(),
        'p_values': p_values.to_dict(),
        'r_squared': rsquared,
        'adjusted_r_squared': adj_rsquared
    }

    with open('regression_results.json', 'w') as f:
        json.dump(results, f)

    print("Regression analysis results saved in 'regression_results.json'")

    # Scatterplot matrix, show linear regression line for each plot
    sns.pairplot(df[['Product_Sold_Count($)', 'positive', 'negative', 'neutral']])
    plt.save('scatterplot_matrix.png')
    plt.show()

    # Heatmap of the correlation matrix
    corr_matrix = df[['Product_Sold_Count($)', 'positive', 'negative', 'neutral']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
    plt.save('heatmap.png')
    plt.show()



def linear_regression_ML(data_file):
    data = pd.read_csv(data_file)

    # Prepare the dependent and independent variables
    X = data[['positive', 'negative', 'neutral']]
    y = data['Product_Sold_Count($)']

    # Perform multiple linear regression analysis
    print("Performing linear regression analysis using scikit-learn...")
    model = LinearRegression().fit(X, y)
    print("Model fit complete. Calculating model performance metrics...")
    # Create the folder if it does not exist
    folder_name = "ML_data_analysis_result"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Get the results
    coefficients = model.coef_
    intercept = model.intercept_
    r_squared = model.score(X, y)

    # Calculate adjusted R-squared
    n = len(y)  # number of samples
    p = X.shape[1]  # number of independent variables
    adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)

    # Save the results in a JSON file
    results = {
        'coefficients': list(coefficients),
        'intercept': intercept,
        'r_squared': r_squared,
        'adjusted_r_squared': adjusted_r_squared
    }

    json_file_path = os.path.join(folder_name, 'regression_results_ML.json')
    with open(json_file_path, 'w') as f:
        json.dump(results, f)

    print("Regression analysis results saved in 'regression_results_ML.json'")

    print("Stating Data Visualization...")


    # Data visualization
    sns.set(style="whitegrid")

    # Pairplot to visualize the relationships between variables
    plot_data=data[['Product_Sold_Count($)', 'highest_count(pos=1,neu=0,neg=-1)']]
    sns.pairplot(plot_data)
    pairplot_filename = os.path.join(folder_name, "pairplot_ML.png")
    plt.savefig(pairplot_filename)

    # Correlation heatmap
    correlation_matrix = plot_data.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    heatmap_filename = os.path.join(folder_name, "heatmap_ML.png")
    plt.savefig(heatmap_filename)

    # Bar plot for coefficients
    plt.figure(figsize=(8, 6))
    coef_df = pd.DataFrame(coefficients, index=X.columns, columns=['Coefficient'])
    coef_df.plot(kind='bar', legend=False)
    plt.ylabel("Coefficient")
    plt.title("Linear Regression Coefficients")
    barplot_filename = os.path.join(folder_name, "barplot_ML.png")
    plt.savefig(barplot_filename)

    plt.show()

    print("Data Visualization Complete.")


