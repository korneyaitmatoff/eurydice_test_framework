from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.engine import Result
from sqlalchemy.orm import (DeclarativeMeta, Query, Session, create_session,
                            declarative_base)


class DatabaseHandler:
    """Database class handler, which using context manager for make session"""
    session: Session

    def __init__(self, user: str, password: str, host: str, port: str, database: str, dialect: str = 'postgresql'):
        self.url = f"{dialect}://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(
            url=self.url,
            echo=False
        )
        self.session = None

    def __enter__(self):
        self.session = create_session(bind=self.engine)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def select(self, table: DeclarativeMeta, filters=()) -> Query:
        """Method for select rows from table with using filters"""
        return self.session.query(table).filter(*filters)

    def insert(self, table: DeclarativeMeta, filters=()) -> None:
        """Method for insert data into table"""
        self.session.query(table).filter(*filters)

    def update(self, table: DeclarativeMeta, data: dict, filters=()) -> None:
        """Method for update rows in the table"""
        self.select(table=table, filters=filters).update(data)
        self.session.commit()

    def delete(self, table: DeclarativeMeta, filters=()) -> None:
        """Method for delete rows in the table"""
        self.select(table=table, filters=filters).delete()
        self.session.commit()

    def execute_sql(self, sql: str) -> Result:
        """Method fot execute sql statement"""
        return self.session.execute(text(sql))

    def get_table_model(self, table_name: str) -> DeclarativeMeta:
        """Method for get table class"""
        (meta := MetaData()).reflect(bind=self.engine)

        if table_name in meta.tables:
            table = meta.tables[table_name]

            table_class = type(
                table_name.capitalize(),
                (declarative_base(),),
                {
                    '__tablename__': table_name,
                    '__table__': table,
                    "__mapper_args__": {"primary_key": table.columns['id']},
                    "columns": [col.name for col in table.columns],
                },
            )

            for col in table.columns:
                setattr(table_class, col.name, col)

            return table_class
        else:
            raise Exception(f"Table {table_name} not found!\n")
