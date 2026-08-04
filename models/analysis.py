from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class InitialElementAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str | None = None
    existed_initially: bool


class CurrentElementAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str | None = None


class InitialPromptElementsAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: InitialElementAnalysis
    context: InitialElementAnalysis
    goal: InitialElementAnalysis
    constraints: InitialElementAnalysis
    output: InitialElementAnalysis
    examples: InitialElementAnalysis
    reasoning: InitialElementAnalysis
    evaluation: InitialElementAnalysis


class CurrentPromptElementsAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: CurrentElementAnalysis
    context: CurrentElementAnalysis
    goal: CurrentElementAnalysis
    constraints: CurrentElementAnalysis
    output: CurrentElementAnalysis
    examples: CurrentElementAnalysis
    reasoning: CurrentElementAnalysis
    evaluation: CurrentElementAnalysis


class InitialAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain: str | None = None
    prompt_elements: InitialPromptElementsAnalysis


class CurrentAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain: str | None = None
    prompt_elements: CurrentPromptElementsAnalysis
