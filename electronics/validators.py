import datetime
from typing import Any
from rest_framework.exceptions import ValidationError


class ReleaseDateValidator:
    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        try:
            tmp_val = value[self.field]
        except:
            raise ValidationError("release date required")
        if type(tmp_val) is None:
            raise ValidationError("release date cannot be blank")
        tz = datetime.timezone("europe/Moscow")
        if tmp_val > datetime.datetime.now(tz):
            raise ValidationError("release date should be now or earlier")


class SupplierValidator:
    def __init__(self, fields) -> None:
        self.supplier_choice = fields[0]
        self.factory = fields[1]
        self.network = fields[2]

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        tmp_choice = value[self.supplier_choice]
        tmp_factory = value[self.factory]
        tmp_network = value[self.network]
        if tmp_choice == "ФАБРИКА" and (tmp_factory is None or tmp_network is not None):
            raise ValidationError("supplier should be after supplier choice (factory)")
        if tmp_choice == "РОЗНИЧНАЯ СЕТЬ" and (
            tmp_network is None or tmp_factory is not None
        ):
            raise ValidationError("supplier should be after supplier choice (network)")
