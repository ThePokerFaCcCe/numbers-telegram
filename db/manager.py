from orm import Manager as BaseManager


class Manager(BaseManager):
    def filter_and(self, *keys):
        query = ""
        for i, k in enumerate(keys):
            prefix = "" if i == 0 else " AND "
            query += f"{prefix} {k} = ?"
        return query

    def get(self, **fields):
        """Get an object from database, return `None` if not found"""
        sql = 'SELECT * FROM %s WHERE ' % self.table_name
        sql += self.filter_and(*fields.keys())

        result = self.db.execute(sql, *fields.values())
        row = result.fetchone()
        if not row:
            return None
        return self.create(**row)

    def has(self, **fields):
        """Check if object with this information exists or not"""
        sql = 'SELECT id FROM %s WHERE ' % self.table_name
        sql += self.filter_and(*fields.keys())

        result = self.db.execute(sql, *fields.values())
        return True if result.fetchall() else False


class ManagerMixin:

    @classmethod
    def manager(cls, db=None, type_check=True):
        return Manager(db if db else cls.db, cls, type_check)
