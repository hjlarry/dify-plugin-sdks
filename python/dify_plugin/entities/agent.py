from typing import Optional
from pydantic import BaseModel, Field, field_validator

from dify_plugin.core.utils.yaml_loader import load_yaml_file
from dify_plugin.entities import I18nObject
from dify_plugin.entities.tool import (
    ToolIdentity,
    ToolInvokeMessage,
    ToolOutputSchema,
    ToolParameter,
    ToolProviderIdentity,
)


class AgentProviderIdentity(ToolProviderIdentity):
    pass


class AgentIdentity(ToolIdentity):
    pass


class AgentParameter(ToolParameter):
    pass


class AgentOutputSchema(ToolOutputSchema):
    pass


class AgentStrategyConfigurationExtra(BaseModel):
    class Python(BaseModel):
        source: str

    python: Python


class AgentStrategyConfiguration(BaseModel):
    identity: AgentIdentity
    parameters: list[AgentParameter] = Field(default=[], description="The parameters of the agent")
    description: I18nObject
    extra: AgentStrategyConfigurationExtra
    has_runtime_parameters: bool = Field(default=False, description="Whether the tool has runtime parameters")
    output_schema: Optional[AgentOutputSchema] = None


class AgentProviderConfigurationExtra(BaseModel):
    class Python(BaseModel):
        source: str

    python: Python


class AgentProviderConfiguration(BaseModel):
    class Python(BaseModel):
        source: str

    identity: AgentProviderIdentity
    strategies: list[AgentStrategyConfiguration] = Field(default=[], description="The strategies of the agent provider")
    extra: AgentProviderConfigurationExtra

    @field_validator("strategies", mode="before")
    @classmethod
    def validate_strategies(cls, value) -> list[AgentStrategyConfiguration]:
        if not isinstance(value, list):
            raise ValueError("strategies should be a list")

        strategies: list[AgentStrategyConfiguration] = []

        for strategy in value:
            # read from yaml
            if not isinstance(strategy, str):
                raise ValueError("strategy path should be a string")
            try:
                file = load_yaml_file(strategy)
                strategies.append(
                    AgentStrategyConfiguration(
                        **{
                            "identity": AgentIdentity(**file["identity"]),
                            "parameters": [AgentParameter(**param) for param in file.get("parameters", []) or []],
                            "description": I18nObject(**file["description"]),
                            "extra": AgentStrategyConfigurationExtra(**file.get("extra", {})),
                        }
                    )
                )
            except Exception as e:
                raise ValueError(f"Error loading agent strategy configuration: {str(e)}") from e

        return strategies


class AgentInvokeMessage(ToolInvokeMessage):
    pass