from pydantic import BaseModel, ConfigDict, constr, Field, field_validator
from datetime import datetime
from typing import Optional


class ItemBase(BaseModel):
    """
    アイテムの基本モデル（共通項目を定義）

    Attributes
    ----------
    name : str
        アイテムの名前。
    """
    
    name: str # カスタムバリデーションで検証
    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v

    class Config:
        from_attributes = True
        model_config = ConfigDict()

class ItemCreate(ItemBase):
    """
    アイテム作成時のモデル（追加のプロパティはなし）

    このクラスは `ItemBase` を継承しており、アイテム作成時に必要な基本項目を提供します。
    特別な追加項目はありません。
    """
    pass  # ItemBaseを継承し、特別な追加項目はない


class Item(ItemBase):
    """
    アイテム取得時のモデル（IDやタイムスタンプを含む）

    Attributes
    ----------
    id : int
        アイテムの一意のID。
    created_at : datetime
        アイテムが作成された日時。
    updated_at : datetime
        アイテムが最後に更新された日時。
    """
    id: int  # アイテムの一意のID
    created_at: datetime  # 作成日時
    updated_at: datetime  # 更新日時

    class Config:
        from_attributes = True  # ORM モードを有効にして属性から値を取得できるようにする
        model_config = ConfigDict()