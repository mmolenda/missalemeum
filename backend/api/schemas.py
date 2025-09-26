from typing import List, Optional

from pydantic import BaseModel, Field


class Info(BaseModel):
    """Shared metadata block used by multiple endpoints."""
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
        description="List of additional informations such as liturgical color, station church, or season.",
    )


class Section(BaseModel):
    """Represents a single section within propers or supplements."""
    id: Optional[str] = Field(
        default=None,
        description="Identifier of the section. Unique within the scope of one resource.",
    )
    label: Optional[str] = Field(
        default=None,
        description="Name of the section in vernacular language.",
    )
    body: List[List[str]] = Field(
        default_factory=list,
        description=(
            "Section content. Each item contains one or two strings representing a rubric or "
            "vernacular/Latin pair formatted using DivinumOfficium markup."
        ),
    )


class SupplementLink(BaseModel):
    """Reference to an additional resource related to a proper."""
    path: Optional[str] = Field(
        default=None,
        description="Either path to a resource inside the app or an external URL",
    )
    label: Optional[str] = Field(
        default=None,
        description="Human readable label for the supplement link.",
    )


class ProperInfo(Info):
    """Information block returned alongside a proper."""

    colors: Optional[List[str]] = Field(
        default=None,
        description="Feast colours. For example g - green, r - red.",
    )
    date: Optional[str] = Field(
        default=None,
        description="Date of the observance when fetched by date (YYYY-MM-DD).",
    )
    description: Optional[str] = Field(
        default=None,
        description="Narrative description of the observance.",
    )
    rank: Optional[int] = Field(
        default=None,
        description="Feast rank (class).",
    )
    supplements: Optional[List[SupplementLink]] = Field(
        default=None,
        description="List of additional resources related to the proper.",
    )
    tempora: Optional[str] = Field(
        default=None,
        description="Textual description of the current liturgical season.",
    )
    commemorations: Optional[List[str]] = Field(
        default=None,
        description="Commemorations falling on the given day.",
    )


class ContentItem(BaseModel):
    """Structured content resource (supplement/ordo)."""
    info: Info = Field(
        ..., description="Metadata describing the resource."
    )
    sections: List[Section] = Field(
        default_factory=list,
        description="Ordered list of sections comprising the resource."
    )


class Proper(BaseModel):
    """Proper returned by the API."""
    info: ProperInfo = Field(
        ..., description="Metadata describing the proper."
    )
    sections: List[Section] = Field(
        default_factory=list,
        description="Ordered list of sections making up the proper."
    )


class CalendarItem(BaseModel):
    """Entry in the liturgical calendar."""
    title: str = Field(
        ..., description="Title of the observance."
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Additional information such as station church or season.",
    )
    colors: List[str] = Field(
        default_factory=list,
        description="Feast colours (b - black, g - green, r - red, v - violet, w - white, p - pink).",
    )
    rank: int = Field(
        ..., description="Feast rank (class)."
    )
    id: str = Field(
        ..., description="ID of the observance (YYYY-MM-DD)."
    )
    commemorations: List[str] = Field(
        default_factory=list,
        description="Commemorations falling on the given day.",
    )


class VersionInfo(BaseModel):
    """API version response."""

    version: str = Field(
        ...,
        description="Semantic version of the running API.",
        json_schema_extra={"example": "v5.0.1"},
    )
