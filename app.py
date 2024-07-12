import streamlit as st
from scripts import extract_data, generate_report, email_automate
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

st.title("Daily Sales Report Generator")

# Sidebar for generating the report
st.sidebar.header("Generate Report")

# Upload Excel file
uploaded_file = st.sidebar.file_uploader("Upload Sales Data (Excel file)", type=["xlsx"])

# User inputs for column names
date_col = st.sidebar.text_input("Date Column Name", "Date")
sales_col = st.sidebar.text_input("Sales Column Name", "Sales")
product_col = st.sidebar.text_input("Product Column Name", "Product Names")

# Generate Report button
if st.sidebar.button("Generate Report"):
    if uploaded_file:
        # Extract data
        data = extract_data.extract_sales_data(uploaded_file)

        # Generate PDF report
        pdf_buffer = generate_report.generate_pdf_report(uploaded_file, sales_col, date_col, product_col)
        
        # Define the path to save the PDF
        pdf_path = os.path.join("reports", "daily_sales_report.pdf")
        
        # Save the PDF report
        with open(pdf_path, "wb") as f:
            f.write(pdf_buffer.getbuffer())

        st.success("Report generated successfully!")

        # Display the report
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download Report",
                    data=f,
                    file_name="daily_sales_report.pdf",
                    mime="application/octet-stream"
                )
    else:
        st.error("Please upload a sales data Excel file.")

# Sidebar for sending the email
st.sidebar.header("Send Email")

# Email configuration
email_to = st.sidebar.text_input("Recipient Email", "recipient@example.com")
schedule_option = st.sidebar.selectbox("Send Email", ("Now", "Schedule"))

if schedule_option == "Schedule":
    schedule_time = st.sidebar.time_input("Schedule Time")

# Send Email button
if st.sidebar.button("Send Email"):
    pdf_path = os.path.join("reports", "daily_sales_report.pdf")
    if os.path.exists(pdf_path):
        # Send email
        if schedule_option == "Now":
            email_automate.send_email("Daily Sales Report", email_to, "Management Team", pdf_path)
            st.success("Email sent successfully!")
        else:
            email_automate.schedule_email("Daily Sales Report", email_to, "Management Team", pdf_path, schedule_time.strftime("%H:%M"))
            st.success(f"Email scheduled for {schedule_time.strftime('%H:%M')}")
    else:
        st.error("Please generate the report first.")
