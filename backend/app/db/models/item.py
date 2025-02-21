from .database import BaseDatabase
from sqlalchemy import Column, String, Text


class Item(BaseDatabase):
    """
    アイテムモデル。アイテムの情報を保持します。

    Attributes
    ----------
    id : UUID
        アイテムの一意な識別子（BaseDatabaseから継承）
    name : str
        アイテムの名前
    description : str
        アイテムの説明
    created_at : datetime
        作成日時（BaseDatabaseから継承）
    updated_at : datetime
        更新日時（BaseDatabaseから継承）
    """
    __tablename__ = "items"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
