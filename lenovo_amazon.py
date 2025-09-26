# Step 1: Import Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Step 2: Set search URL and headers
search_query = "lenovo+laptop"
base_url = "https://www.amazon.in/s?k=" + search_query

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9"
}

# Step 3: Create empty lists to store data
product_names = []
product_prices = []
product_ratings = []
product_reviews = []

# Step 4: Loop through first 5 pages
for page in range(1, 6):
    print(f"Scraping page {page}...")
    url = base_url + f"&page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Step 5: Find all product containers
    containers = soup.find_all("div", {"data-component-type": "s-search-result"})
    
    # Step 6: Extract data from each container
    for container in containers:
        # Product Name
        name_tag = container.h2
        name = name_tag.text.strip() if name_tag else "No Name"
        product_names.append(name)
        
        # Product Price (Updated Extraction)
        price_tag = container.find("span", class_="a-price")
        if price_tag:
            price_whole = price_tag.find("span", class_="a-price-whole")
            price_fraction = price_tag.find("span", class_="a-price-fraction")
            if price_whole and price_fraction:
                price = price_whole.text + price_fraction.text
            elif price_whole:
                price = price_whole.text
            else:
                price = "0"
        else:
            price = "0"
        product_prices.append(price.replace(',', ''))
        
        # Product Rating
        rating_tag = container.find("span", class_="a-icon-alt")
        rating = rating_tag.text if rating_tag else "No Rating"
        product_ratings.append(rating)
        
        # Number of Reviews
        review_tag = container.find("span", {"class": "a-size-base"})
        review = review_tag.text if review_tag else "0"
        product_reviews.append(review.replace(',', ''))
    
    # Delay to avoid being blocked
    time.sleep(2)

# Step 7: Create DataFrame
df = pd.DataFrame({
    "Product Name": product_names,
    "Price (INR)": product_prices,
    "Rating": product_ratings,
    "Reviews": product_reviews
})

# Step 8: Save to CSV
df.to_csv("amazon_lenovo_laptops.csv", index=False)
print("Scraping complete! Data saved to amazon_lenovo_laptops.csv")
