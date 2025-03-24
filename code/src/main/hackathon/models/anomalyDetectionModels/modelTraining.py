import pickle
from hackathon.common.utils.utils import convert_datetime_features, frequency_ranking_encode
from hackathon.factory.Abstract_class import AbstractProduct
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt

from hackathon.models.anomalyDetectionModels.modelEvaluation import calculate_silhouette_scores

class ModelTraining(AbstractProduct):
    def __init__(self, config):
        self.config = config
        self.train_data_path = config.get('data', 'train_data_path')
        self.test_data_path = config.get('data', 'test_data_path')
        self.final_data_path = config.get('data', 'final_data_path')
        self.missingvalue_features_90 = config.get('data', 'missingvalue_features_90')
        self.low_variance_numerical_features = config.get('data', 'low_variance_numerical_features')
        self.high_correlation_features = config.get('data', 'high_correlation_features')
        self.single_value_features = config.get('data', 'single_value_features')
        self.all_dropped_features = config.get('data', 'all_dropped_features')
        self.final_features = config.get('data', 'final_features')
        self.numerical_features_mean_median = config.get('data', 'numerical_features_mean_median')
        self.categorical_features_mode = config.get('data', 'categorical_features_mode')
        self.features_mean = config.get('data', 'features_mean')
        self.features_median = config.get('data', 'features_median')
        self.encoding_file = config.get('data', 'encoding_file')
        self.test_data_size = config.get('data', 'test_data_size')
        self.random_state = config.get('data', 'random_state')
        self.anomaly_data_path = config.get('model', 'anomalies_path')
        self.model_path = config.get('model', 'model_path')
        self.predictions_path = config.get('model', 'predictions_path')
        self.scores_path_train = config.get('model', 'scores_path_train')
        self.scores_path_test = config.get('model', 'scores_path_test')
        self.pca_n_components = config.get('model', 'pca')['n_components']
        self.pca_enable = config.get('model', 'pca')['enable']
        self.model_name = config.get('model', 'model_name')
        self.model_params = config.get('model', 'model_params')

    def initiate_processing(self):
        print("Initiating Model Training")

    def read_data(self):
        print("Reading Data")
        self.data = pd.read_csv(self.train_data_path)
        self.uniqueID = self.data['IdentifierValue']
        self.data.drop(['IdentifierValue'], axis=1, inplace=True)

    def preprocess_data(self):
        print("Preprocessing Data")
        self.data.replace(['','NULL','np','null','missing'], np.nan, inplace=True)

        # dropping columns with more than 90% missing values
        missing_percentage = self.data.isnull().sum() / len(self.data)
        drop_cols = missing_percentage[missing_percentage > 0.9].index.tolist()
        self.data.drop(drop_cols, axis=1, inplace=True)
        drop_cols_df = pd.DataFrame({'feature': drop_cols},{'missing_percentage': missing_percentage[missing_percentage > 0.9]})
        drop_cols_df.to_csv(self.missingvalue_features_90, index=False)

        # handling date time features
        date_features = []
        for col in self.data.columns:
            if pd.api.types.is_datetime64_any_dtype(self.data[col]):
                date_features.append(col)
        self.data = convert_datetime_features(self.data, date_features)

        # dropping low variance numerical features
        numerical_features = self.data.select_dtypes(include=['int64', 'float64']).columns
        variance = self.data[numerical_features].var()
        low_variance_cols = variance[variance < 0.1].index.tolist()
        self.data.drop(low_variance_cols, axis=1, inplace=True)
        low_variance_cols_df = pd.DataFrame({'feature': drop_cols},{'variance':variance[low_variance_cols]})
        low_variance_cols_df.to_csv(self.low_variance_numerical_features, index=False)

        # drop feature with single value
        single_value_cols = self.data.columns[self.data.nunique(dropna=True) == 1].tolist()
        self.data.drop(single_value_cols, axis=1, inplace=True)
        single_value_cols_df = pd.DataFrame({'feature': single_value_cols})
        single_value_cols_df.to_csv(self.single_value_features, index=False)

        # handling missing values
        self.handle_missing_values()

        #encoding categorical features

        # find all numerical features
        numerical_features = [feature for feature in self.data.columns if self.data[feature].dtype != 'O' and self.data[feature].dtype != 'datetime64[ns]']

        # find discrete numerical features with nunique < 10
        discrete_numerical_features = [feature for feature in numerical_features if self.data[feature].nunique() < 10]

        # find continuous numerical features
        continuous_numerical_features = [feature for feature in numerical_features if feature not in discrete_numerical_features]

        # convert discrete numerical features into string
        self.data[discrete_numerical_features] = self.data[discrete_numerical_features].astype(str)

        # find all categorical features
        categorical_features = [feature for feature in self.data.columns if self.data[feature].dtype == 'O']

        self.data = frequency_ranking_encode(self.data, categorical_features)

        # find all numerical features - updated
        numerical_features = [feature for feature in self.data.columns if self.data[feature].dtype != 'O' and self.data[feature].dtype != 'datetime64[ns]']

        # standardize the data
        scaler = StandardScaler()
        self.data = scaler.fit_transform(self.data)

        # drop highly correlated features
        corr_matrix = self.data.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]
        self.data.drop(to_drop, axis=1, inplace=True)
        to_drop_df = pd.DataFrame({'feature': to_drop})
        to_drop_df.to_csv(self.high_correlation_features, index=False)

        # save all dropped features to csv
        all_dropped_features = drop_cols + low_variance_cols + single_value_cols + to_drop
        all_dropped_features_df = pd.DataFrame({'feature': all_dropped_features})
        all_dropped_features_df.to_csv(self.all_dropped_features, index=False)

        # perform PCA
        if self.pca_enable:
            pca = PCA(n_components=self.pca_n_components)
            self.data = pca.fit_transform(self.data)
            self.pca_df = pd.DataFrame({'feature': self.data.columns})
        # add unique identifier back to the data
        self.pca_df['IdentifierValue'] = self.uniqueID

        # save the final data to csv
        self.pca_df.to_csv(self.final_data_path, index=False)
    
    def handle_missing_values(self):
        # handling missing values
        # find all numerical features
        numerical_features = [feature for feature in self.data.columns if self.data[feature].dtype!='O' and self.data[feature].dtype!='datetime64[ns]']

        # calculate mean and median for each numerical feature
        mean_values = self.data[numerical_features].mean(skipna=True)
        median_values = self.data[numerical_features].median(skipna=True)

        # create a dataframe with the features, mean and median
        feature_stats = pd.DataFrame({'Feature': numerical_features, 'Mean': mean_values, 'Median': median_values})

        # write to csv file
        feature_stats.to_csv(self.numerical_features_mean_median, index=False)

        # find all categorical features
        categorical_features = self.data.select_dtypes(include=['object']).columns

        # find the high frequency category for each categorical feature
        high_frequency_categories = self.data[categorical_features].apply(lambda x: x.mode()[0])

        # create a dataframe with features and their high fequency category
        high_frequency_df = pd.DataFrame({'Feature': high_frequency_categories.index, 'High Frequency Category': high_frequency_categories.values})

        # write to csv
        high_frequency_df.to_csv(self.categorical_features_mode, index=False)

        # load stats file
        stats = pd.read_csv(self.numerical_features_mean_median)
        
        # create a dictionary for quick lookup
        mean_dict = stats.set_index('Feature')['Mean'].to_dict()
        median_dict = stats.set_index('Feature')['Median'].to_dict()
        
        # find numerical features with missing values
        numerical_features_with_missing_values = [self.data[numerical_features].isnull().mean() > 0][0].index
        
        # cols filled with mean and median
        cols_filled_with_mean = []
        cols_filled_with_median = []

        # fill all the missing values of numerical features based on outlier, in case of outlier fill with median, else mean
        for feature in numerical_features_with_missing_values:
            if self.data[feature].isnull().sum() > 0:
                q1 = self.data[feature].quantile(0.25)
                q3 = self.data[feature].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                has_outliers = (self.data[feature] < lower_bound) | (self.data[feature] > upper_bound)
                if has_outliers.any():
                    self.data[feature].fillna(median_dict[feature], inplace=True)
                    cols_filled_with_median.append(feature)
                else:
                    self.data[feature].fillna(mean_dict[feature], inplace=True)
                    cols_filled_with_mean.append(feature)
        
        # save the features filled with mean and median to csv
        mean_filled_df = pd.DataFrame({'feature': cols_filled_with_mean})
        median_filled_df = pd.DataFrame({'feature': cols_filled_with_median})
        mean_filled_df.to_csv(self.features_mean, index=False)
        median_filled_df.to_csv(self.features_median, index=False)
        
        # load the high frequency category data from the csv file
        high_frequency_categories = pd.read_csv(self.categorical_features_mode)
        
        # create dictionary for quick lookup
        high_frequency_dict = high_frequency_categories.set_index('Feature')['High Frequency Category'].to_dict()
        
        # find categorical features with missing values
        categorical_features_with_missing_values = [self.data[categorical_features].isnull().mean() > 0][0].index
        
        # fill missing values of categorical features with high frequency category
        for feature in categorical_features_with_missing_values:
            if feature in high_frequency_dict:
                self.data[feature].fillna(high_frequency_dict[feature], inplace=True)
    def get_anomalies(self):
        df_copy = pd.read_csv(self.train_data_path)
        # Get the unique identifiers from the filtered DataFrame
        identifier_values_to_retrieve = self.filtered_df['unique_id'].tolist()

        # Use these identifiers to retrieve datapoints from df_copy
        retrieved_datapoints = df_copy[df_copy['IdentifierValue'].isin(identifier_values_to_retrieve)]

        retrieved_datapoints.to_csv(self.anomaly_data_path, index=False)
        print('saved anomalies to csv')

        # write to csv
        retrieved_datapoints.to_csv('/content/drive/MyDrive/CodeCrafters_WF/Model Input Data/Data/retrieved_datapoints.csv', index=False)
    def fit_model(self):
        print("Training Model")
        DBSCAN_model = DBSCAN(**self.model_params['DBSCAN'])
        self.labels = DBSCAN_model.fit_predict(self.pca_df)
        with open(self.model_path, 'wb') as file:
            pickle.dump(DBSCAN_model, file)
        DBSCAN_model_labels = DBSCAN_model.labels_
        
        # Assuming 'labels' is the output from your DBSCAN clustering
        unique_id = self.pca_df['IdentifierValue']
        labels_with_unique_id = pd.DataFrame({'unique_id': unique_id, 'cluster_label': DBSCAN_model_labels})
        labels_with_unique_id.to_csv(self.predictions_path, index=False)

        #calculate silhoutte scores
        average_silhoutte_scores=calculate_silhouette_scores(self.pca_df,DBSCAN_model_labels)
        if average_silhoutte_scores:
            cluster_labels_below_threshold = [
                cluster_label for cluster_label, avg_score in average_silhoutte_scores.items()
                if avg_score < 0.7
            ]

            # Filter the DataFrame to include only rows with cluster labels below the threshold
            self.filtered_df = labels_with_unique_id[
                labels_with_unique_id.cluster_label.isin(cluster_labels_below_threshold)
            ]

            print(
                "Cluster labels with average silhouette score less than 0.7:",
                self.filtered_df.cluster_label.unique(),
            )
            print(self.filtered_df)
        else:
            print("No clusters found or silhouette scores not calculated.")
   
    def process(self):
        print("Processing")
        self.initiate_processing()
        self.read_data()
        self.preprocess_data()
        self.fit_model()
        self.get_anomalies()
        print("Processing Completed")