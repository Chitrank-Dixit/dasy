from click.testing import CliRunner

from dasy.dasy import checkCommand
from dasy.models import Product, ProductCount
from dasy.utils import DBUtils


class TestModelsBase:
    def setup(self):
        db_utils = DBUtils()
        self.master = db_utils.get_router()
        runner = CliRunner()
        result = runner.invoke(checkCommand, ["-m", "forward"])
        assert result.exit_code == 0

    def teardown(self):
        del self.master


class TestProductsModel(TestModelsBase):
    def test_insert(self):

        audit = Product(
            sku="test-1",
            name="Test User",
            description="This is just a test description"
        )
        self.master.add(audit)
        self.master.commit()
        data = (
            self.master.query(Product)
            .filter(Product.sku == "test-1")
            .all()
        )
        self.master.close()
        assert len(data) == 1

    def test_read(self):
        data = (
            self.master.query(Product)
                .filter(Product.sku == "test-1")
                .all()
        )
        self.master.close()
        assert len(data) == 1

    def test_update(self):
        product = (
            self.master.query(Product)
                .filter(Product.sku == "test-1")
                .first()
        )
        product.description = "Sample description"
        self.master.commit()

        data = (
            self.master.query(Product)
                .filter(Product.sku == "test-1")
                .first()
        )
        self.master.close()
        assert data.description == "Sample description"

    def test_delete(self):
        product = (
            self.master.query(Product)
                .filter(Product.sku == "test-1")
                .first()
        )
        self.master.delete(product)
        self.master.commit()
        data = (
            self.master.query(Product)
                .filter(Product.sku == "test-1")
                .all()
        )
        self.master.close()
        assert len(data) == 0


class TestProductCountModel(TestModelsBase):
    def test_insert(self):

        audit = ProductCount(
            name="Test User",
            no_of_products=12
        )
        self.master.add(audit)
        self.master.commit()
        data = (
            self.master.query(ProductCount)
            .filter(ProductCount.name == "Test User")
            .all()
        )
        self.master.close()
        assert len(data) == 1

    def test_read(self):
        data = (
            self.master.query(ProductCount)
                .filter(ProductCount.name == "Test User")
                .all()
        )
        self.master.close()
        assert len(data) == 1

    def test_update(self):
        product_count = (
            self.master.query(ProductCount)
                .filter(ProductCount.name == "Test User")
                .first()
        )
        product_count.no_of_products = 200
        self.master.commit()

        data = (
            self.master.query(ProductCount)
                .filter(ProductCount.name == "Test User")
                .first()
        )
        self.master.close()
        assert data.no_of_products == 200

    def test_delete(self):
        product_count = (
            self.master.query(ProductCount)
                .filter(ProductCount.name == "Test User")
                .first()
        )
        self.master.delete(product_count)
        self.master.commit()
        data = (
            self.master.query(ProductCount)
                .filter(ProductCount.name == "Test User")
                .all()
        )
        self.master.close()
        assert len(data) == 0
