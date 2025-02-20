from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from .src.db.models import item as item_model
from .src.db.schemas import item as item_schema
from typing import Optional, List


# アイテムIDで特定のアイテムを取得する関数
async def get_item(db: AsyncSession, item_id: int) -> Optional[item_model.Item]:
    """
    アイテムIDで特定のアイテムを取得します。

    Parameters
    ----------
    db : AsyncSession
        データベースセッション。
    item_id : int
        取得するアイテムのID。

    Returns
    -------
    Optional[models.Item]
        見つかった場合はアイテムオブジェクト、存在しない場合はNone。
    """
    result = await db.execute(select(item_model.Item).filter(item_model.Item.id == item_id))
    return result.scalars().first()

# 複数のアイテムを取得する関数
async def get_items(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[item_model.Item]:
    """
    アイテムのリストを取得します（ページング可能）。

    Parameters
    ----------
    db : AsyncSession
        データベースセッション。
    skip : int, optional
        取得をスキップするレコード数（デフォルトは0）。
    limit : int, optional
        取得する最大レコード数（デフォルトは10）。

    Returns
    -------
    List[models.Item]
        アイテムオブジェクトのリスト。
    """
    result = await db.execute(select(item_model.Item).offset(skip).limit(limit))
    return result.scalars().all()

# 新しいアイテムを作成する関数
async def create_item(db: AsyncSession, item: item_schema.ItemCreate) -> item_model.Item:
    """
    新しいアイテムを作成します。

    Parameters
    ----------
    db : AsyncSession
        データベースセッション。
    item : schemas.ItemCreate
        新規アイテムの情報を含むスキーマ。

    Returns
    -------
    models.Item
        作成された新しいアイテムオブジェクト。
    """
    db_item = item_model.Item(name=item.name)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

# アイテムを更新する関数
async def update_item(db: AsyncSession, item_id: int, item: item_schema.ItemCreate) -> Optional[item_model.Item]:
    """
    アイテムIDでアイテムを更新します。

    Parameters
    ----------
    db : AsyncSession
        データベースセッション。
    item_id : int
        更新するアイテムのID。
    item : schemas.ItemCreate
        更新するアイテム情報を含むスキーマ。

    Returns
    -------
    Optional[models.Item]
        更新されたアイテムオブジェクト。アイテムが存在しない場合はNone。
    """
    result = await db.execute(select(item_model.Item).filter(item_model.Item.id == item_id))
    db_item = result.scalars().first()
    if db_item is None:
        return None
    db_item.name = item.name
    await db.commit()
    await db.refresh(db_item)
    return db_item

# アイテムを削除する関数
async def delete_item(db: AsyncSession, item_id: int) -> Optional[item_model.Item]:
    """
    アイテムIDでアイテムを削除します。

    Parameters
    ----------
    db : AsyncSession
        データベースセッション。
    item_id : int
        削除するアイテムのID。

    Returns
    -------
    Optional[models.Item]
        削除されたアイテムオブジェクト。アイテムが存在しない場合はNone。
    """
    result = await db.execute(select(item_model.Item).filter(item_model.Item.id == item_id))
    db_item = result.scalars().first()
    if db_item is None:
        return None
    await db.delete(db_item)
    await db.commit()
    return db_item