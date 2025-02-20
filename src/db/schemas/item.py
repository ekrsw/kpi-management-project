from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class ItemBase(BaseModel):
    """
    アイテムの基本モデル（共通項目を定義）

    Attributes
    ----------
    name : str
        アイテムの名前
    description : Optional[str]
        アイテムの説明
    """
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v.strip()

    model_config = ConfigDict(from_attributes=True)


class ItemCreate(ItemBase):
    """
    アイテム作成時のモデル
    """
    pass


class ItemUpdate(BaseModel):
    """
    アイテム更新時のモデル（全てのフィールドがオプショナル）
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None

    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name must not be empty')
        return v.strip() if v else v

    model_config = ConfigDict(from_attributes=True)


class Item(ItemBase):
    """
    アイテム取得時のモデル（IDやタイムスタンプを含む）

    Attributes
    ----------
    id : UUID
        アイテムの一意のID
    created_at : datetime
        作成日時
    updated_at : datetime
        更新日時
    """
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
