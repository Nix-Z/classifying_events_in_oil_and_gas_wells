import pandas as pd
import plotly.express as px
from data_extraction import load_and_process_merged_data

def visualize_data():
    data = load_and_process_merged_data()

    categorical_features = data.select_dtypes("object").columns
    print(f"\nCategorical Features: {categorical_features}")
    numerical_features = data.select_dtypes("number").columns
    print(f"\nNumerical Features: {numerical_features}")

    # Creates correlation plot for numerical featues
    corr_data_num = data[numerical_features].corr()
    print(corr_data_num)
    fig_1 = px.imshow(corr_data_num, labels=dict(color="Correlation"), text_auto=True, x=corr_data_num.columns,
                      y=corr_data_num.index, template='plotly_dark')
    fig_1.show()
    fig_1.write_image('fig_1.jpg')

    # Creates pie chart to show the distribution of events
    class_counts = data['class'].value_counts().reset_index()
    class_counts.columns = ['class', 'count']
    key_names = {0: 'Normal',
                1: 'Abrupt Increase of BSW',
                2: 'Spurious Closure of DHSV',
                3: 'Severe Slugging',
                4: 'Flow Instability',
                5: 'Rapid Productivity Loss',
                6: 'Quick Restriction in PCK',
                8: 'Hydrate in Production Line'
                }
    class_counts['class'] = class_counts['class'].map(key_names)
    fig_2 = px.pie(class_counts, names='class', values='count', title='Distribution of Events',
                   template='plotly_dark')
    fig_2.show()
    fig_2.write_image('fig_2.jpg')

    return data

visualize_data()
