import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Define the File Path
# This is the location of the file you pointed out
input_file_path = 'RAW_DATA/Covid_19/COVID-19 data from John Hopkins University/CONVENIENT_global_confirmed_cases.csv'

# 2. Load the Data
try:
    # Read the CSV
    raw_df = pd.read_csv(input_file_path)
    
    # Rename first column for clarity
    raw_df.rename(columns={'Country/Region': 'Date'}, inplace=True)
    
    # 3. Select Country and Clean
    target_country = 'India' # Change this to 'US', 'China', 'Italy' etc. as needed

    if target_country in raw_df.columns:
        # Skip the metadata row (row 0 contains province names)
        country_data = raw_df[['Date', target_country]].iloc[1:].copy()
        
        # Rename columns
        country_data.columns = ['Date', 'New_Cases']
        country_data['Date'] = pd.to_datetime(country_data['Date'])
        
        # Convert to numeric (coercing errors to NaN, then filling with 0)
        country_data['New_Cases'] = pd.to_numeric(country_data['New_Cases'], errors='coerce').fillna(0)
        
        # 4. Calculate Cumulative "Confirmed"
        country_data['Confirmed'] = country_data['New_Cases'].cumsum()
        
        # 5. Add 'Day' column
        start_date = country_data['Date'].min()
        country_data['Day'] = (country_data['Date'] - start_date).dt.days
        
        # Reorder columns
        df_final = country_data[['Date', 'Day', 'Confirmed', 'New_Cases']].reset_index(drop=True)
        
        
        # Create the new filename
        output_filename = f'processed_{target_country}_data.csv'
        
        # Combine them to get the full output path
        output_path = os.path.join('temp_DATA', output_filename)
        
        df_final.to_csv(output_path, index=False)
        
        print(f"Success! Processed data saved at:\n{output_path}")
        print(df_final.head())
        
        # Optional: Quick Plot
        plt.figure(figsize=(10, 5))
        plt.plot(df_final['Day'], df_final['Confirmed'])
        plt.title(f"{target_country} Cumulative Cases")
        plt.show()
        
    else:
        print(f"Error: Country '{target_country}' not found in the file.")

except FileNotFoundError:
    print(f"Error: Could not find the file at {input_file_path}")
    print("Please check your folder structure.")