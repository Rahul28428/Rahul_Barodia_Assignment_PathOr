import time
import pandas as pd
from scripts import extract_data
from scripts import generate_report
from scripts import email_automate

def confirm_prompt(prompt, filename_prompt=None):
    while True:
        if filename_prompt:
            response = input(f"You: {filename_prompt} (yes/no): ").strip().lower()
        else:
            response = input(f"You: {prompt} (yes/no): ").strip().lower()
            
        if response == 'yes':
            return True
        elif response == 'no':
            return False
        else:
            print("AI: Please respond with 'yes' or 'no'.")

def conversational_agent():
    print("AI: Hi! How can I help you today?")
    while True:
        user_input = input("You: ")
        
        if "report" in user_input.lower():
            filename_prompt = input("You: Please enter the file name for data extraction: ").strip()
            confirm_file = confirm_prompt("Do you want to use this file for data extraction?", filename_prompt)
            
            if confirm_file:
                date_col = input("You: Please enter the column name for Date: ").strip()
                sales_col = input("You: Please enter the column name for Sales: ").strip()
                product_col = input("You: Please enter the column name for Product Names: ").strip()
                
                print("AI: Generating report...")
                try:
                    sales_data = extract_data.extract_sales_data(filename_prompt)
                    if sales_data is not None:
                        total_sales = sales_data[sales_col].sum()
                        avg_sales = sales_data[sales_col].mean()
                        min_sales = sales_data[sales_col].min()
                        max_sales = sales_data[sales_col].max()
                        
                        summary = f"Total Sales: {total_sales}\nAverage Sales: {avg_sales}\nMin Sales: {min_sales}\nMax Sales: {max_sales}"
                        print(f"AI: Summary:\n{summary}")
                        
                        generate_pdf = confirm_prompt("Do you want me to generate a PDF report?")
                        if generate_pdf:
                            pdf_buffer = generate_report.generate_pdf_report(filename_prompt, sales_col, date_col, product_col)
                            pdf_path = "reports/daily_sales_report.pdf"
                            with open(pdf_path, "wb") as f:
                                f.write(pdf_buffer.getbuffer())
                            print("AI: Report generated successfully.")
                        
                        send_email_confirm = confirm_prompt("Do you want me to send the report via email?")
                        if send_email_confirm:
                            receiver_email = input("You: Please enter the recipient's email address: ").strip()
                            schedule_email = input("You: Do you want to send it now or schedule it? (now/schedule): ").strip().lower()
                            if schedule_email == "now":
                                email_automate.send_email("Daily Sales Report", receiver_email, "Recipient", "reports/daily_sales_report.pdf")
                                print("AI: Email sent successfully!")
                                break
                            elif schedule_email == 'schedule':
                                schedule_time = input("You: Please enter the scheduling time (format: HH:MM): ").strip()
                                email_automate.schedule_email("Daily Sales Report", receiver_email, "Management Team", pdf_path, schedule_time)
                                print(f"AI: Email scheduled for {schedule_time}.")
                
                except KeyError as e:
                    print(f"AI: Error accessing column '{e.args[0]}'. Please check the column name.")
                
                except Exception as e:
                    print(f"AI: An error occurred: {str(e)}")
        
        elif "exit" in user_input.lower():
            print("AI: Goodbye!")
            break
        
        else:
            print("AI: Sorry, I didn't understand that. Please try again.")

if __name__ == "__main__":
    conversational_agent()
