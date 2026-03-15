from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .forms import PredictionForm
import pandas as pd
import os
from django.conf import settings
import matplotlib
matplotlib.use('Agg')  # ensures matplotlib works without GUI
import matplotlib.pyplot as plt


def load_sales_data():
    file_path = os.path.join(settings.BASE_DIR, 'dataset', 'sales_data.csv')
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print("CSV Load Error:", e)
        return None


# HOME / DASHBOARD PAGE
def dashboard_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'dataset', 'sales_data.csv')

    total_sales = 0
    total_orders = 0
    avg_price = 0
    chart_path = '/static/charts/monthly_chart.png'

    top_product = "N/A"
    region_data = {}
    monthly_data = {}
    max_region_value = 1
    max_month_value = 1

    try:
        df = pd.read_csv(file_path)

        # Your CSV uses lowercase columns
        qty_col = 'quantity'
        price_col = 'price'
        product_col = 'product'
        region_col = 'region'
        date_col = 'date'

        # Make sure required columns exist
        if qty_col in df.columns and price_col in df.columns:
            # Create Sales column
            df['Sales'] = df[qty_col] * df[price_col]

            # Summary values
            total_sales = df['Sales'].sum()
            total_orders = len(df)
            avg_price = df[price_col].mean()

            # Top selling product
            if product_col in df.columns:
                product_sales = df.groupby(product_col)['Sales'].sum()
                if not product_sales.empty:
                    top_product = product_sales.idxmax()

            # Revenue by region
            if region_col in df.columns:
                region_sales = df.groupby(region_col)['Sales'].sum()
                region_data = region_sales.to_dict()
                if region_data:
                    max_region_value = max(region_data.values())

            # Monthly revenue trend from date column
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df.dropna(subset=[date_col])

                # Extract month names like Jan, Feb
                df['month_name'] = df[date_col].dt.strftime('%b')

                month_sales = df.groupby('month_name')['Sales'].sum()

                # Keep month order correct
                month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

                month_sales = month_sales.reindex(
                    [m for m in month_order if m in month_sales.index]
                )

                monthly_data = month_sales.to_dict()

                if monthly_data:
                    max_month_value = max(monthly_data.values())

                    # ---------------- CREATE CHART ---------------- #
                    charts_dir = os.path.join(settings.BASE_DIR, 'static', 'charts')
                    os.makedirs(charts_dir, exist_ok=True)

                    chart_file = os.path.join(charts_dir, 'monthly_chart.png')

                    plt.figure(figsize=(8, 4))
                    plt.plot(list(monthly_data.keys()), list(monthly_data.values()), marker='o')
                    plt.title('Monthly Sales Trend')
                    plt.xlabel('Month')
                    plt.ylabel('Revenue')
                    plt.grid(True)
                    plt.tight_layout()
                    plt.savefig(chart_file)
                    plt.close()
                    # --------------------------------------------- #

    except Exception as e:
        print("Dashboard error:", e)

    return render(request, 'dashboard.html', {
        'total_sales': round(total_sales, 2),
        'total_orders': total_orders,
        'avg_price': round(avg_price, 2),
        'chart_path': chart_path,
        'top_product': top_product,
        'region_data': region_data,
        'max_region_value': max_region_value,
        'monthly_data': monthly_data,
        'max_month_value': max_month_value,
    })


# REPORTS PAGE
def reports_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'dataset', 'sales_data.csv')

    total_sales = 0
    total_orders = 0
    avg_price = 0
    chart_path = '/static/charts/monthly_chart.png'
    table_data = []

    try:
        df = pd.read_csv(file_path)

        if 'Quantity' in df.columns and 'Price' in df.columns:
            df['Sales'] = df['Quantity'] * df['Price']
            total_sales = df['Sales'].sum()
            total_orders = len(df)
            avg_price = df['Price'].mean()
            table_data = df.head(15).to_dict(orient='records')

        elif 'quantity' in df.columns and 'price' in df.columns:
            df['Sales'] = df['quantity'] * df['price']
            total_sales = df['Sales'].sum()
            total_orders = len(df)
            avg_price = df['price'].mean()
            table_data = df.head(15).to_dict(orient='records')

    except Exception as e:
        print("Reports error:", e)

    return render(request, 'reports.html', {
        'total_sales': round(total_sales, 2),
        'total_orders': total_orders,
        'avg_price': round(avg_price, 2),
        'chart_path': chart_path,
        'table_data': table_data,
    })


# PREDICTION PAGE
def prediction_view(request):
    prediction = None

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            prediction = quantity * price
    else:
        form = PredictionForm()

    return render(request, 'prediction.html', {
        'form': form,
        'prediction': prediction
    })


# Custom Admin Dashboard (only for staff/superuser)
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_dashboard(request):
    return render(request, 'analyticsapp/admin_dashboard.html')


# ---------------- API ENDPOINTS ---------------- #

def sales_api(request):
    data = {
        "message": "Sales API is working",
        "top_product": "Biscuits",
        "total_sales": 50000
    }
    return JsonResponse(data)


def reports_api(request):
    data = {
        "message": "Reports API is working",
        "report_summary": "Monthly sales increased by 12%"
    }
    return JsonResponse(data)


def predict_api(request):
    data = {
        "message": "Prediction API is working",
        "prediction": "Next month sales may increase by 8%"
    }
    return JsonResponse(data)






# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .services import top_selling_product, revenue_by_region, monthly_revenue, predict_sales
# from .forms import PredictionForm



# def dashboard(request):
#     top_product = top_selling_product()
#     region_data = revenue_by_region()
#     monthly_data = monthly_revenue()

#     # Find highest values for graph scaling
#     max_region_value = max(region_data.values()) if region_data else 1
#     max_month_value = max(monthly_data.values) if not monthly_data.empty else 1

#     context = {
#         "top_product": top_product,
#         "region_data": region_data,
#         "monthly_data": monthly_data,
#         "max_region_value": max_region_value,
#         "max_month_value": max_month_value,
#     }

#     return render(request, "dashboard.html", context)


# @login_required
# def reports_view(request):
#     top_product = top_selling_product()
#     region_data = revenue_by_region()
#     monthly_data = monthly_revenue()

#     context = {
#         "top_product": top_product,
#         "region_data": region_data,
#         "monthly_data": monthly_data,
#     }

#     return render(request, "reports.html", context)


# @login_required
# def prediction_view(request):
#     prediction = None
#     form = PredictionForm()

#     if request.method == "POST":
#         form = PredictionForm(request.POST)

#         if form.is_valid():
#             quantity = form.cleaned_data["quantity"]
#             price = form.cleaned_data["price"]

#             prediction = predict_sales(quantity, price)

#     context = {
#         "form": form,
#         "prediction": prediction,
#     }

#     return render(request, "prediction.html", context)


