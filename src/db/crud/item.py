from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemUpdate


def get_item(db: Session, item_id: UUID) -> Optional[Item]:
    """
    指定されたIDのアイテムを取得します。

    Parameters
    ----------
    db : Session
        データベースセッション
    item_id : UUID
        取得するアイテムのID

    Returns
    -------
    Optional[Item]
        アイテムが見つかった場合はアイテムオブジェクト、見つからなかった場合はNone
    """
    return db.get(Item, item_id)


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """
    アイテムの一覧を取得します。

    Parameters
    ----------
    db : Session
        データベースセッション
    skip : int, optional
        スキップする件数, by default 0
    limit : int, optional
        取得する最大件数, by default 100

    Returns
    -------
    List[Item]
        アイテムオブジェクトのリスト
    """
    return list(db.execute(select(Item).offset(skip).limit(limit)).scalars())


def create_item(db: Session, item: ItemCreate) -> Item:
    """
    新しいアイテムを作成します。

    Parameters
    ----------
    db : Session
        データベースセッション
    item : ItemCreate
        作成するアイテムの情報

    Returns
    -------
    Item
        作成されたアイテムオブジェクト
    """
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: UUID, item: ItemUpdate) -> Optional[Item]:
    """
    指定されたIDのアイテムを更新します。

    Parameters
    ----------
    db : Session
        データベースセッション
    item_id : UUID
        更新するアイテムのID
    item : ItemUpdate
        更新する情報

    Returns
    -------
    Optional[Item]
        更新されたアイテムオブジェクト、アイテムが見つからなかった場合はNone
    """
    update_data = item.model_dump(exclude_unset=True)
    if not update_data:
        return get_item(db, item_id)

    result = db.execute(
        update(Item)
        .where(Item.id == item_id)
        .values(**update_data)
        .returning(Item)
    )
    db.commit()
    
    updated_item = result.scalar_one_or_none()
    return updated_item


def delete_item(db: Session, item_id: UUID) -> bool:
    """
    指定されたIDのアイテムを削除します。

    Parameters
    ----------
    db : Session
        データベースセッション
    item_id : UUID
        削除するアイテムのID

    Returns
    -------
    bool
        削除に成功した場合はTrue、アイテムが見つからなかった場合はFalse
    """
    result = db.execute(delete(Item).where(Item.id == item_id))
    db.commit()
    return result.rowcount > 0
