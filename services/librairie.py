
import matplotlib.pyplot as plt
from modeles.livres import Livre
from modeles.status import STATUS
from modeles.utilisateurs import Utilisateur
from data.donnees_livres import DONNEES_LIVRES
from data.donnees_utilisateurs import DONNEES_UTILISATEURS

class Librairie:
    def __init__(self, livres=None, utilisateurs=None):
        self.livres = list(livres) if livres else list(DONNEES_LIVRES)
        self.utilisateurs = list(utilisateurs) if utilisateurs else list(DONNEES_UTILISATEURS)
    """FONCTIONS INTERNES"""


    def _trouver_livre(self, id_livre):
        for livre in self.livres:
            if livre.id == id_livre:
                return livre
        return None

    def _trouver_utilisateur(self, id_utilisateur):
        for u in self.utilisateurs:
            if u.id_utilisateur == id_utilisateur:
                return u
        return None


    """gestion des livres : liste des livres disponibles, chnagement de statut, ajout et suppression d'un livre, recherche
    par titre, auteur, mot-clé d'un livre"""


    def liste_des_livres(self):
        return self.livres

    def livres_disponibles(self):
        livres_dispo = []
        for livre in self.livres:
            if livre.status == STATUS.disponible:
                livres_dispo.append((livre.titre, livre.id))
        return livres_dispo

    def changer_statut(self, id_livre, nouveau_statut):

        if isinstance(nouveau_statut, str):
            if nouveau_statut == "disponible":
                nouveau_statut = STATUS.disponible
            elif nouveau_statut == "emprunte":
                nouveau_statut = STATUS.emprunte
            else:
                print("Statut invalide")
                return False

        for livre in self.livres:
            if livre.id == id_livre:
                livre.status = nouveau_statut
                print("Statut changé avec succès !")
                return True

        print("Livre non trouvé.")
        return False

    def gestion_livre(self, action, id_livre=None, titre=None, auteur=None):

        if action == "ajouter":
            if id_livre is None or titre is None or auteur is None:
                print("Il faut id + titre + auteur pour ajouter.")
                return False

            if any(livre.id == id_livre for livre in self.livres):
                print("Un livre avec cet ID existe déjà !")
                return False

            self.livres.append(Livre(id=id_livre, titre=titre, auteur=auteur, status=STATUS.disponible))
            print(f"Livre '{titre}' ajouté !")
            return True

        elif action == "supprimer":
            for livre in self.livres:
                if livre.id == id_livre:
                    if livre.status == STATUS.disponible:
                        self.livres.remove(livre)
                        print("Livre supprimé.")
                        return True
                    else:
                        print("Livre emprunté, suppression impossible.")
                        return False

            print("Livre non trouvé !")
            return False

        else:
            print("Action inconnue.")
            return False



    def recherche_par_titre(self, titre):
        return [livre for livre in self.livres if titre.lower() in livre.titre.lower()]

    def recherche_par_auteur(self, auteur):
        return [livre for livre in self.livres if auteur.lower() in livre.auteur.lower()]

    def recherche_par_mot_cle(self, mot_cle):
        mot_cle = mot_cle.lower()
        return [
            livre for livre in self.livres
            if mot_cle in livre.titre.lower() or mot_cle in livre.auteur.lower()
        ]


    """GESTION DES UTILISATEURS"""


    def liste_des_utilisateurs(self):
        return self.utilisateurs

    def ajouter_utilisateur(self, nom):
        nouvel_id = max(u.id_utilisateur for u in self.utilisateurs) + 1
        self.utilisateurs.append(Utilisateur(id_utilisateur=nouvel_id, nom_utilisateur=nom))
        print(f"Utilisateur '{nom}' ajouté !")
        return nouvel_id

    def supprimer_utilisateur(self, id_utilisateur):
        utilisateur = self._trouver_utilisateur(id_utilisateur)
        if utilisateur is None:
            print("Utilisateur non trouvé.")
            return False

        if utilisateur.livres_empruntes:
            print("Utilisateur a encore des livres, suppression impossible.")
            return False

        self.utilisateurs.remove(utilisateur)
        print("Utilisateur supprimé.")
        return True


    """EMPRUNTS & RETOURS"""


    def emprunt_livre(self, id_utilisateur, id_livre):

        utilisateur = self._trouver_utilisateur(id_utilisateur)
        livre = self._trouver_livre(id_livre)

        if utilisateur is None or livre is None:
            print("Utilisateur ou livre introuvable.")
            return False

        if livre.status == STATUS.emprunte:
            print("Livre déjà emprunté.")
            return False

        livre.status = STATUS.emprunte
        utilisateur.livres_empruntes.append(id_livre)

        print(f"{utilisateur.nom_utilisateur} a emprunté '{livre.titre}'.")
        return True

    def retour_livre(self, id_utilisateur, id_livre):

        utilisateur = self._trouver_utilisateur(id_utilisateur)
        livre = self._trouver_livre(id_livre)

        if utilisateur is None or livre is None:
            print("Utilisateur ou livre introuvable.")
            return False

        if id_livre not in utilisateur.livres_empruntes:
            print("Cet utilisateur n'a pas ce livre.")
            return False

        livre.status = STATUS.disponible
        utilisateur.livres_empruntes.remove(id_livre)

        print(f"{utilisateur.nom_utilisateur} a rendu '{livre.titre}'.")
        return True


    """STATISTIQUES"""

    def statistiques(self):
        total_livres = len(self.livres)
        total_utilisateurs = len(self.utilisateurs)
        distribution = {}

        print("STATISTIQUES")
        print(f"Total livres : {total_livres}")
        print(f"Total utilisateurs : {total_utilisateurs}")

        titres = {livre.id: livre.titre for livre in self.livres}

        """Graphique permettant de visualiser le nombre d'utilisateur qui ont emprunté des livres"""
        noms = []
        nombre_livres = []

        for u in self.utilisateurs:
            emprunts = [titres[id_l] for id_l in u.livres_empruntes]
            distribution[u.nom_utilisateur] = emprunts
            noms.append(u.nom_utilisateur)
            nombre_livres.append(len(emprunts))

            print(f"- {u.nom_utilisateur} : {len(emprunts)} emprunt(s)")
            if emprunts:
                print("  → " + ", ".join(emprunts))


        plt.figure(figsize=(8, 5))
        plt.bar(noms, nombre_livres)
        plt.title("Nombre de livres empruntés par utilisateur")
        plt.xlabel("Utilisateurs")
        plt.ylabel("Livres empruntés")
        plt.tight_layout()
        plt.show()

        return total_livres, total_utilisateurs, distribution

