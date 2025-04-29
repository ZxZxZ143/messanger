
#устанавливаем общие настройки, подключение к дб и секретный ключ для токена
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:134679002@localhost:5432/corporate_messenger'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jdflbgsiyverifnvoljnadrligfbayeibniaeythbl'