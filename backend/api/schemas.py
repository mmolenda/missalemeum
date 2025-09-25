from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Info(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = Field(
        default=None,
        description=(
            "ID of the resource. Depending on the context it can be either a slugified "
            "title (supplements, prayers, etc.) or a date in format YYYY-MM-DD."
        ),
    )
    title: str = Field(
        ..., description="Human readable title of the resource."
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="List of additional informations such as liturgical color or season.",
    )


class Section(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = Field(
        default=None,
        description="Identifier of the section. Unique within a single resource.",
    )
    label: Optional[str] = Field(
        default=None,
        description="Name of the section in vernacular language.",
    )
    body: List[List[str]] = Field(
        default_factory=list,
        description=(
            "Section content. Each item contains one or two strings representing a rubric "
            "or vernacular/Latin pair formatted using DivinumOfficium markup."
        ),
    )


class ContentItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    info: Info = Field(
        ..., description="Metadata describing the resource."
    )
    sections: List[Section] = Field(
        default_factory=list,
        description="Ordered list of sections comprising the resource."
    )
