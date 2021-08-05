from enum import IntEnum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator

from symbench_athens_client.models.designs import SeedDesign


class Pipeline(BaseModel):
    name: str = Field(name="JenkinsPipeline")

    description: str = Field("", description="The description of the pipeline")

    parameters: Dict[str, str] = Field(
        ..., description="The parameters for the pipeline"
    )

    requires_extra_params: bool = Field(
        False,
        description="A flag mentioning if it requires extra design parameters to run",
    )

    class Config:
        validate_assignment = True
        aribtrary_types_allowed = True
        allow_mutation = False


class UAVWorkflowPipeline(Pipeline):
    @validator("parameters", pre=True, always=True)
    def validate_parameters(cls, params):
        # ToDo: Once specific rules are specified for parameters
        return params


class JOB_STATUS(IntEnum):
    NOT_STARTED = 0
    STARTED = 1
    RUNNING = 2
    SUCCESS = 3
    FAILED = 4


class Job(BaseModel):
    build_number: Optional[int] = Field(
        None, description="The jenkins build id for this job"
    )

    pipeline: Pipeline = Field(..., description="The pipeline for this job")

    status: int = Field(JOB_STATUS.NOT_STARTED, description="The status for this job")

    output: str = Field("", description="The standard output for this job")

    executor: Optional[Any] = Field(
        None, description="The executor information for this job"
    )

    design: SeedDesign = Field(..., description="The seed design to run this job on")

    parameters: Dict[str, Any] = Field(
        {}, description="The build parameters for this job insance"
    )

    def to_jenkins_parameters(self):
        params = (
            self.design.to_jenkins_parameters()
            if self.pipeline.requires_extra_params
            else {}
        )
        params.update(self.parameters)
        return params

    def set_parameters(self, params):
        self.parameters = params

    @property
    def name(self):
        return self.pipeline.name

    @validator("parameters", pre=True, always=True)
    def validate_parameters(cls, parameters, values):
        for key in parameters:
            assert key in values["pipeline"].parameters
        return parameters

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True


#################### Existing Pipelines in the Jenkins Server ##########################
AddConnection = Pipeline(
    name="AddConnection",
    description="Add Connections between components",
    parameters={
        "FromDesignName": "Name of existing design in the database",
        "FromComponentName": "Name of the ComponentInstance in the Design",
        "FromConnectorName": "Name of the connectorInstance on FromComponentInstance",
        "ToComponentName": "Name of the ComponentInstance in the Design",  # Inferred
        "ToConnectorName": "Name of the connectorInstance in the Design on ToComponentInstance",  # Inferred
    },
    requires_extra_params=False,
)

ClearDesign = Pipeline(
    name="ClearDesign",
    description="Clear a design of all component instances",
    parameters={"DesignName": "Name of existing design in the database"},
    requires_extra_params=False,
)

CloneDesign = Pipeline(
    name="CloneDesign",
    description="Clone a design in the database",
    parameters={
        "FromDesignName": "Name of existing design in the database",
        "ToDesignName": "Name of the new design",
    },
    requires_extra_params=False,
)

CopyComponent = Pipeline(
    name="CopyComponent",
    description="Copy Component Instance into a design. Typically, copy a component instance from AllComponents to a target design",
    parameters={
        "FromDesignName": "Name of the existing design in the database",
        "FromComponentName": "Name of the ComponentInstance in the Source Design",
        "ToDesignName": "Name of the connectorInstance on FromComponentInstance",  # FixMe: What does this mean?
        "ToComponentName": "Name of the ComponentInstance in the Target Design",
    },
    requires_extra_params=False,
)

clearComponents = Pipeline(
    name="clearComponents",
    description="Clear a design of all component instances",
    parameters={"DesignName": "Name of existing design in the database"},
    requires_extra_params=False,
)
#################### Existing Pipelines in the Jenkins Server ##########################
