import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
file_path = "D:/College/Sem-03/DAV/Programs/Restuarant_Review_Analyzer/Hyderabad_Unique_Restaurants_Cleaned.xlsx"
df = pd.read_excel(file_path)

# Example 1: Distribution of Average Prices
plt.figure(figsize=(8,5))
sns.histplot(df["Avg_Price_Restaurant"], bins=20, kde=True, color="skyblue")
plt.title("Distribution of Average Restaurant Prices")
plt.xlabel("Average Price")
plt.ylabel("Count")
plt.tight_layout()
plt.show(block=True)   # 👈 Forces the graph window to stay open
# plt.savefig("price_distribution.png")  # 👈 Or save as image
