# KPI Management Project

## テスト

### ユニットテスト

#### Item CRUD テスト

Item モデルに対する CRUD 操作のユニットテストを実装しています。

**テストの実行方法**

Docker コンテナ環境でテストを実行します：

```bash
# 特定のテストファイルを実行
docker exec -it kpi_fastapi pytest tests/db/crud/test_item.py -v

# マイグレーションテストを実行
docker exec -it kpi_fastapi pytest tests/db/test_migrations.py -v

# 全てのテストを実行
docker exec -it kpi_fastapi pytest tests -v
```

**テストの内容**

1. Create 操作のテスト

   - 通常のアイテム作成
   - 説明なしのアイテム作成

2. Read 操作のテスト

   - 単一アイテムの取得
   - 存在しないアイテムの取得
   - アイテム一覧の取得
   - ページネーション機能

3. Update 操作のテスト

   - 全フィールドの更新
   - 部分的な更新（名前のみ、説明のみ）
   - 存在しないアイテムの更新

4. Delete 操作のテスト
   - アイテムの削除
   - 存在しないアイテムの削除

**テスト環境**

- PostgreSQL データベースを使用（テスト用の別データベースを自動作成）
- 各テストケース実行後にデータを自動クリーンアップ
- uuid-ossp エクステンションを自動設定
- マイグレーションの自動適用とロールバック

**テストファイル構成**

```
tests/
├── __init__.py
├── conftest.py          # テスト全体の設定とフィクスチャ
├── pytest.ini          # pytestの設定
└── db/
    ├── __init__.py
    ├── test_migrations.py  # マイグレーションテスト
    └── crud/
        ├── __init__.py
        └── test_item.py    # Item CRUDテスト
```
