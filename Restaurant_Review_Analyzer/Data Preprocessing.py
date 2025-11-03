import pandas as pd

# Load the dataset
file_path = "D:/College/Sem-03/DAV/Programs/Restuarant_Review_Analyzer/Zomato Dataset.xlsx"
df = pd.read_excel(file_path, sheet_name="enhanced_zomato_dataset_clean")

# Step 1: Clean extra spaces in city names
df["City"] = df["City"].str.strip()

# Step 2: Keep only rows where City = Hyderabad
df_hyd = df[df["City"].str.lower() == "hyderabad"]

# Step 3: Remove duplicate restaurants, keeping the first occurrence
df_unique = df_hyd.drop_duplicates(subset="Restaurant_Name", keep="first")

# Step 4: Drop unwanted columns
cols_to_drop = ["Item_Name", "Best_Seller", "Votes", "Prices", "Is_Bestseller"]
df_unique = df_unique.drop(columns=cols_to_drop, errors="ignore")

# Step 5: Display the final processed dataset
print(df_unique)

# Save the result to a new Excel file
df_unique.to_excel("Hyderabad_Unique_Restaurants_Cleaned.xlsx", index=False)
