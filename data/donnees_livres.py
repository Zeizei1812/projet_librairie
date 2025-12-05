
import random
from modeles.livres import Livre
from modeles.status import STATUS

DONNEES_LIVRES = [
    Livre(id=1, titre="Les Misérables", auteur="Victor Hugo",
          status=random.choice([STATUS.disponible, STATUS.emprunte])),
    Livre(id=2, titre="Le Petit Prince", auteur="Antoine de Saint-Exupéry",
          status=random.choice([STATUS.disponible, STATUS.emprunte])),
    Livre(id=3, titre="Prince of Persia", auteur="Jordan Mechner",
          status=random.choice([STATUS.disponible, STATUS.emprunte])),
]