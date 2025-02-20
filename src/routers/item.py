from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.dependencies import get_db
from ..db.crud import item as crud
from ..db.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter(
    prefix="/api/items",
    tags=["Items"]
)


@router.get("", response_model=List[Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    アイテムの一覧を取得します。

    Parameters
    ----------
    skip : int, optional
        スキップする件数, by default 0
    limit : int, optional
        取得する最大件数, by default 100
    db : Session
        データベースセッション

    Returns
    -------
    List[Item]
        アイテムオブジェクトのリスト
    """
    return crud.get_items(db, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=Item)
def read_item(item_id: UUID, db: Session = Depends(get_db)):
    """
    指定されたIDのアイテムを取得します。

    Parameters
    ----------
    item_id : UUID
        取得するアイテムのID
    db : Session
        データベースセッション

    Returns
    -------
    Item
        アイテムオブジェクト

    Raises
    ------
    HTTPException
        アイテムが見つからない場合は404エラー
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.post("", response_model=Item, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    新しいアイテムを作成します。

    Parameters
    ----------
    item : ItemCreate
        作成するアイテムの情報
    db : Session
        データベースセッション

    Returns
    -------
    Item
        作成されたアイテムオブジェクト
    """
    return crud.create_item(db=db, item=item)


@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: UUID,
    item: ItemUpdate,
    db: Session = Depends(get_db)
):
    """
    指定されたIDのアイテムを更新します。

    Parameters
    ----------
    item_id : UUID
        更新するアイテムのID
    item : ItemUpdate
        更新する情報
    db : Session
        データベースセッション

    Returns
    -------
    Item
        更新されたアイテムオブジェクト

    Raises
    ------
    HTTPException
        アイテムが見つからない場合は404エラー
    """
    db_item = crud.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: UUID, db: Session = Depends(get_db)):
    """
    指定されたIDのアイテムを削除します。

    Parameters
    ----------
    item_id : UUID
        削除するアイテムのID
    db : Session
        データベースセッション

    Raises
    ------
    HTTPException
        アイテムが見つからない場合は404エラー
    """
    if not crud.delete_item(db=db, item_id=item_id):
        raise HTTPException(status_code=404, detail="Item not found")
