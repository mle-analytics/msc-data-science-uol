import pandas as pd
import os
import ssl
import nltk
import re
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from nltk.corpus import stopwords

ssl._create_default_https_context = ssl._create_unverified_context
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
except:
    stop_words = set(['the', 'and', 'for', 'with', 'this', 'that'])

file_path = "pokemon_cards_ultimate_2026.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path, sep=",", encoding="utf-8-sig")
    print("File loaded successfully!")
else:
    print("Error: The file was not found. Please check your file_path.")
    exit()

print("\n--- Data Summary ---")
print(df[['price_usd', 'image_count']].describe())

most_expensive = df.sort_values(by='price_usd', ascending=False).head(5)
print("\n--- Top 5 Most Expensive Cards ---")
print(most_expensive[['title', 'price_usd']])

rarity_summary = df.groupby('rarity_class')['price_usd'].mean().sort_values(ascending=False)
print("\n--- Average Price by Rarity Class ---")
print(rarity_summary)

text = " ".join(df['title'].astype(str)).lower()
tokens = re.findall(r'\b[a-z]{3,}\b', text)
filtered_tokens = [w for w in tokens if w not in stop_words]
f_dist = FreqDist(filtered_tokens)

output_path = "pokemon_analysis_summary.csv"
rarity_summary.to_csv(output_path)
print(f"\nAnalysis saved to: {output_path}")

f_dist.plot(15, title="Top 15 Most Common Keywords in Titles")
plt.show()