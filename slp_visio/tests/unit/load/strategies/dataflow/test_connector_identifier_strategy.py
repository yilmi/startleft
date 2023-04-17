from slp_visio.slp_visio.load.strategies.connector.impl.connector_identifier_by_connects import \
    ConnectorIdentifierByConnects
from slp_visio.slp_visio.load.strategies.connector.connector_identifier_strategy import ConnectorIdentifierStrategy
from slp_visio.slp_visio.lucid.load.strategies.connector.impl.connector_identifier_by_lucid_line_name import \
    ConnectorIdentifierByLucidLineName


class TestConnectorIdentifierStrategy:

    def test_get_strategies(self):
        # WHEN we get the strategies from CreateConnectorStrategy
        strategies = ConnectorIdentifierStrategy.get_strategies()

        # THEN we have the expected number of strategies
        assert strategies.__len__() == 2

        # AND we have the expected implementations
        assert strategies[0].__class__ == ConnectorIdentifierByConnects
        assert strategies[1].__class__ == ConnectorIdentifierByLucidLineName