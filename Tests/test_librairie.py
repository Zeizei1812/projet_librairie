from modeles.livres import Livre
from modeles.status import STATUS
from modeles.utilisateurs import Utilisateur
from data.donnees_livres import DONNEES_LIVRES
from data.donnees_utilisateurs import DONNEES_UTILISATEURS
from services.librairie import Librairie


def test_initialisation():
    lib = Librairie()
    assert len(lib.livres) == len(DONNEES_LIVRES)
    assert len(lib.utilisateurs) == len(DONNEES_UTILISATEURS)


def test_trouver_livre_utilisateur():
    lib = Librairie()
    livre = lib._trouver_livre(DONNEES_LIVRES[0].id)
    utilisateur = lib._trouver_utilisateur(DONNEES_UTILISATEURS[0].id_utilisateur)
    assert livre.id == DONNEES_LIVRES[0].id
    assert utilisateur.id_utilisateur == DONNEES_UTILISATEURS[0].id_utilisateur


def test_livres_disponibles():
    lib = Librairie()
    dispo = lib.livres_disponibles()
    for titre, identifiant in dispo:
        assert isinstance(titre, str)
        assert isinstance(identifiant, int)
        livre = lib._trouver_livre(identifiant)
        assert livre.status == STATUS.disponible


def test_changer_statut():
    lib = Librairie()
    livre = lib.livres[0]

    # Changer en emprunté
    lib.changer_statut(livre.id, STATUS.emprunte)
    assert livre.status == STATUS.emprunte

    # Changer en disponible
    lib.changer_statut(livre.id, "disponible")
    assert livre.status == STATUS.disponible


def test_gestion_livre_ajouter_supprimer():
    lib = Librairie()

    # Ajouter un livre
    resultat_ajout = lib.gestion_livre("ajouter", id_livre=999, titre="Test", auteur="Moi")
    assert resultat_ajout is True
    assert any(l.id == 999 for l in lib.livres)

    # Supprimer le livre
    resultat_suppr = lib.gestion_livre("supprimer", id_livre=999)
    assert resultat_suppr is True
    assert not any(l.id == 999 for l in lib.livres)


def test_recherche_livres():
    lib = Librairie()

    # Recherche par titre
    titre = DONNEES_LIVRES[0].titre[:3]  # premiers caractères
    resultats_titre = lib.recherche_par_titre(titre)
    assert len(resultats_titre) > 0
    assert all(titre.lower() in l.titre.lower() for l in resultats_titre)

    # Recherche par auteur
    auteur = DONNEES_LIVRES[0].auteur.split()[0]  # première partie du nom
    resultats_auteur = lib.recherche_par_auteur(auteur)
    assert len(resultats_auteur) > 0
    assert all(auteur.lower() in l.auteur.lower() for l in resultats_auteur)

    # Recherche par mot-clé
    mot_cle = "Prince"
    resultats_mot = lib.recherche_par_mot_cle(mot_cle)
    assert len(resultats_mot) > 0
    assert all(mot_cle.lower() in l.titre.lower() or mot_cle.lower() in l.auteur.lower() for l in resultats_mot)


def test_utilisateurs_ajout_suppression():
    lib = Librairie()

    nouvel_id = lib.ajouter_utilisateur("NouvelUtilisateur")
    assert any(u.id_utilisateur == nouvel_id for u in lib.utilisateurs)

    # Essayer de supprimer un utilisateur qui a emprunté un livre
    utilisateur = lib._trouver_utilisateur(nouvel_id)
    livre = lib.livres[0]
    lib.emprunt_livre(utilisateur.id_utilisateur, livre.id)
    resultat_suppr = lib.supprimer_utilisateur(utilisateur.id_utilisateur)
    assert resultat_suppr is False

    # Retour du livre et suppression
    lib.retour_livre(utilisateur.id_utilisateur, livre.id)
    resultat_suppr = lib.supprimer_utilisateur(utilisateur.id_utilisateur)
    assert resultat_suppr is True
    assert utilisateur not in lib.utilisateurs


def test_emprunt_retour_livre():
    lib = Librairie()
    utilisateur = lib.utilisateurs[0]
    livre = lib.livres[0]

    # Emprunt
    res_emprunt = lib.emprunt_livre(utilisateur.id_utilisateur, livre.id)
    assert res_emprunt is True
    assert livre.status == STATUS.emprunte
    assert livre.id in utilisateur.livres_empruntes

    # Essayer d'emprunter à nouveau
    res_emprunt2 = lib.emprunt_livre(utilisateur.id_utilisateur, livre.id)
    assert res_emprunt2 is False

    # Retour
    res_retour = lib.retour_livre(utilisateur.id_utilisateur, livre.id)
    assert res_retour is True
    assert livre.status == STATUS.disponible
    assert livre.id not in utilisateur.livres_empruntes

    # Essayer de retourner un livre non emprunté
    res_retour2 = lib.retour_livre(utilisateur.id_utilisateur, livre.id)
    assert res_retour2 is False


def test_statistiques():
    lib = Librairie()
    total_livres, total_utilisateurs, distribution = lib.statistiques()

    assert total_livres == len(lib.livres)
    assert total_utilisateurs == len(lib.utilisateurs)
    assert isinstance(distribution, dict)
    for nom, livres in distribution.items():
        assert isinstance(nom, str)
        assert isinstance(livres, list)
