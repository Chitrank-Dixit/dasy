Dasy (Data (processing) System)
=====================

Installation
==============

- use `make up` to pull and create necessary containers (you can use -d option in the related up docker-compose command 
  to start containers in detached mode)
  
Usage
==========

- create migrations using `make create-migrations` (would create all the db migrations).
- destroy migrations using `make destroy-migrations` (would destroy all the db migrations).
- put the csv file in folder `/data` with name `products.csv`.  
- start products consumer using `make products-consumer` (would start processing products data that would be queued).
- start products producer using `make products-producer` (this will push all the data to products table).
- start product count consumer using `make product-count-consumer`. (would start processing product_count data that would be queued)
- start product count producer using `make product-count-producer` (this will push all the data to product_count table).

Points Acheived
===============

Done
----

- Your code should follow concept of OOPS
- Support for regular non-blocking parallel ingestion of the given file into a table. Consider thinking about the scale of what should happen if the file is to be processed in 2 mins.
- Support for updating existing products in the table based on `sku` as the primary key. (Yes, we know about the kind of data in the file. You need to find a workaround for it)
- All product details are to be ingested into a single table
- An aggregated table on above rows with `name` and `no. of products` as the columns

Improve
------

- Add ConsumerMixin and ProducerMixin, such that it would acheive a single source for producer and consumer logic.
- refactor code for products and product_count producer consumer flow adding better reusability.
- Improve tests for producer consumer flow.
- explore event driven approach for adding product and no_of_product each time a new record is updated. I had tried using triggers (which are obviously slow).
but a separate process to lookup products table and fill up product_count table would be very nice to have.
  
DB schema
----------
- I have added db schema in `dasy/migrations` folder.