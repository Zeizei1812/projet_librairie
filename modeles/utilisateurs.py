
from dataclasses import dataclass, field
from typing import List

@dataclass
class Utilisateur:
    id_utilisateur: int
    nom_utilisateur: str
    livres_empruntes: List[int] = field(default_factory=list)
