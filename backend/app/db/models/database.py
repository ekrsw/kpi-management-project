from sqlalchemy import create_engine, Column, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from ...core.config import settings
import uuid

# データベース接続URLの構築
DATABASE_URL = (
    f"postgresql://{settings.database_user}:"
    f"{settings.database_password}@{settings.database_host}:"
    f"{settings.database_port}/{settings.database_name}"
)

# エンジンの作成
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# セッションファクトリの設定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# デクラレーティブベースの作成
Base = declarative_base()


class BaseDatabase(Base):
    """
    すべてのデータベースモデルの基底クラスです。

    このクラスは、ID、作成日時、更新日時のカラムを各モデルに自動的に追加します。

    Attributes
    ----------
    id : UUID
        レコードの一意な識別子
    created_at : datetime
        レコードの作成日時を格納するカラム。デフォルトで現在時刻が設定され、変更不可です。
    updated_at : datetime
        レコードの最終更新日時を格納するカラム。デフォルトで現在時刻が設定され、
        レコードが更新されるたびに自動的に更新されます。
    """

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
