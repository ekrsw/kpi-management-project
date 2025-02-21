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

## 本番環境向けの設定

### セキュリティ設定

1. 強力なパスワードの設定

```bash
# SECRET_KEYとREFRESH_SECRET_KEYの生成
openssl rand -hex 32  # 各キーに対して実行
```

2. SSL/TLS 証明書の設定

- 証明書と秘密鍵を`./ssl/`ディレクトリに配置
  - cert.pem: SSL 証明書
  - key.pem: 秘密鍵

3. 環境変数の設定

- ENVIRONMENT=production
- ALLOWED_HOSTS: 実際のドメイン名を設定
- CORS_ORIGINS: フロントエンドのドメインを設定
- データベースと Redis の認証情報を強力なものに変更

### データベースマイグレーション

#### 本番環境での初回デプロイ

1. データベースの初期化

```bash
# PostgreSQLコンテナの起動（uuid-ossp拡張とタイムスタンプ更新関数の作成）
docker-compose up -d postgres
```

2. マイグレーションの実行

```bash
docker-compose exec fastapi alembic upgrade head
```

#### 本番環境での更新手順

1. バックアップの作成（必須）

```bash
# タイムスタンプ付きでバックアップを作成
docker-compose exec postgres pg_dump -U ${DATABASE_USER} ${DATABASE_NAME} > backup_$(date +%Y%m%d_%H%M%S).sql
```

2. マイグレーションの適用

```bash
# マイグレーションの実行
docker-compose exec fastapi alembic upgrade head
```

3. 問題発生時のロールバック

```bash
# 直前のバージョンに戻す場合
docker-compose exec fastapi alembic downgrade -1

# 特定のバージョンに戻す場合
docker-compose exec fastapi alembic downgrade <revision_id>
```

### 開発環境でのマイグレーション

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

### 本番環境での注意事項

1. セキュリティ

- 定期的なセキュリティアップデートの実施
- ログの定期的な監査
- 不要なポートの閉鎖

2. バックアップ

- 定期的なバックアップの自動化
- バックアップの暗号化
- 別の場所へのバックアップの保存

3. パフォーマンス

- コネクションプールの適切な設定
- キャッシュの活用
- 定期的なパフォーマンスモニタリング

4. メンテナンス

- システムアップデートの計画的な実施
- ディスク使用量の監視
- ログローテーションの設定

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
- テスト環境でのみ実行し、本番環境では実行しないでください
