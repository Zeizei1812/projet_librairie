
from dataclasses import dataclass
from modeles.status import STATUS

@dataclass
class Livre:
    id: int
    titre: str
    auteur: str
    status: STATUS = STATUS.disponible