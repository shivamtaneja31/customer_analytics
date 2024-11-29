from flask import Flask, render_template, jsonify
import json
import pandas as pd
from data_generator import CustomerDataGenerator
from analytics import CustomerAnalytics
import plotly
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import threading
import time
import queue

app = Flask(__name__)

# Initialize data and analytics
data_generator = CustomerDataGenerator()
initial_data = data_generator.generate_customer_data()
analytics = CustomerAnalytics(initial_data)

# Simulate real-time data queue
real_time_queue = queue.Queue()

def real_time_data_generator():
    """Background thread to generate real-time data"""
    while True:
        new_data = data_generator.generate_real_time_data()
        real_time_queue.put(new_data)
        time.sleep(2)  # Generate new data every 2 seconds

# Start real-time data generation thread
threading.Thread(target=real_time_data_generator, daemon=True).start()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/customer-segments')
def customer_segments():
    segments = analytics.segment_customers()
    fig = px.scatter(
        segments,
        x='total_spend',
        y='purchase_count',
        color='segment',
        title='Customer Segments'
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/api/category-insights')
def category_insights():
    insights = analytics.get_category_insights()
    fig = px.bar(
        insights,
        x='category',
        y='total_revenue',
        title='Revenue by Category'
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/api/time-series')
def time_series():
    analysis = analytics.get_time_series_analysis()
    fig = px.line(
        analysis,
        x='date',
        y='total_sales',
        title='Daily Sales Trend'
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/api/churn-risk')
def churn_risk():
    churn_data = analytics.predict_churn_risk()
    risk_counts = churn_data['churn_risk'].value_counts()
    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title='Customer Churn Risk Distribution'
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/api/real-time-transactions')
def real_time_transactions():
    # Get latest transactions from queue
    transactions = []
    while not real_time_queue.empty() and len(transactions) < 10:
        transactions.append(real_time_queue.get())
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True)
