from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Кадастр'
    description: str = """Сервис принимает кадастровый номер объекта,
    его широту и долготу и отправляет запрос на внешний сервис"""
    database_url: str
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
