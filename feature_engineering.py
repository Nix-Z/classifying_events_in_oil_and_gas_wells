import pandas as pd
from sklearn.preprocessing import StandardScaler
from data_preprocess import preprocess_data

def engineer_features():
    data = preprocess_data()

    # Scale Features
    X = data.drop(columns=['class'])
    y = data['class']
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(X)
    scaled_data = pd.DataFrame(scaled_features, columns=X.columns)
    y.reset_index(drop=True, inplace=True)  # Reset index of the target variable
    scaled_data['class'] = y

    data.to_csv('gas_well_events_cleansed_data.csv', index=False)

    return scaled_data

engineer_features()
