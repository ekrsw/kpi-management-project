# KPI Management Project

## 概要

KPI 管理システム

## 環境構築

### 必要条件

- Docker
- Docker Compose

### セットアップ

1. リポジトリをクローン

```bash
git clone [repository-url]
```

2. 環境変数ファイルの設定

```bash
cp .env.example .env
# .envファイルを編集して必要な環境変数を設定
```

3. Docker コンテナの起動

```bash
docker-compose up -d
```

## データベースマイグレーション

### マイグレーションコマンド

#### 新しいマイグレーションの作成

モデルを変更した後、以下のコマンドで変更を検出してマイグレーションファイルを作成します：

```bash
docker exec -it kpi_fastapi alembic revision --autogenerate -m "変更の説明"
```

#### マイグレーションファイルの確認

生成されたマイグレーションファイルは `migrations/versions/` ディレクトリに保存されます。
適用前に必ずファイルの内容を確認してください。

#### マイグレーションの適用

データベースに変更を適用します：

```bash
docker exec -it kpi_fastapi alembic upgrade head
```

#### その他の便利なコマンド

- 現在のリビジョンを確認：

```bash
docker exec -it kpi_fastapi alembic current
```

- マイグレーション履歴の確認：

```bash
docker exec -it kpi_fastapi alembic history
```

- 1 つ前のバージョンに戻す：

```bash
docker exec -it kpi_fastapi alembic downgrade -1
```

- 特定のバージョンに戻す：

```bash
docker exec -it kpi_fastapi alembic downgrade <revision_id>
```

### 注意事項

- マイグレーションコマンドを実行する前に、FastAPI コンテナ（kpi_fastapi）が起動していることを確認してください
- マイグレーションファイル生成後は、必ず内容を確認してから適用してください
- 本番環境での実行時は特に慎重にマイグレーションの内容を確認してください

## テスト

### マイグレーションテストの実行

マイグレーションのテストを実行するには、以下のコマンドを使用します：

```bash
docker exec -it kpi_fastapi pytest tests/db/test_migrations.py -v
```

このテストでは以下の項目を確認します：

1. マイグレーションの整合性テスト

   - 全てのマイグレーションを順番に適用
   - 適用後のテーブル構造の確認
   - 逆順でのロールバック確認

2. モデルの操作テスト
   - データの作成
   - データの更新
   - タイムスタンプの動作確認

テスト実行時の注意事項：

- テストはテスト用のデータベース（my_database_test）を使用します
- 各テスト後にデータは自動的にクリーンアップされます
