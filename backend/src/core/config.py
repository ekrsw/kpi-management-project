from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Any


class Settings(BaseSettings):
    """
    アプリケーションの設定を管理するクラスです。

    Attributes
    ----------
    database_host : str
        データベースのホスト名。環境変数 `DATABASE_HOST` から取得します。デフォルトは `"db"` です。
    database_port : int
        データベースのポート番号。環境変数 `DATABASE_PORT` から取得します。デフォルトは `5432` です。
    database_user : str
        データベースのユーザー名。環境変数 `DATABASE_USER` から取得します。デフォルトは `"admin"` です。
    database_password : str
        データベースのパスワード。環境変数 `DATABASE_PASSWORD` から取得します。デフォルトは `"my_database_password"` です。
    database_name : str
        データベースの名前。環境変数 `DATABASE_NAME` から取得します。デフォルトは `"my_database"` です。
    
    redis_host : str
        Redisのホスト名。環境変数 `REDIS_HOST` から取得します。デフォルトは `"redis"` です。
    redis_port : int
        Redisのポート番号。環境変数 `REDIS_PORT` から取得します。デフォルトは `6379` です。
    
    api_host : str
        APIサーバーのホスト名。環境変数 `API_HOST` から取得します。デフォルトは `"0.0.0.0"` です。
    api_port : int
        APIサーバーのポート番号。環境変数 `API_PORT` から取得します。デフォルトは `8000` です。
    
    nginx_port : int
        Nginxのポート番号。環境変数 `NGINX_PORT` から取得します。デフォルトは `8080` です。
    
    secret_key : str
        JWTのシークレットキー。環境変数 `SECRET_KEY` から取得します。必須項目です。
    algorithm : str
        JWTのアルゴリズム。環境変数 `ALGORITHM` から取得します。デフォルトは `"HS256"` です。
    access_token_expire_minutes : int
        アクセストークンの有効期限（分）。環境変数 `ACCESS_TOKEN_EXPIRE_MINUTES` から取得します。デフォルトは `30` 分です。
    refresh_algorithm : str
        リフレッシュトークンのアルゴリズム。環境変数 `REFRESH_ALGORITHM` から取得します。デフォルトは `"HS256"` です。
    refresh_secret_key : str
        リフレッシュトークンのシークレットキー。環境変数 `REFRESH_SECRET_KEY` から取得します。必須項目です。
    refresh_token_expire_minutes : int
        リフレッシュトークンの有効期限（分）。環境変数 `REFRESH_TOKEN_EXPIRE_MINUTES` から取得します。デフォルトは `1440` 分（1日）です。
    
    initial_admin_username : str
        初期管理者ユーザーのユーザー名。環境変数 `INITIAL_ADMIN_USERNAME` から取得します。必須項目です。
    initial_admin_password : str
        初期管理者ユーザーのパスワード。環境変数 `INITIAL_ADMIN_PASSWORD` から取得します。必須項目です。
    """

    # データベース設定
    database: str = "postgresql"
    database_host: str = Field("db")
    database_port: int = Field(5432)
    database_user: str = Field("admin")
    database_password: str = Field("my_database_password")
    database_name: str = Field("my_database")
    
    # Redis設定
    redis_host: str = Field("redis")
    redis_port: int = Field(6379)
    
    # API設定
    api_host: str = Field("0.0.0.0")
    api_port: int = Field(8000)
    
    # Nginx設定
    nginx_port: int = Field(8080)
    
    # JWT設定
    secret_key: str = Field(...)
    algorithm: str = Field("HS256")
    access_token_expire_minutes: int = Field(30)
    refresh_algorithm: str = Field("HS256")
    refresh_secret_key: str = Field(...)
    refresh_token_expire_minutes: int = Field(1440)
    
    # 初期管理者ユーザー設定
    initial_admin_username: str = Field(...)
    initial_admin_password: str = Field(...)
    
    model_config = ConfigDict(
        env_file=".env",
        alias_generator=lambda field_name: field_name.upper()
    )


settings = Settings()
