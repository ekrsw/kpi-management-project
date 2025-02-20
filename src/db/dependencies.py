from typing import Generator
from sqlalchemy.orm import Session
from .models.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    データベースセッションを取得するための依存関数です。

    この関数は、セッションファクトリ `SessionLocal` を使用して
    データベースセッションを生成し、FastAPIの依存関係として提供します。
    リクエストごとに新しいセッションを作成し、リクエスト終了時にセッションをクローズします。

    Yields
    ------
    Session
        使用中のデータベースセッションオブジェクト。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
