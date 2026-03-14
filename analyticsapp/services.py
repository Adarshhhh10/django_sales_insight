import pandas as pd
from .models import SalesRecord
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_dataframe():

    data = SalesRecord.objects.all().values()

    df = pd.DataFrame(data)

    return df


def top_selling_product():

    df = get_dataframe()

    result = df.groupby('product')['quantity'].sum()

    return result.idxmax()


def revenue_by_region():

    df = get_dataframe()

    result = df.groupby('region')['revenue'].sum()

    return result.to_dict()


def monthly_revenue():

    df = get_dataframe()

    df['date'] = pd.to_datetime(df['date'])

    df['month'] = df['date'].dt.to_period('M')

    result = df.groupby('month')['revenue'].sum()

    return result


from sklearn.linear_model import LinearRegression
import numpy as np

def predict_sales(quantity, price):

    df = get_dataframe()

    X = df[['quantity','price']]

    y = df['revenue']

    model = LinearRegression()

    model.fit(X, y)

    prediction = model.predict([[quantity,price]])

    return round(prediction[0],2)


import matplotlib.pyplot as plt
import os
from django.conf import settings

def create_region_chart():

    df = get_dataframe()

    data = df.groupby('region')['revenue'].sum()

    plt.figure()

    data.plot(kind='bar')

    plt.title("Revenue by Region")

    plt.ylabel("Revenue")

    chart_path = os.path.join(settings.BASE_DIR.parent,"static","charts","region_chart.png")

    plt.savefig(chart_path)

    plt.close()



def create_monthly_chart():

    df = get_dataframe()

    df['date'] = pd.to_datetime(df['date'])

    df['month'] = df['date'].dt.to_period('M')

    data = df.groupby('month')['revenue'].sum()

    plt.figure()

    data.plot(kind='line',marker='o')

    plt.title("Monthly Revenue Trend")

    plt.ylabel("Revenue")

    chart_path = os.path.join(settings.BASE_DIR.parent,"static","charts","monthly_chart.png")

    plt.savefig(chart_path)

    plt.close()