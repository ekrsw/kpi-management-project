import pytest
from alembic.command import upgrade, downgrade
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.db.models.database import Base
from src.db.models.item import Item


def test_migrations_stairway(alembic_config: Config, postgres_engine: Engine) -> None:
    """
    このテストは全てのマイグレーションを順番に適用し、
    その後逆順にロールバックすることで、マイグレーションの整合性を確認します。
    """
    from alembic.script import ScriptDirectory
    
    # 全てのリビジョンを取得
    script = ScriptDirectory.from_config(alembic_config)
    revisions = list(reversed([sc.revision for sc in script.walk_revisions()]))

    # 最も古いリビジョンから順番にアップグレード
    for revision in revisions:
        upgrade(alembic_config, revision)
        
        # マイグレーション後にテーブルが存在することを確認
        with postgres_engine.connect() as conn:
            tables = conn.execute(text(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """
            )).fetchall()
            table_names = [table[0] for table in tables]
            
            # 期待されるテーブルが存在することを確認
            if revision == revisions[-1]:  # 最新のリビジョン
                assert 'items' in table_names, "items テーブルが存在しません"

    # 逆順にダウングレード
    for revision in reversed(revisions[:-1]):
        downgrade(alembic_config, revision)
        
        # ダウングレード後のテーブル構造を確認
        with postgres_engine.connect() as conn:
            tables = conn.execute(text(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """
            )).fetchall()
            table_names = [table[0] for table in tables]
            
            # 適切なテーブルが存在することを確認
            if revision == revisions[0]:  # 最初のリビジョン
                assert 'items' not in table_names, "items テーブルが予期せず存在しています"


def test_model_creation(postgres_session):
    """
    モデルの作成が正常に機能することを確認するテスト
    """
    # テストデータの作成
    test_item = Item(
        name="テストアイテム",
        description="テストアイテムの説明"
    )
    
    # データベースにアイテムを追加
    postgres_session.add(test_item)
    postgres_session.commit()
    
    # データベースから追加したアイテムを取得
    saved_item = postgres_session.query(Item).filter_by(name="テストアイテム").first()
    
    # 保存されたデータの検証
    assert saved_item is not None
    assert saved_item.name == "テストアイテム"
    assert saved_item.description == "テストアイテムの説明"
    assert saved_item.id is not None
    assert saved_item.created_at is not None
    assert saved_item.updated_at is not None


def test_model_update(postgres_session):
    """
    モデルの更新が正常に機能することを確認するテスト
    """
    # テストデータの作成と保存
    test_item = Item(
        name="更新前",
        description="更新前の説明"
    )
    postgres_session.add(test_item)
    postgres_session.commit()
    
    # 一度保存したデータを取得して更新
    saved_item = postgres_session.query(Item).filter_by(name="更新前").first()
    saved_item.name = "更新後"
    saved_item.description = "更新後の説明"
    postgres_session.commit()
    
    # 更新されたデータを再取得
    updated_item = postgres_session.query(Item).filter_by(name="更新後").first()
    
    # 更新結果の検証
    assert updated_item is not None
    assert updated_item.name == "更新後"
    assert updated_item.description == "更新後の説明"
    assert updated_item.updated_at > updated_item.created_at
