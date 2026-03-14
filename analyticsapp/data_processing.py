import pandas as pd
import os
from django.conf import settings
from .models import SalesRecord


def load_sales_data():

    file_path = os.path.join(settings.BASE_DIR.parent, "dataset", "sales_data.csv")

    df = pd.read_csv(file_path)

    df.dropna(inplace=True)

    df["revenue"] = df["quantity"] * df["price"]

    for _, row in df.iterrows():

        SalesRecord.objects.create(
            date=row["date"],
            product=row["product"],
            region=row["region"],
            quantity=row["quantity"],
            price=row["price"],
            revenue=row["revenue"]
        )

    print("Data loaded successfully!")