import pytest
from src.main.api.db.engine import SessionLocal, engine


@pytest.fixture(scope='function')
def db_session():
    connection = engine.connect()   # Соединение через движок
    transaction = connection.begin()    # Контейнер операций с БД (вставки, удаления и тп)
    session = SessionLocal(bind=connection)     #Соединение
    try:
        yield session
    finally:
        session.close()     # Закрыввем сессию
        transaction.rollback()      # Откат транзакции
        connection.close()      # Закрытие соединения
