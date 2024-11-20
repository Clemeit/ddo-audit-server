from datetime import datetime
from enum import Enum
from typing import Optional

from models.character import Character
from models.base_model import ConfiguredBaseModel as BaseModel


class QuestLevel(BaseModel):
    heroic_normal: Optional[int] = None
    heroic_hard: Optional[int] = None
    heroic_elite: Optional[int] = None
    epic_normal: Optional[int] = None
    epic_hard: Optional[int] = None
    epic_elite: Optional[int] = None


class QuestXP(BaseModel):
    heroic_normal: Optional[int] = None
    heroic_hard: Optional[int] = None
    heroic_elite: Optional[int] = None
    epic_normal: Optional[int] = None
    epic_hard: Optional[int] = None
    epic_elite: Optional[int] = None


class Quest(BaseModel):
    id: str
    alt_id: Optional[str] = None
    area_id: Optional[str] = None
    name: Optional[str] = None
    level: Optional[QuestLevel] = None
    xp: Optional[QuestXP] = None
    is_free_to_play: Optional[bool] = None
    is_free_to_vip: Optional[bool] = None
    required_adventure_pack: Optional[str] = None
    adventure_area: Optional[str] = None
    quest_journal_group: Optional[str] = None
    group_size: Optional[str] = None
    patron: Optional[str] = None
    average_time: Optional[float] = None
    tip: Optional[str] = None


class LfmActivityEvent(BaseModel):
    tag: Optional[str] = None
    data: Optional[str] = None


class LfmActivity(BaseModel):
    timestamp: Optional[datetime] = None
    events: Optional[list[LfmActivityEvent]] = None


class Lfm(BaseModel):
    id: str
    comment: Optional[str] = None
    quest: Optional[Quest] = None
    is_quest_guess: Optional[bool] = None
    difficulty: Optional[str] = None
    accepted_classes: Optional[list[str]] = None
    accepted_classes_count: Optional[int] = None
    minimum_level: Optional[int] = None
    maximum_level: Optional[int] = None
    adventure_active_time: Optional[int] = None
    leader: Optional[Character] = None
    members: Optional[list[Character]] = None
    activity: Optional[list[LfmActivity]] = None
    server_name: Optional[str] = None


class LfmActivityType(str, Enum):
    posted = "posted"
    comment = "comment"
    quest = "quest"
    member_joined = "member_joined"
    member_left = "member_left"
