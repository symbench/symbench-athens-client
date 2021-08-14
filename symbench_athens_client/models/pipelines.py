from pydantic import BaseModel, Field


class JenkinsPipeline(BaseModel):
    @property
    def pipeline_name(self):
        return self.__class__.__name__

    def to_jenkins_parameters(self):
        return self.parameters()

    def parameters(self):
        return self.dict(by_alias=True)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        validate_assignment = True


class CloneDesign(JenkinsPipeline):
    """Clone a design in the graphdb."""

    from_design_name: str = Field(
        "UUV_PARAMETRIC_CYLINDER_DISCRETE",
        description="From Design name",
        alias="FromDesignName",
    )

    to_design_name: str = Field(
        "CLONE123", description="To Design name", alias="ToDesignName"
    )


class ClearDesign(JenkinsPipeline):
    """Remove a design from the graph database."""

    design_name: str = Field(
        "BLANK", description="The design name to clear", alias="DesignName"
    )


class CopyComponent(JenkinsPipeline):
    """Copy a component from a design to another design."""

    from_design_name: str = Field(
        "AllComponents",
        description="Name of existing design in the database",
        alias="FromDesignName",
    )

    from_component_name: str = Field(
        "fin_c",
        description="Name of the ComponentInstance in the Source Design",
        alias="FromComponentName",
    )

    to_design_name: str = Field(
        "BLANK",
        description="Name of the connectorInstance on FromComponentInstance",
        alias="ToDesignName",
    )

    to_component_name: str = Field("fin_x", description="", alias="ToComponentName")


class SwapComponent(JenkinsPipeline):
    """Swap components in the design"""

    design: str = Field(
        "UUV_PARAMETRIC_CYLINDER_DISCRETE",
        description="Name of existing design in the database",
        alias="Design",
    )

    ci_name: str = Field(
        "Battery_V2", description="Name of the component Instance", alias="CIName"
    )

    from_comp_name: str = Field(
        "Battery_LiFeP04",
        description="Name of the Original Component",
        alias="fromCompName",
    )

    to_comp_name: str = Field(
        "NBP60AH_Battery_LiFeP04",
        description="Name of the new component",
        alias="toCompName",
    )


class AddConnection(JenkinsPipeline):
    """Add a connection between two components of a design."""

    from_design_name: str = Field(
        "Blank",
        description="Name of existing design in the database",
        alias="FromDesignName",
    )

    from_component_name: str = Field(
        "fin_x",
        description="Name of the ComponentInstance in the Source Design",
        alias="FromComponentName",
    )

    from_connector_name: str = Field(
        "UUVFin",
        description="Name of the connectorInstance on From ComponentInstance",
        alias="FromConnectorName",
    )

    to_component_name: str = Field(
        "ActuatorMount",
        description="Destination component name",
        alias="ToComponentName",
    )

    to_connector_name: str = Field(
        "UUVFin0", description="Destination connector name", alias="ToConnectorName"
    )


class clearComponents(ClearDesign):
    """clear components from a design."""
