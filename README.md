# Où le vivant résiste-t-il dans le Val-d’Oise ?

Décryptage cartographique de l’Atlas territorial de la DDT 95 consacré aux réservoirs de nature, aux continuités écologiques, à l’eau et aux appuis potentiels de fraîcheur.

## Fonctionnement

- recherche d’une commune ou d’un EPCI ;
- cinq lectures cartographiques, une seule active à la fois ;
- survol avec mise en évidence et valeur contextualisée ;
- portrait territorial au clic ;
- fiche autonome imprimable ou exportable en PDF ;
- présentation explicite des sources et limites.

Servir le dossier avec un serveur HTTP, par exemple `python3 -m http.server 8426`, puis ouvrir `http://localhost:8426/`.

## Données

Les fichiers publics nécessaires à l’interface sont versionnés dans `data/`. Les profils communaux et intercommunaux sont produits par `scripts/build_profiles.py`. Le script :

1. intersecte les couches avec les limites territoriales en projection Lambert-93 ;
2. dissout les chevauchements entre inventaires et protections pour éviter les doubles comptes ;
3. calcule les surfaces végétalisées et de réservoirs, les longueurs de cours d’eau et le nombre de connexions ;
4. agrège les communes val-d’oisiennes par EPCI.

Installer les dépendances avec `pip install -r requirements.txt`, puis exécuter `python scripts/build_profiles.py`.

## Publication

Site statique compatible avec GitHub Pages. Le workflow `.github/workflows/pages.yml` publie la branche `main`.

