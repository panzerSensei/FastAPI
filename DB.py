from sqlalchemy.orm import DeclarativeBase

class Base_Model(DeclarativeBase):
    def __repr__(self): ## переопределили вывод на мечать данных, чтобы ну хоть что-то информативное получать
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f'{col}={getattr(self, col)}')
        return f"<{self.__class__.__name__} {','.join(cols)}>"