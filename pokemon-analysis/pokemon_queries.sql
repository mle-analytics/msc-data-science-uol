-- 1. Look at the first 10 rows
SELECT * FROM 'pokemon-analysis/pokemon_cards_ultimate_2026.csv'
LIMIT 10;

-- 2. Find the most expensive rarity classes (Average Price)
SELECT 
    rarity_class, 
    ROUND(AVG(price_usd), 2) as avg_price,
    COUNT(*) as card_count
FROM 'pokemon-analysis/pokemon_cards_ultimate_2026.csv'
GROUP BY rarity_class
ORDER BY avg_price DESC;

-- 3. Find "Charizard" cards priced over $100
SELECT title, price_usd, rarity_class
FROM 'pokemon-analysis/pokemon_cards_ultimate_2026.csv'
WHERE title ILIKE '%Charizard%' 
  AND price_usd > 100
ORDER BY price_usd DESC;