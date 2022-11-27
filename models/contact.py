from dataclasses import dataclass, field


@dataclass
class Contact:
    first_name: str
    last_name: str
    tel: int
    id: int | None = field(
        default=None,
        compare=False,
    )
