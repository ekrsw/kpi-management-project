# KPI Management Project

## テスト

### ユニットテスト

#### Item CRUD テスト

Item モデルに対する CRUD 操作のユニットテストを実装しています。

**テストの実行方法**

```bash
python -m pytest tests/db/crud/test_item.py -v
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

- インメモリ SQLite データベースを使用
- 各テストケース実行後にデータベースをクリーンアップ
- UUID と Datetime 型の SQLite 互換実装

**テストファイル構成**

```
tests/
├── __init__.py
├── conftest.py          # テスト全体の設定
└── db/
    ├── __init__.py
    └── crud/
        ├── __init__.py
        └── test_item.py # Item CRUDテスト
```
