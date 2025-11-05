import zipfile
import os
import pandas as pd

zip_path = r"C:\Users\Administrator\Downloads\archive (8).zip"  # the zip file
extract_to = r"C:\Users\Administrator\Desktop\olist_data"       # folder to extract CSVs
os.makedirs(extract_to, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_to)

print("Extracted files to:", extract_to)
print("Files in extracted folder:", os.listdir(extract_to)[:50])

def load_if_exists(name):
    path = os.path.join(extract_to, name)
    if os.path.exists(path):
        print("Loading", name)
        return pd.read_csv(path)
    else:
        print("Missing:", name)
        return None

orders    = load_if_exists("olist_orders_dataset.csv")
customers = load_if_exists("olist_customers_dataset.csv")
items     = load_if_exists("olist_order_items_dataset.csv")
products  = load_if_exists("olist_products_dataset.csv")
payments  = load_if_exists("olist_order_payments_dataset.csv")
reviews   = load_if_exists("olist_order_reviews_dataset.csv")
sellers   = load_if_exists("olist_sellers_dataset.csv")
geo       = load_if_exists("olist_geolocation_dataset.csv")

for name, df in [("orders",orders),("customers",customers),("items",items),
                 ("products",products),("payments",payments),("reviews",reviews),
                 ("sellers",sellers),("geo",geo)]:
    if df is not None:
        print(name, "shape:", df.shape)


datasets={
    "orders": orders,
    "customers": customers,
    "items": items,
    "products": products,
    "payments": payments,
    "reviews": reviews,
    "sellers": sellers,
    "geo": geo
    

}

for name, df in datasets.items():
    if df is not None:
        print(f"\n{name.upper()} (shape: {df.shape}):")
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if missing.empty:
            print("  No missing values.")
        else:
            print("  Missing values (only >0):")
            print(missing)
        print("  Duplicate rows:", df.duplicated().sum())



orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])


products['product_weight_g'].fillna(products['product_weight_g'].median(), inplace=True)
products['product_length_cm'].fillna(products['product_length_cm'].median(), inplace=True)
products['product_height_cm'].fillna(products['product_height_cm'].median(), inplace=True)
products['product_width_cm'].fillna(products['product_width_cm'].median(), inplace=True)


products['product_category_name'].fillna('unknown', inplace=True)
products['product_name_lenght'].fillna(0, inplace=True)
products['product_description_lenght'].fillna(0, inplace=True)
products['product_photos_qty'].fillna(0, inplace=True)



reviews['review_comment_title'].fillna('No comment', inplace=True)
reviews['review_comment_message'].fillna('No comment', inplace=True)

# Remove duplicate geolocation rows
geo.drop_duplicates(inplace=True)

# Quick check
print(orders.isnull().sum())
print(products.isnull().sum())
print(reviews.isnull().sum())
print("Geo duplicates after cleaning:", geo.duplicated().sum())



import os
output_path = r"C:\Users\Administrator\Desktop\olist_cleaned_data"
os.makedirs(output_path, exist_ok=True)


orders.to_csv(os.path.join(output_path, "orders_cleaned.csv"), index=False)
customers.to_csv(os.path.join(output_path, "customers_cleaned.csv"), index=False)
items.to_csv(os.path.join(output_path, "order_items_cleaned.csv"), index=False)
products.to_csv(os.path.join(output_path, "products_cleaned.csv"), index=False)
payments.to_csv(os.path.join(output_path, "payments_cleaned.csv"), index=False)
reviews.to_csv(os.path.join(output_path, "reviews_cleaned.csv"), index=False)
sellers.to_csv(os.path.join(output_path, "sellers_cleaned.csv"), index=False)
geo.to_csv(os.path.join(output_path, "geolocation_cleaned.csv"), index=False)

print("✅ All cleaned datasets saved to:", output_path)



