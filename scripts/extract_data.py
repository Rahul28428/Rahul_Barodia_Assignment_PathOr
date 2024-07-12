import pandas as pd

def extract_sales_data(excel_file):
    df = pd.read_excel(excel_file)
    return df