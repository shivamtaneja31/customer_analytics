import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class CustomerDataGenerator:
    def __init__(self):
        self.customer_ids = range(1, 1001)  # 1000 customers
        
    def generate_customer_data(self):
        data = []
        now = datetime.now()
        
        for customer_id in self.customer_ids:
            # Generate random purchase history
            num_purchases = np.random.randint(1, 20)
            for _ in range(num_purchases):
                date = now - timedelta(days=np.random.randint(0, 365))
                amount = np.random.uniform(10, 1000)
                category = np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'])
                
                data.append({
                    'customer_id': customer_id,
                    'purchase_date': date,
                    'amount': round(amount, 2),
                    'category': category,
                    'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-55', '55+']),
                    'location': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                })
        
        return pd.DataFrame(data)

    def generate_real_time_data(self):
        """Simulate real-time transaction data"""
        customer_id = np.random.choice(self.customer_ids)
        amount = np.random.uniform(10, 1000)
        category = np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'])
        
        return {
            'customer_id': customer_id,
            'purchase_date': datetime.now(),
            'amount': round(amount, 2),
            'category': category,
            'location': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
        }
