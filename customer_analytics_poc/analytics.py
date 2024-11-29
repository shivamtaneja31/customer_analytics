import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

class CustomerAnalytics:
    def __init__(self, data):
        self.data = data
        self.scaler = StandardScaler()
        
    def calculate_customer_metrics(self):
        """Calculate key customer metrics"""
        customer_metrics = self.data.groupby('customer_id').agg({
            'amount': ['count', 'sum', 'mean'],
            'purchase_date': ['min', 'max']
        }).reset_index()
        
        customer_metrics.columns = ['customer_id', 'purchase_count', 'total_spend', 
                                  'average_spend', 'first_purchase', 'last_purchase']
        
        # Calculate days since last purchase and customer lifetime
        now = datetime.now()
        customer_metrics['days_since_last_purchase'] = (
            now - pd.to_datetime(customer_metrics['last_purchase'])
        ).dt.days
        
        customer_metrics['customer_lifetime_days'] = (
            pd.to_datetime(customer_metrics['last_purchase']) - 
            pd.to_datetime(customer_metrics['first_purchase'])
        ).dt.days
        
        return customer_metrics
    
    def segment_customers(self, n_clusters=4):
        """Segment customers using K-means clustering"""
        metrics = self.calculate_customer_metrics()
        
        # Select features for clustering
        features = ['purchase_count', 'total_spend', 'average_spend', 
                   'days_since_last_purchase', 'customer_lifetime_days']
        
        # Scale the features
        X = self.scaler.fit_transform(metrics[features])
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        metrics['segment'] = kmeans.fit_predict(X)
        
        return metrics
    
    def predict_churn_risk(self):
        """Simple churn risk prediction based on customer behavior"""
        metrics = self.calculate_customer_metrics()
        
        # Define simple rules for churn risk
        metrics['churn_risk'] = 'Low'
        metrics.loc[metrics['days_since_last_purchase'] > 90, 'churn_risk'] = 'Medium'
        metrics.loc[metrics['days_since_last_purchase'] > 180, 'churn_risk'] = 'High'
        
        return metrics
    
    def get_category_insights(self):
        """Analyze purchase patterns by category"""
        category_insights = self.data.groupby('category').agg({
            'amount': ['count', 'sum', 'mean'],
            'customer_id': 'nunique'
        }).reset_index()
        
        category_insights.columns = ['category', 'transaction_count', 
                                   'total_revenue', 'average_transaction', 
                                   'unique_customers']
        
        return category_insights
    
    def get_time_series_analysis(self):
        """Analyze purchase trends over time"""
        self.data['purchase_date'] = pd.to_datetime(self.data['purchase_date'])
        daily_sales = self.data.groupby(
            self.data['purchase_date'].dt.date
        )['amount'].agg(['sum', 'count']).reset_index()
        
        daily_sales.columns = ['date', 'total_sales', 'transaction_count']
        return daily_sales
