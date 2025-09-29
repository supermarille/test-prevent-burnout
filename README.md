# Prévention du burnout chez les développeuses et les développeurs
Dans une idée de prévenir les situations de burnout des développeuses et 
développeurs, ce script produit un rapport reprenant par personne un taux
de travail “hors horaires”, qu’on définit comme la part des commits
réalisés le week-end ou avant 8h / après 20h.  
Le script Python prend les données du dépôt de Passerelle https://git.entrouvert.org/entrouvert/passerelle.git
et affiche ces taux.

Le résultat au 28/09/25 est le suivant :

```
FREDERIC PETERS : 15% (135/904)
JEROME SCHNEIDER : 14% (4/28)
THOMAS NOEL : 5% (36/721)
LAURELINE GUERIN : 2% (5/291)
JOSUE KOUKA : 2% (2/116)
GAEL PASGRIMAUD : 2% (1/54)
BENJAMIN DAUVERGNE : 2% (15/654)
SERGHEI MIHAI : 1% (5/384)
NICOLAS ROCHE : 1% (4/789)
YANN WEBER : 0% (0/28)
VALENTIN DENIAUD : 0% (0/150)
THOMAS JUND : 0% (0/1)
SERGHEI : 0% (0/4)
PIERRE DUCROQUET : 0% (0/10)
PAUL MARILLONNET : 0% (0/9)
JEAN-BAPTISTE JAILLET : 0% (0/10)
GUILLAUME BAFFOIN : 0% (0/1)
ETIENNE LOUPIAS : 0% (0/2)
EMMANUEL CAZENAVE : 0% (1/364)
ELIAS SHOWK : 0% (0/1)
CORENTIN SECHET : 0% (0/139)
CHRISTOPHE SIRAUT : 0% (0/3)
AGATE BERRIOT : 0% (0/11)
AGATE : 0% (0/8)
```

## Cheminement
### 1. Visualiser (2 min)  
J'ai pris des notes dans un cahier. Ma première étape a été de visualiser le résultat pour avoir un objectif clair à 
atteindre, à garder sous les yeux :
```
- Marie : 10% (10/100)
- Samy : 5% (5/100)
- Jupiler : 1% (1/100)
```
_(mes chats)_

### 2. Explorer l'existant (45 min)  
J'ai passé du temps à regarder les packages Python déjà existants. J'ai trouvé des packages qui font 
déjà tout le travail, comme par exemple [Git Py Stats](https://github.com/git-quick-stats/git-py-stats/tree/main), 
mais du coup ce n'est plus très intéressant à montrer pour un test. Il y a aussi beaucoup plus de fonctionnalités que
l'exercice proposé. J'ai vite trouvé [GitPython](https://gitpython.readthedocs.io/en/stable/index.html), qui m'a paru 
approprié.  
Je n'ai pas trouvé de moyen simple de faire le script sans avoir à cloner le repo.

J'ai navigué un peu dans Passerelle pour savoir à combien d'auteur·ices on doit s'attendre (une dizaine).
Tous les commits ont l'air de bien figurer dans `main`, je n'ai pas trouvé de cas de squash. 

### 3. Ecrire (5h30)
J'ai créé ma première branche et j'ai commencé à écrire le code, en explorant un peu les possibilités de GitPython.
La méthode `iter_commits` de GitPython facilite la tâche. Je normalise les noms pour limiter les doublons. 
Je me lance dans la construction d'un dictionnaire qui contient les infos qu'on cherche :
```
{
'name': {
        'off_work' : 5,
        'total' : 384,
        'rate': 1 
    }
}
```

Je laisse les méthodes `is_weekend` et `is_off_hours` séparées à la fois pour la lisibilité du code et à la fois pour 
laisser la possibilité de faire plus de statistiques par la suite si on le souhaite.

Une fois que j'ai les résultats voulus, il me reste un peu de temps alors j'ajoute des options pour le tri (alphabétique
ou pas taux). J'ajoute aussi des options sur les dates (7 derniers jours ou personnalisé). Par défaut, tous les commits
sont parcourus.

## Améliorations possibles
- [OK] Sur une période de temps donné
- Passer en option l'url du repo
- [OK] Laisser le choix entre le tri alphabétique et le classement par taux ; l'usage est la prévention du burnout, un
classement peut paraître maladroit
- Ajouter des tests
- Trouver un moyen de faire ce rapport sans cloner le repo


## Limitations
### Noms en double
Des noms ont l'air d'être en double, mais il y a peut-être vraiment plusieurs Agate ou Serghei.  

### Fiabilité : réécriture de l'historique Git
Les auteur·ices peuvent changer la date et l'heure des commits (avec `--amend`).
