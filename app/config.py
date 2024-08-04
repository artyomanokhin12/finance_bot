from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    BOT_API: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    ADMIN_TELEGRAM_API: int

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    class Config:
        env_file = '.env'


settings = Settings()
