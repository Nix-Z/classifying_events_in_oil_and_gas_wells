import pandas as pd
import os
from tsfresh import extract_features
from tsfresh.feature_extraction import feature_calculators
from datavisualization import visualize_data

def extracting_features():

    data = visualize_data()

    # Divide data into time windows
    step = 300  # Size of each window, 5m

    window_features = pd.DataFrame()

    feature_dict = {
        'mean': None,
        'variance': None,
        'skewness': None,
        'kurtosis': None,
        'abs_energy': None,
        'maximum': None,
        'minimum': None,
        'median': None,
        'quantile': [{"q": 0.25}, {"q": 0.75}],
        'variation_coefficient': None,
        'mean_change': None,
        'mean_second_derivative_central': None,
    }

    # Organize the dataframe into combinations of instances (files) and classes to extract samples
    instance_and_class_groups = data.groupby(["instance", "class"])
    print("Starting feature extraction:")

    combinations = 0
    for group_labels, group_data in instance_and_class_groups:
        class_code = group_labels[1]

        # Drop "instance" column since it's not a useful feature
        group_data = group_data.drop("instance", axis=1)

        f_idx = 0
        l_idx = group_data.shape[0]
        if (l_idx - f_idx) < step:
            continue
        for i in range(0, l_idx, step):
            raw_samples = group_data.iloc[i:i+step]
            extracted_features = extract_features(raw_samples,
                                                  column_id="class",
                                                  column_sort="timestamp",
                                                  default_fc_parameters=feature_dict,
                                                  n_jobs=0,
                                                  disable_progressbar=True)
            extracted_features["class"] = class_code
            window_features = pd.concat([window_features, extracted_features], ignore_index=True)

        combinations += 1
        if (combinations % 100) == 0:
            print(f"  Extracted features for {combinations} instance-and-class combinations...")

    print("Finished feature extraction!")

    return window_features

# extracting_features()

