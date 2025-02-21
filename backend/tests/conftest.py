import os
import sys
from typing import Generator

import pytest
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

# プロジェクトルートディレクトリをPYTHONPATHに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import settings
from src.db.models.database import Base


# テスト用のデータベースURL
TEST_DATABASE_URL = (
    f"postgresql://{settings.database_user}:"
    f"{settings.database_password}@{settings.database_host}:"
    f"{settings.database_port}/{settings.database_name}_test"
)


@pytest.fixture(scope="session")
def postgres_engine():
    """テスト用のデータベースエンジンを提供するフィクスチャ"""
    # デフォルトのデータベースに接続してテスト用データベースを作成
    default_engine = create_engine(
        f"postgresql://{settings.database_user}:"
        f"{settings.database_password}@{settings.database_host}:"
        f"{settings.database_port}/{settings.database_name}"
    )
    
    # 既存の接続を切断
    default_engine.dispose()
    
    with default_engine.connect() as conn:
        conn.execute(text("COMMIT"))  # 既存のトランザクションを終了
        conn.execute(text(f"DROP DATABASE IF EXISTS {settings.database_name}_test"))
        conn.execute(text("COMMIT"))  # DROP DATABASE後にコミット
        conn.execute(text(f"CREATE DATABASE {settings.database_name}_test"))
        conn.execute(text("COMMIT"))
        conn.execute(text(f"""
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;
            GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO {settings.database_user};
        """))
        conn.execute(text("COMMIT"))
    
    # テスト用データベースに接続
    engine = create_engine(TEST_DATABASE_URL)
    
    # uuid-osspエクステンションをインストール
    with engine.connect() as conn:
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        conn.commit()
    
    Base.metadata.create_all(engine)
    
    yield engine
    
    # テスト終了後にテーブルを削除
    Base.metadata.drop_all(engine)
    
    # 全ての接続を切断してからデータベースを削除
    engine.dispose()
    with default_engine.connect() as conn:
        conn.execute(text("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = :datname
            AND pid <> pg_backend_pid()
        """), {"datname": f"{settings.database_name}_test"})
        conn.execute(text("COMMIT"))
        conn.execute(text(f"DROP DATABASE IF EXISTS {settings.database_name}_test"))
        conn.execute(text("COMMIT"))
    default_engine.dispose()


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    """Alembicの設定を提供するフィクスチャ"""
    config = Config("alembic.ini")
    
    # テスト用データベースURLを設定
    config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    
    return config


@pytest.fixture
def postgres_session(postgres_engine, alembic_config) -> Generator[Session, None, None]:
    """テスト用のデータベースセッションを提供するフィクスチャ"""
    from alembic import command
    
    # マイグレーションを適用
    command.upgrade(alembic_config, "head")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        # マイグレーションをロールバック
        command.downgrade(alembic_config, "base")
