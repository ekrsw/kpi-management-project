from datetime import datetime
from uuid import UUID
import uuid

import pytest
from sqlalchemy import create_engine, Column, func, DateTime
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as pgUUID

from app.db.schemas.item import ItemCreate, ItemUpdate

# SQLite用のUUID型
class UUID_SQLite(TypeDecorator):
    """SQLite互換のUUID型"""
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(pgUUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, UUID):
                return value.hex
            return value.replace('-', '').lower()

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, UUID):
            value = UUID(value)
        return value

# テスト用のベースモデル
Base = declarative_base()

# テスト用のItemモデル
class Item(Base):
    __tablename__ = "items"
    
    id = Column(UUID_SQLite(), primary_key=True, default=uuid.uuid4)
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


@pytest.fixture
def db_session():
    """テスト用のデータベースセッションを提供するフィクスチャ"""
    # インメモリSQLiteデータベースを使用
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # テーブルの作成
    Base.metadata.create_all(engine)
    
    # セッションの作成
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # テーブルの削除
        Base.metadata.drop_all(engine)


@pytest.fixture
def sample_item(db_session: Session) -> Item:
    """テスト用のサンプルアイテムを作成するフィクスチャ"""
    item_data = ItemCreate(name="Test Item", description="Test Description")
    return create_item(db_session, item_data)


def create_item(db: Session, item: ItemCreate) -> Item:
    """
    新しいアイテムを作成します。
    """
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: UUID) -> Item:
    """
    指定されたIDのアイテムを取得します。
    """
    return db.get(Item, item_id)


def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    """
    アイテムの一覧を取得します。
    """
    return list(db.query(Item).offset(skip).limit(limit).all())


def update_item(db: Session, item_id: UUID, item: ItemUpdate) -> Item | None:
    """
    指定されたIDのアイテムを更新します。
    """
    update_data = item.model_dump(exclude_unset=True)
    if not update_data:
        return get_item(db, item_id)

    db_item = get_item(db, item_id)
    if not db_item:
        return None

    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: UUID) -> bool:
    """
    指定されたIDのアイテムを削除します。
    """
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True


def test_create_item(db_session: Session):
    """アイテム作成のテスト"""
    item_data = ItemCreate(name="New Item", description="New Description")
    item = create_item(db_session, item_data)
    
    assert item.name == "New Item"
    assert item.description == "New Description"
    assert isinstance(item.id, UUID)
    assert isinstance(item.created_at, datetime)
    assert isinstance(item.updated_at, datetime)


def test_create_item_without_description(db_session: Session):
    """説明なしでアイテムを作成するテスト"""
    item_data = ItemCreate(name="No Description Item")
    item = create_item(db_session, item_data)
    
    assert item.name == "No Description Item"
    assert item.description is None


def test_get_item(db_session: Session, sample_item: Item):
    """アイテム取得のテスト"""
    retrieved_item = get_item(db_session, sample_item.id)
    
    assert retrieved_item is not None
    assert retrieved_item.id == sample_item.id
    assert retrieved_item.name == sample_item.name
    assert retrieved_item.description == sample_item.description


def test_get_item_not_found(db_session: Session):
    """存在しないアイテムの取得テスト"""
    non_existent_id = UUID('12345678-1234-5678-1234-567812345678')
    retrieved_item = get_item(db_session, non_existent_id)
    
    assert retrieved_item is None


def test_get_items(db_session: Session):
    """アイテム一覧取得のテスト"""
    # 複数のテストアイテムを作成
    items_data = [
        ItemCreate(name=f"Item {i}", description=f"Description {i}")
        for i in range(3)
    ]
    for item_data in items_data:
        create_item(db_session, item_data)
    
    # アイテム一覧を取得
    items = get_items(db_session)
    
    assert len(items) == 3
    assert all(isinstance(item.id, UUID) for item in items)
    assert all(item.name.startswith("Item ") for item in items)


def test_get_items_pagination(db_session: Session):
    """アイテム一覧のページネーションテスト"""
    # 5つのテストアイテムを作成
    for i in range(5):
        create_item(db_session, ItemCreate(name=f"Item {i}"))
    
    # ページネーションをテスト
    items = get_items(db_session, skip=2, limit=2)
    
    assert len(items) == 2
    assert items[0].name == "Item 2"
    assert items[1].name == "Item 3"


def test_update_item(db_session: Session, sample_item: Item):
    """アイテム更新のテスト"""
    update_data = ItemUpdate(name="Updated Item", description="Updated Description")
    updated_item = update_item(db_session, sample_item.id, update_data)
    
    assert updated_item is not None
    assert updated_item.name == "Updated Item"
    assert updated_item.description == "Updated Description"
    assert updated_item.id == sample_item.id


def test_update_item_partial(db_session: Session, sample_item: Item):
    """アイテムの部分更新テスト"""
    # 名前のみ更新
    update_data = ItemUpdate(name="Updated Name")
    updated_item = update_item(db_session, sample_item.id, update_data)
    
    assert updated_item is not None
    assert updated_item.name == "Updated Name"
    assert updated_item.description == sample_item.description

    # 説明のみ更新
    update_data = ItemUpdate(description="Updated Description")
    updated_item = update_item(db_session, sample_item.id, update_data)
    
    assert updated_item.name == "Updated Name"  # 前回の更新が維持されている
    assert updated_item.description == "Updated Description"


def test_update_item_not_found(db_session: Session):
    """存在しないアイテムの更新テスト"""
    non_existent_id = UUID('12345678-1234-5678-1234-567812345678')
    update_data = ItemUpdate(name="Updated Item")
    updated_item = update_item(db_session, non_existent_id, update_data)
    
    assert updated_item is None


def test_delete_item(db_session: Session, sample_item: Item):
    """アイテム削除のテスト"""
    # 削除を実行
    result = delete_item(db_session, sample_item.id)
    assert result is True
    
    # 削除されたことを確認
    deleted_item = get_item(db_session, sample_item.id)
    assert deleted_item is None


def test_delete_item_not_found(db_session: Session):
    """存在しないアイテムの削除テスト"""
    non_existent_id = UUID('12345678-1234-5678-1234-567812345678')
    result = delete_item(db_session, non_existent_id)
    
    assert result is False
