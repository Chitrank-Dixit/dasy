import pytest
from click.testing import CliRunner
from dasy.dasy import checkCommand


class TestSideEffectArguments(object):
    def test_help_option(self):
        runner = CliRunner()
        result = runner.invoke(checkCommand, ["--help"])
        assert result.exit_code == 0
        assert (
            result.output
            == "Usage: checkcommand [OPTIONS]\n\n  CLI tool to process large files\n\nOptions:\n  -w, --write-from TEXT  write data to the db\n  -r, --read-from TEXT   read data from the db\n  -m, --migrate TEXT     migrate db\n  -t, --test TEXT        to test producer consumer flow\n  --help                 Show this message and exit.\n"
        )

    def test_create_migrations(self):
        runner = CliRunner()
        result = runner.invoke(checkCommand, ["-m", "forward"])
        assert result.exit_code == 0

    @pytest.mark.parametrize(
        "producer_args, consumer_args,",
        [("./data/product_test.csv", "products",), ("product_count", "product_count",)],
    )
    def test_producer_consumers(self, producer_args, consumer_args):
        runner = CliRunner()
        result = runner.invoke(checkCommand, ["-w", producer_args])
        assert result.exit_code == 0

        result = runner.invoke(checkCommand, ["-r", consumer_args, '--test', 'true'])
        assert result.exit_code == 0
        assert result.output == 'records stored in db...\n'

    def test_destroy_migrations(self):
        runner = CliRunner()
        result = runner.invoke(checkCommand, ["-m", "backward"])
        assert result.exit_code == 0

