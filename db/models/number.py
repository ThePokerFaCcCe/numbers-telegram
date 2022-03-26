from .. import Model


class Number(Model):
    number = str

    def __init__(self, number) -> None:
        super().__init__()
        self.number = number
