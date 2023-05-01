class Item:
    def __init__(
        self,
        id: int,
        length: float,
        width: float,
        demand: int,
        value: float = None,
        place: list = None,
    ):
        if place is None:
            place = []
        self.id = id
        self.length = int(length)
        self.width = int(width)
        self.demand = demand
        self.value = value
        self.place = place

    __hash__ = object.__hash__
    __slots__ = "id", "length", "demand", "width", "value", "place"

    # for Item printing
    def __repr__(self) -> str:
        return f"\nid: {self.id:3} ,length: {self.length:4} ,width:{self.width:4} ,demand: {self.demand:2} ,value: {self.value:8} ,pos: {self.place}"

    # for sorting
    def __lt__(self, other):
        return (
            self.width < other.width
            if self.width != other.width
            else self.length < other.length
        )
