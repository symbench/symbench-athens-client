import logging

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __

from symbench_athens_client.utils import get_logger


class GraphDBDriver:
    def __init__(self, gremlin_url="ws://localhost:8182/gremlin", log_level=None):
        self.gremlin_url = gremlin_url
        self.logger = get_logger(
            self.__class__.__name__, level=log_level or logging.DEBUG
        )
        self._connect()

    def _connect(self):
        self.connection = DriverRemoteConnection(self.gremlin_url, "g")
        self.g = traversal().withRemote(self.connection)
        self.logger.info(f"Connected to gremlin server at {self.gremlin_url}")
        self.is_connected = True

    def reconnect(self):
        if self.is_connected:
            self.dispose()
        self._connect()

    def dispose(self):
        self.connection.close()
        self.connection = None
        self.g = None
        self.is_connected = False
        self.logger.info("Closed connection to the gremlin server")


class UAMGraphOperator(GraphDBDriver):
    """Utility class for cloning/clearing designs in the Graph Database."""

    def clone(self, src_name, dst_name):
        if not self.is_connected:
            self._connect()

        self.g.V().has("VertexLabel", "[avm]Design").has("[]Name", src_name).as_(
            "tmp"
        ).property("_duptag_", "_SRC_").select("tmp").repeat(
            __.in_("inside").as_("tmp").property("_duptag_", "_SRC_").select("tmp")
        ).times(
            20
        )

        self.g.V().has("_duptag_", "_SRC_").as_("x").select("x").addV(
            __.select("x").label()
        ).as_("y").property("_duptag_", "_DUP_").addE("clone").from_("x").to(
            "y"
        ).iterate()

        self.g.V().has("_duptag_", "_SRC_").as_("x").out("clone").where(
            __.has("_duptag_", "_DUP_")
        ).as_("y").select("x").properties().as_("xps").select("y").property(
            __.select("xps").key(), __.select("xps").value()
        ).select(
            "y"
        ).property(
            "_duptag_", "_DUP_"
        ).iterate()

        self.g.V().has("_duptag_", "_SRC_").as_("orig").out("clone").where(
            __.has("_duptag_", "_DUP_")
        ).as_("cloned").select("orig").inE().where(__.label().is_(__.neq("clone"))).as_(
            "elabel"
        ).select(
            "elabel"
        ).outV().out(
            "clone"
        ).where(
            __.has("_duptag_", "_DUP_")
        ).as_(
            "inTarg"
        ).select(
            "cloned"
        ).addE(
            __.select("elabel").label()
        ).from_(
            "inTarg"
        ).to(
            "cloned"
        ).iterate()

        self.g.V().has("_duptag_", "_SRC_").as_("orig").out("clone").where(
            __.has("_duptag_", "_DUP_")
        ).as_("cloned").select("orig").out("component_id").as_("linkDest").addE(
            "component_id"
        ).from_(
            "cloned"
        ).to(
            "linkDest"
        ).iterate()

        self.g.V().has("_duptag_", "_SRC_").as_("orig").out("clone").where(
            __.has("_duptag_", "_DUP_")
        ).as_("cloned").select("orig").out("id_in_component_model").as_(
            "linkDest"
        ).addE(
            "id_in_component_model"
        ).from_(
            "cloned"
        ).to(
            "linkDest"
        ).iterate()

        self.g.V().has("[]Name", "__SOURCENAME__").has("_duptag_", "_DUP_").property(
            "[]Name", dst_name
        )

        self.g.V().has("_duptag_", "_SRC_").outE("clone").drop().iterate()
        self.g.V().has("_duptag_", "_SRC_").property("_duptag_", "_cpysrc_")
        self.g.V().has("_duptag_", "_DUP_").property("_duptag_", "_cpydst_")
