from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Кадастр'
    description: str = """Сервис принимает кадастровый номер объекта,
    его широту и долготу и отправляет запрос на внешний получает ответ True или False"""
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        env_file = '.env'


settings = Settings()
