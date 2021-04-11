from sqlalchemy import Column, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):

    __tablename__ = "products"
    sku = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)


class ProductCount(Base):

    __tablename__ = "product_count"
    name = Column(Text, primary_key=True)
    no_of_products = Column(Integer, default=0)

#Base.metadata.bind = get_engine()
#Base.metadata.create_all()


