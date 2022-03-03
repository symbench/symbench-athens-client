import logging

from gremlin_python.driver.client import Client

from symbench_athens_client.queries import CLONE_QUERY
from symbench_athens_client.utils import get_logger


class GraphDBDriver:
    def __init__(self, gremlin_url="ws://localhost:8182/gremlin", log_level=None):
        import nest_asyncio  # Hack to make it work in jupyter notebook. Further Investigating necessary

        nest_asyncio.apply()
        self.gremlin_url = gremlin_url
        self.logger = get_logger(
            self.__class__.__name__, level=log_level or logging.DEBUG
        )

        self.client = Client(gremlin_url, "g")
        self.logger.info(f"Connected to gremlin server at {self.gremlin_url}")

    def close(self):
        self.client.close()

    def run_queries(self, queries, commit=False):
        request_options = {"evaluationTimeout": 0}
        for query in queries:
            result_set = self.client.submit(query, request_options=request_options)
            self.logger.debug(f"Successfully ran query: {query}")
            future_results = result_set.all()
            results = future_results.result()
            self.logger.debug(f"Query Results: {results}")

        if commit:
            self.client.submit("g.tx().commit()", request_options=request_options)

        self.logger.info(
            f"Done executing queries, please note that setting "
            f"commit=False will not save any changes to the DB"
        )


class SymbenchAthensGraphDBClient(GraphDBDriver):
    """Utility class for cloning/clearing designs in the Graph Database."""

    def _clone(self, src_name, dst_name):
        clone_query = CLONE_QUERY.format(**{"src_name": src_name, "dst_name": dst_name})

        self.run_queries(clone_query.split("\n"), commit=True)

    def _clear(self, name):
        pass

    def get_all_design_names(self):
        results = self.client.submit(
            "g.V().has('VertexLabel', '[avm]Design').values('[]Name').toList()"
        )
        future_results = results.all()
        designs = future_results.result()
        return set(designs)

    def clone_design(self, design):
        """Clone a design in the graph database."""
        all_designs = self.get_all_design_names()
        i = 0
        assert design.name in all_designs, "Cannot clone a non existent design"
        clone_name = design.name + f"Clone{i + 1}"

        while clone_name in all_designs:
            clone_name = design.name + f"{i + 1}"
            i += 1

        self.logger.info(f"About to clone design {design.name} to {clone_name}")
        self._clone(design.name, clone_name)
        design.name = clone_name
        self.logger.info(f"Successfully cloned the design as {design.name}")
