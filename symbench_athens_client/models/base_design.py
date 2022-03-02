from typing import ClassVar, Dict, List, Tuple, Union

from pydantic import BaseModel, Field, validator

from symbench_athens_client.utils import dict_to_design_vars


class SeedDesign(BaseModel):

    __design_vars__: ClassVar[str] = {
        "q_position",
        "q_velocity",
        "q_angular_velocity",
        "q_angles",
        "r",
    }

    name: str = Field(
        "", alias="name", description="Name of the seed design in the graph database"
    )

    swap_list: Dict[str, List[str]] = Field(
        {}, description="list of swap components for this design", alias="swap_list"
    )

    q_position: Union[float, Tuple[float, float]] = Field(
        default=1.0, alias="Q_Position", description="The Q-Position"
    )

    q_velocity: Union[float, Tuple[float, float]] = Field(
        default=1.0, description="The Q-Velocity", alias="Q_Velocity"
    )

    q_angular_velocity: Union[float, Tuple[float, float]] = Field(
        default=1.0, description="The Q-Angular Velocity", alias="Q_Angular_Velocity"
    )

    q_angles: Union[float, Tuple[float, float]] = Field(
        1.0, description="The Q-Angles", alias="Q_Angles"
    )

    r: Union[float, Tuple[float, float]] = Field(
        1.0, description="The R-Parameter", alias="R"
    )

    def to_jenkins_parameters(self):
        design_vars = self.dict(by_alias=True, include=self.__design_vars__)
        return {"DesignVars": dict_to_design_vars(design_vars, repeat_values=True)}

    def parameters(self):
        return self.dict(by_alias=True, include=self.__design_vars__)

    def components(self, by_alias=True):
        all_components = self.dict(
            by_alias=by_alias, exclude={"name", "swap_list"}.union(self.__design_vars__)
        )
        names = {}

        for component in all_components:
            names[component] = (
                all_components[component]["Name"]
                if by_alias
                else all_components[component]["name"]
            )

        return names

    def reset_name(self):
        self.name = self.__class__.__name__

    def clear_swap(self, component_instance_name=None):
        if component_instance_name is None:
            self.swap_list = {}
        else:
            del self.swap_list[component_instance_name]

    def needs_swap(self):
        return len(self.swap_list) > 0

    def iter_components(self, by_alias=True):
        for field_key, v in self.__dict__.items():
            if field_key not in self.__design_vars__ and field_key != "name":
                name = field_key
                if by_alias:
                    name = self.__fields__[field_key].alias
                yield name, v

    def __setattr__(self, key, value):
        if key not in self.__design_vars__ and (key != "name" and key != "swap_list"):
            if getattr(self, key) != value:
                field_info_for_key = self.__fields__[key]
                if not self.swap_list.get(field_info_for_key.alias):
                    self.swap_list[field_info_for_key.alias] = [getattr(self, key).name]
                self.swap_list[field_info_for_key.alias].append(value.name)

        super().__setattr__(key, value)

    @validator("name", pre=True, always=True)
    def validate_name(cls, name):
        if name is None or name == "":
            name = cls.__name__
        return name

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
