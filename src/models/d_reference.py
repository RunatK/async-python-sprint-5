from enum import Enum

VisibilityType = Enum(
    value='VisibilityType',
    names=('private', 'public')
)

class DReference:
    def __init__(self, _id: int, short_id: str, short_url: str, original_url: str, visibility: VisibilityType, user_id: int) -> None:
        self.id = _id
        self.short_id: str = short_id
        self.short_url: str = short_url
        self.original_url: str = original_url
        self.visibility: VisibilityType = visibility
        self.user_id: int = user_id