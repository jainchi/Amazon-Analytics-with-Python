# Amazon-Analytics-with-Python-Pandas

End-to-end exploratory analysis of a simulated Amazon-style multi-table e-commerce dataset, built entirely in Python/Pandas. The project answers 40+ business questions across customers, sellers, products, and operations, organized into function-based sections for readability and reuse.

## Dataset

9 relational CSV tables, joined on the following primary keys:

| Table | Primary Key | Description |
|---|---|---|
| `customers.csv` | `customer_id` | Customer demographics + state |
| `orders.csv` | `order_id` | Order-level records, linked to customer & seller |
| `order_items.csv` | `order_item_id` | Line items per order (product, quantity, price) |
| `products.csv` | `product_id` | Product catalog |
| `category.csv` | `category_id` | Product categories |
| `sellers.csv` | `seller_id` | Seller info, including origin |
| `shipping.csv` | `shipping_id` | Delivery status & shipping provider |
| `payments.csv` | `payment_id` | Payment status per order |
| `inventory.csv` | `inventory_id` | Stock levels per product/warehouse |

**Scale:** 765 products, 54 sellers, ~682 customers, 21,141 shipments, order history from Jan 2020 – Jul 2024 (2024 is a partial year).

## Tech stack

- Python 3 / Pandas (3.0+, using native `how='left_anti'` merges)
- NumPy

## Project structure

The analysis script is organized into five sections, each a set of standalone functions that can be run independently:

- **Category Murder** — revenue & quantity contribution by category, unique customers per category, sellers active across all categories
- **Customers Murder** — customer lifetime value, no-purchase customers, repeat/retention rates, return behavior, geographic breakdown
- **Seller's Murder** — revenue & quantity per seller, above-average sellers, return rates, YoY growth, inactive sellers
- **Products Murder** — revenue by product, cross-seller product coverage, YoY decline detection
- **Miscellaneous Killing** — shipping provider revenue, inventory alerts, delivery delays, monthly trend, order status breakdown

## Key insights

**Customers**
- 212 of ~894 customers have never placed an order
- 94.46% of customers who ordered, ordered more than once
- Returns are highly concentrated: only 30 of 682 customers (≈4.4%) have ever had a return, and most of those return ~100% of their orders — a strong anomaly signal, not organic behavior
- Returning customers are concentrated in just 7 of 49 US states (South Carolina highest)

**Sellers**
- Return behavior is normal and volume-correlated on the seller side (r ≈ 0.996 between order volume and return count) — unlike the customer-side anomaly, this looks like healthy, expected business variance
- Return *rate* ranges narrowly from ~4% to ~29% across all sellers, with no correlation to seller size (r ≈ 0.026)
- 2 sellers (Clorox, Lysol) have never received an order
- Ailun reaches the most states (38); most sellers are US-based

**Products**
- Top revenue product: Apple iMac Pro (~$630K)
- Only 79 of 765 products (≈10%) are sold by more than half of all sellers — most products are carried by a narrower seller subset
- Apple AirPods Max leads on states reached and unique customers, but not on revenue
- Product ID 6 has the most returns (23) — flagged for potential quality/logistics investigation

**Operations**
- FedEx contributes the most shipping revenue of the 3 providers
- 236 products are low-stock (<30 units)
- Median delivery time is 3 days (range 1–5); ~40% of orders take longer than 3 days
- 2022 had both the highest raw return count and highest return rate (14.04%) of any year — the only year where both measures agree, even after normalizing for shipment volume

## Known data caveats (handled in the analysis)

- **Partial 2024 data**: order history ends July 30, 2024, so 2024 has ~58% of a full year's data. All YoY comparisons involving 2024 exclude it to avoid a misleading ~85% "decline" artifact.
- **`delivery_status` had inconsistent whitespace** in the raw data (e.g. `'Returned '`); stripped once at load time rather than patched per-query.
- **Wyoming is the only US state with zero customers** in this dataset.

## Running it

```bash
pip install pandas numpy
python amazon_analysis.py
```

Each question is a standalone function (e.g. `customer_q1()`, `seller_q7()`) — call individually or run the full script to execute all of them in sequence.


-----
Chitransh Jain
