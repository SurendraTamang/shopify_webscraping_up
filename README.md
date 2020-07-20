## Shopify app store scraping

## HOW TO RUN THE SCRIPT
We have two scraping 
* product_scraping.py
  
    This will help you to scrape all the urls of the products listed in shopify.
    and output the result in json file in products.json



* product_details.py
  
    This will go to each link and scrape all the details of the product each link.
  

















## OUPUT JSON FOMAT
Scrape apps.shopify.com

All apps, by category.

Return collection of json objects structured as follows:

```
{
	“categories”: [
		“marketing”,
		“store-design”,
		“sales-and-conversion-optimization”
	],
	“app_name”: “judge.me”,
	“app_page”:”https://apps.shopify.com/judgeme?surface_detail=all&surface_inter_position=1&surface_intra_position=7&surface_type=category#reviews”,
	“website”:”https://judge.me”,
	“email”:”support@judge.me”,
	“short_description”:”Site & product reviews (photos, videos, Q&A for social proof)”,
	“long_description”:”<full dump here>”,
	“reviews”: {
		“count”:2451,
		“5”:2393,
		“4”:27,
		“3”:4,
		“2”:5,
		“1”:22 
	}
	“rating”:4.9,
	“pricing”:	{
		”free”, “free”,
		“awesome”,”$15”
	}
}
```
