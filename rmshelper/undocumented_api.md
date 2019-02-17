# Undocumented API Methods

Methods in the Current RMS API that aren't documented. A quick reference guide for myself.

## Opportunities
### Find opportunities with a given a stock level ID

```
GET /opportunities?q[opportunity_items_item_assets_stock_level_id_eq]=1234
```
## Stock Levels
###  Get a stock level by Asset Number (Barcode)

```
GET /stock_levels?q[asset_number_eq]=123-456
```
