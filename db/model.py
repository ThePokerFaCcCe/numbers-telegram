
from .database import db
from .manager import ManagerMixin


class Model(ManagerMixin, db.Model):

    def delete(self, type_check=True, commit=True):
        result = super().delete(type_check=type_check)
        if commit:
            self.db.commit()
        return result

    def save(self, type_check=True, commit=True):
        result = super().save(type_check=type_check)
        if commit:
            self.db.commit()
        return result

    def update(self, type_check=True, commit=True):
        result = super().update(type_check=type_check)
        if commit:
            self.db.commit()
        return result
