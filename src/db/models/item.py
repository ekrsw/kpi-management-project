from .database import BaseDatabase
from sqlalchemy import Column, Integer, String


class Item(BaseDatabase):
    """
    アイテムモデル。アイテムの情報を保持します。

    Attributes
    ----------
    id : sqlalchemy.Column
        アイテムの一意な識別子。プライマリキーであり、インデックスが作成されています。
    name : sqlalchemy.Column
        アイテムの名前。インデックスが作成されており、必須項目です。
    """
    __tablename__ = "items"

    name = Column(String, index=True, nullable=False)
