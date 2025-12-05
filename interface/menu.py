from services.librairie import Librairie

def afficher_menu():
    print("\nMENU LIBRAIRIE")
    print("1 - Afficher tous les livres")
    print("2 - Afficher les livres disponibles")
    print("3 - Ajouter un livre")
    print("4 - Supprimer un livre")
    print("5 - Rechercher (titre, auteur, mot-clé)")
    print("6 - Afficher les utilisateurs")
    print("7 - Ajouter utilisateur")
    print("8 - Supprimer utilisateur")
    print("9 - Emprunter un livre")
    print("10 - Rendre un livre")
    print("11 - Statistiques")
    print("0 - Quitter")


def lancer_application():
    lib = Librairie()
    print("Bienvenue dans la librairie !")

    while True:
        afficher_menu()
        choix = input("Choix : ").strip()

        if choix == "1":
            for l in lib.liste_des_livres():
                print(f"{l.id} | {l.titre} ({l.auteur}) [{l.status.value}]")

        elif choix == "2":
            dispo = lib.livres_disponibles()
            print("Livres disponibles :")
            for t, i in dispo:
                print(f"{i} - {t}")

        elif choix == "3":
            id_l = int(input("ID : "))
            t = input("Titre : ")
            a = input("Auteur : ")
            lib.gestion_livre("ajouter", id_livre=id_l, titre=t, auteur=a)

        elif choix == "4":
            id_l = int(input("ID du livre à supprimer : "))
            lib.gestion_livre("supprimer", id_livre=id_l)

        elif choix == "5":
            mot = input("Titre, nom d'auteur ou mot clé : ")
            res = lib.recherche_par_mot_cle(mot)
            for l in res:
                print(f"{l.id} | {l.titre} ({l.auteur}) [{l.status.value}]")

        elif choix == "6":
            for u in lib.liste_des_utilisateurs():
                print(f"{u.id_utilisateur} | {u.nom_utilisateur} | {u.livres_empruntes}")

        elif choix == "7":
            n = input("Nom : ")
            lib.ajouter_utilisateur(n)

        elif choix == "8":
            id_u = int(input("ID user : "))
            lib.supprimer_utilisateur(id_u)

        elif choix == "9":
            id_u = int(input("ID utilisateur : "))
            id_l = int(input("ID livre : "))
            lib.emprunt_livre(id_u, id_l)

        elif choix == "10":
            id_u = int(input("ID utilisateur : "))
            id_l = int(input("ID livre : "))
            lib.retour_livre(id_u, id_l)

        elif choix == "11":
            lib.statistiques()

        elif choix == "0":
            print("Au revoir !")
            break

        else:
            print("Choix invalide.")

    