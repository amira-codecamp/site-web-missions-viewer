
# 1. Conception de la base de données et jeu d’essai
Avoir une base cohérente, normalisée, prête à être exploitée par l’application

# 2. Gestion des utilisateurs à 03 niveaux
- Administrateur : gestion des utilisateurs, supervision globale.  
- Standard : consultation de ses propres trajets.  
- Gestionnaire de missions : accès en lecture/écriture à tous les trajets.

# 3. Récupération des JSON du labo1p5 (facteurs d’émissions)
Intégration des fichiers JSON du labo1p5 contenant les facteurs d’émissions des différents modes de transport (train, avion, voiture, etc).

# 4. Intégration du code de calcul carbone (l1p5)
Réutiliser et intégrer le module de calcul des émissions carbone développé dans le labo1p5 à partir des distances des trajets.

# 5. Intégration de l’API GeoNames pour localisation
Connecter l’application au service GeoNames afin de corriger et récupérer automatiquement les coordonnées géographiques des villes saisies.

# 6. Formulaire d’ajout et de modification de trajet
Formulaires permettant de saisir un nouveau trajet (départ, destination, mode de transport), d’apporter des modifications ou de supprimer un trajet existant.

# 7. Interface de consultation des trajets
- Afficher une liste des trajets pour l’utilisateur connecté avec l’empreinte carbone en Kg CO2 de chaque trajet.  
- Total des émissions carbone cumulées par l’utilisateur sur ses trajets. Comparer ce total au seuil annuel recommandé par personne (~1 tonne CO₂/an).
- Autres visuels et graphiques (à compléter) ;

# 8. Stockage des trajets et gestion de session utilisateur
Lorsqu’un utilisateur est connecté, ses trajets sont chargés depuis la BDD en session, et peuvent être rechargés si nécessaire (en cas de modification ou de suppression). Utilisation également des tokens pour gérer les sessions.

---

## Technologies :
**Backend** - Django, JWT, REST, MySQL  
**Frontend** - Vue.js  

Projet disponible sur : [https://depot.lipn.univ-paris13.fr/lacroix/sitewebmission](https://depot.lipn.univ-paris13.fr/lacroix/sitewebmission)