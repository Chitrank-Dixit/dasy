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
- start products consumer using `make products-consumer` (would start processing products data that would be queued).
- start products producer using `make products-producer` (this will push all the data to products table).
- start product count consumer using `make product-count-consumer`. (would start processing product_count data that would be queued)
- start product count producer using `make product-count-producer` (this will push all the data to product_count table).

