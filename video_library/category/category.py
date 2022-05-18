from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from __seedwork.entities import GenericEntity


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(GenericEntity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(default_factory=lambda: datetime.now())
