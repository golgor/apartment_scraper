# apartment_scraper
This is a project used to get information about apartments available to rent or buy from Willhaben.at, on the biggest platforms available in Austria. You can select yourself what areas of Austria you are interested in, as well as if it is for buying or renting. The data will then be saved in a local database that easily can be used to get a good overview of the market.

## Possible improvements
- Currently it only stores data in the database. It would be nice with some kind of export to for example .csv or excel files.
- Currently only supports Willhaben.at. Might be of interest to add other platforms as well.

## How to use
Checkout out the repo from Github:
```bash
git clone https://github.com/golgor/apartment_scraper.git
```
Then install it as editable install using pip:
```
pip install -e .
```
Customize __main__.py accordingly, execute it, and you will then find the database in the folder of the package, typically `apartment_scraper/apartment_scraper/test.db`.

### Use API
To use the API, go into the folder `api`, and run:
```bash
uvicorn api:app --reload
```