from datetime import datetime


class DFile:
    def __init__(
        self,
        _id: int, 
        name: str, 
        path: str, 
        size: str, 
        is_downloadable: bool, 
        created_ad: datetime,
        user_id: int
        ) -> None:
        self.id = _id
        self.name = name
        self.path = path
        self.size = size
        self.is_downloadable = is_downloadable
        self.created_ad = created_ad
        self.user_id = user_id

    def __str__(self) -> str:
        return f"{self.path}/{self.name}"