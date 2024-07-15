from typing import Any
from rest_framework.exceptions import ValidationError

class NameValidator:
    def __init__(self, field) -> None:
        self.field = field
    
    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        try:
            tmp_val = value[self.field]
        except:
            ValidationError("name error")
        if type(tmp_val) is None:
            raise ValidationError("name cannot be blank")
        if len(tmp_val) > 64:
            raise ValidationError("name is to large")