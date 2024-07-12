import pandas as pd
from fpdf import FPDF
from scripts import extract_data
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

def generate_pdf_report(file_path, sales_col, date_col, product_col):
    # Loading data from Excel
    df = pd.read_excel(file_path)
    
    total_sales = df[sales_col].sum()
    average_sales_per_day = df.groupby(date_col)[sales_col].mean().mean()
    top_selling_products = df.groupby(product_col)[sales_col].sum().nlargest(5)
    
    # Creating PDF canvas
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Daily Sales Report")
    
    # Adding introductory information
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Total Sales: ${total_sales:.2f}")
    c.drawString(50, 700, f"Average Sales per Day: ${average_sales_per_day:.2f}")
    
    # Table 1: Top Selling Products
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 670, "Top Selling Products:")
    c.setFont("Helvetica", 12)
    y_position = 650
    for idx, (product, sales) in enumerate(top_selling_products.items(), start=1):
        c.drawString(70, y_position - idx * 20, f"{idx}. {product}: ${sales:.2f}")
    
    y_position -= len(top_selling_products) * 20 + 50

    # Visualization 1: Sales Trend Over Time
    plt.figure(figsize=(8, 4))
    df.groupby(date_col)[sales_col].sum().plot(kind='line', marker='o')
    plt.title('Sales Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales ($)')
    plt.tight_layout()
    sales_trend_image = BytesIO()
    plt.savefig(sales_trend_image, format='png')  
    sales_trend_image.seek(0)
    
    # Checking if there is enough space on current page for the image
    if y_position - 300 < 50:
        c.showPage()  
        y_position = 750  
    c.drawImage(ImageReader(sales_trend_image), 50, y_position - 300, width=500, height=250)  # Adjust y_position for image
    plt.close()

    y_position -= 350
    
    # Visualization 2: Product Line Sales Distribution
    plt.figure(figsize=(6, 6))
    df.groupby(product_col)[sales_col].sum().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Product Line Sales Distribution')
    plt.ylabel('')
    plt.tight_layout()
    product_sales_image = BytesIO()
    plt.savefig(product_sales_image, format='png')
    product_sales_image.seek(0)
    
    # Checking if there is enough space on current page for the image
    if y_position - 400 < 50:
        c.showPage()  
        y_position = 750 
    c.drawImage(ImageReader(product_sales_image), 50, y_position - 400, width=400, height=400)  # Adjust y_position for image
    plt.close()
    
    # Saving PDF and closing canvas
    c.save()
    
    # Returning the buffer containing the PDF data
    buffer.seek(0)
    return buffer
