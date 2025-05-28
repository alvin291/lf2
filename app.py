from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import os
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Function to process the Excel file
def process_excel(file_path, update_option):
    try:
        # Read the Excel file and ensure the file handle is closed
        with pd.ExcelFile(file_path) as xls:  # Use context manager to ensure file is closed
            df = pd.read_excel(xls)
        
        # Validate required columns
        required_columns = ['Part Number', 'QTY']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing required columns: Part Number or QTY")
        
        # Initialize lists to store updated part numbers and quantities
        updated_part_numbers = []
        quantities = []
        
        # Iterate through rows to process data
        for index, row in df.iterrows():
            part_number = str(row['Part Number']).strip()
            qty = None
            
            # Transform Part Number
            if part_number.startswith('9') and len(part_number) < 10:
                part_number = '000' + part_number
            elif part_number.startswith('3') and len(part_number) < 10:
                part_number = '00' + part_number
            
            # Extract Quantity
            for col in ['QTY', 'QUANTITY', 'REQUIRED QUANTITY']:
                if col in df.columns and pd.notnull(row[col]):
                    qty = str(row[col]).strip()
                    break
            
            # Append processed data
            updated_part_numbers.append(part_number)
            quantities.append(qty if qty else "N/A")
        
        # Update DataFrame based on user option
        if update_option == "replace":
            df['Part Number'] = updated_part_numbers
        elif update_option == "new_column":
            df['Updated Part Number'] = updated_part_numbers
        
        # Save the updated Excel file
        excel_output_file = "updated_file.xlsx"
        df.to_excel(excel_output_file, index=False)
        
        # Create output text file
        txt_output_file = "output.txt"
        with open(txt_output_file, "w") as f:
            for pn, qty in zip(updated_part_numbers, quantities):
                f.write(f"{pn};{qty}\n")
        
        return excel_output_file, txt_output_file
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")  # Debug: Print error
        raise ValueError(f"Error processing file: {str(e)}")

# Function to fetch fun facts dynamically from Wikipedia
def fetch_linde_fun_facts():
    try:
        # Example: Fetching from Wikipedia
        url = "https://en.wikipedia.org/wiki/Linde_Material_Handling "
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract relevant sections (e.g., introduction or history)
        paragraphs = soup.find_all('p')
        fun_facts = []
        for p in paragraphs[:5]:  # Limit to first 5 paragraphs
            text = p.get_text(strip=True)
            if text:
                fun_facts.append(text)
        
        return random.choice(fun_facts)
    except Exception as e:
        print(f"Error fetching fun facts: {str(e)}")
        return "Fun fact not available."

@app.route("/", methods=["GET", "POST"])
def index():
    brand = "Unknown"  # Default brand value
    fun_fact = ""  # Initialize fun fact variable
    download = False  # Initialize download flag

    if request.method == "POST":
        # Check if a file was uploaded
        if "file" not in request.files:
            flash("No file uploaded!", "error")
            return redirect(url_for("index"))
        
        file = request.files["file"]
        
        # Check if the file is empty
        if file.filename == "":
            flash("No file selected!", "error")
            return redirect(url_for("index"))
        
        # Validate file format
        if not file.filename.endswith(('.xlsx', '.xls')):
            flash("Invalid file format! Please upload an Excel file.", "error")
            return redirect(url_for("index"))
        
        # Detect brand from file name
        file_name = file.filename.lower()
        if "linde" in file_name:
            brand = "Linde"
        elif "other_brand" in file_name:  # Add other brands as needed
            brand = "Other Brand"
        
        # Save the uploaded file temporarily
        file_path = "temp.xlsx"
        file.save(file_path)
        
        try:
            # Detect brand from the first column of Sheet1
            df = pd.read_excel(file_path)
            first_column = df.iloc[:, 0].astype(str).str.lower()  # Convert to lowercase
            if "linde" in first_column.values:
                brand = "Linde"
            elif "other_brand" in first_column.values:  # Add other brands as needed
                brand = "Other Brand"
            
            # Load fun facts for Linde
            if brand == "Linde":
                try:
                    with open(os.path.join(app.static_folder, 'brand_assets', 'linde', 'fun_facts.txt'), 'r') as f:
                        fun_facts = f.readlines()
                    # Select a single random fun fact
                    fun_fact = random.choice(fun_facts).strip()
                except FileNotFoundError:
                    # Fetch fun facts dynamically if local file is missing
                    fun_fact = fetch_linde_fun_facts()
            
            # Get the update option from the form
            update_option = request.form.get("update_option", "replace")
            
            # Process the file
            excel_output_file, txt_output_file = process_excel(file_path, update_option)
            
            # Retry deleting the temporary file with a delay
            import time
            retries = 5
            while retries > 0:
                try:
                    os.remove(file_path)
                    break  # Exit loop if deletion succeeds
                except PermissionError:
                    retries -= 1
                    time.sleep(0.5)  # Wait 0.5 seconds before retrying
            
            # Flash success message
            flash(f"File processed successfully for {brand}!", "success")
            
            # Set download flag to True
            download = True
            
            # Send both files for download
            return render_template("index.html", download=download, brand=brand, fun_fact=fun_fact)
        
        except Exception as e:
            # Retry deleting the temporary file in case of error
            import time
            retries = 5
            while retries > 0:
                try:
                    os.remove(file_path)
                    break  # Exit loop if deletion succeeds
                except PermissionError:
                    retries -= 1
                    time.sleep(0.5)  # Wait 0.5 seconds before retrying
            
            flash(str(e), "error")
            return redirect(url_for("index"))
    
    # Render the template with default values
    return render_template("index.html", download=download, brand=brand, fun_fact=fun_fact)

@app.route("/download/<file_type>")
def download(file_type):
    if file_type == "excel":
        return send_file("updated_file.xlsx", as_attachment=True)
    elif file_type == "txt":
        return send_file("output.txt", as_attachment=True)
    else:
        flash("Invalid file type!", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)