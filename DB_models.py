from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy import func
import sqlalchemy.orm
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated

from DB_config import sync_engine
from DB import Base_Model

intpk = Annotated[int, mapped_column(primary_key = True)]
strnotnull = Annotated[str, mapped_column(nullable = False)]


class Table_documents(Base_Model):
    __tablename__ = "Documents"
    ID_doc: Mapped[intpk]
    psth: Mapped[strnotnull]
    date: Mapped[datetime] = mapped_column(nullable = False, server_default = func.now())

    children: Mapped['Table_documents_text'] = relationship(back_populates = 'parent', cascade='all, delete')

class Table_documents_text(Base_Model):
    __tablename__ = "Documents_text"
    ID: Mapped[intpk]
    ID_doc: Mapped[int] = mapped_column(ForeignKey("Documents.ID_doc", ondelete = "CASCADE"), nullable = False)
    text: Mapped[strnotnull]

    parent: Mapped["Table_documents"] = relationship(back_populates = 'children')

def create_Tables_ORM():
    sync_engine.echo = True
    Base_Model.metadata.drop_all(sync_engine)
    Base_Model.metadata.create_all(sync_engine)
    sync_engine.echo = False





