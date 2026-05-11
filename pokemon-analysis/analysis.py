import pandas as pd
import os
import ssl
import nltk
import re
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from nltk.corpus import stopwords

# --- 1. ENVIRONMENT SETUP ---
# Handle SSL for NLTK downloads on macOS
ssl._create_default_https_context = ssl._create_unverified_context

try:
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
except Exception as e:
    print(f"NLTK Download failed, using fallback stopwords. Error: {e}")
    stop_words = set(['the', 'and', 'for', 'with', 'this', 'that'])

# --- 2. SMART FILE PATHING ---
# This ensures the script finds the CSV if it's in the same folder as this .py file
script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = "pokemon_cards_ultimate_2026.csv"
file_path = os.path.join(script_dir, file_name)

# --- 3. DATA LOADING ---
if os.path.exists(file_path):
    df = pd.read_csv(file_path, sep=",", encoding="utf-8-sig")
    print(f"✅ Success: File loaded from {file_path}")
else:
    print(f"❌ Error: Could not find {file_name}")
    print(f"Looking in: {script_dir}")
    exit()

# --- 4. DATA ANALYSIS ---
print("\n" + "="*30)
print("       DATA SUMMARY")
print("="*30)
print(df[['price_usd', 'image_count']].describe())

# Top 5 most expensive
most_expensive = df.sort_values(by='price_usd', ascending=False).head(5)
print("\n--- Top 5 Most Expensive Cards ---")
print(most_expensive[['title', 'price_usd']])

# Rarity analysis
rarity_summary = df.groupby('rarity_class')['price_usd'].mean().sort_values(ascending=False)
print("\n--- Average Price by Rarity Class ---")
print(rarity_summary)

# --- 5. NLP / TEXT TRENDS ---
# Combine all titles into one lowercase string
text = " ".join(df['title'].astype(str)).lower()

# Extract words (3 letters or more)
tokens = re.findall(r'\b[a-z]{3,}\b', text)

# Filter out stopwords
filtered_tokens = [w for w in tokens if w not in stop_words]
f_dist = FreqDist(filtered_tokens)

# --- 6. EXPORT & VISUALIZATION ---
output_path = os.path.join(script_dir, "pokemon_analysis_summary.csv")
rarity_summary.to_csv(output_path)
print(f"\n📁 Analysis saved to: {output_path}")

# Generate Plot
plt.figure(figsize=(10, 6))
f_dist.plot(15, title="Top 15 Most Common Keywords in Pokemon Titles")
plt.show()