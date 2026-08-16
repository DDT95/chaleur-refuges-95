# Îlots de chaleur et refuges climatiques · Val-d’Oise

Décryptage cartographique de l’Atlas territorial de la DDT 95 consacré à l’aléa chaleur de jour et de nuit et aux ressources locales susceptibles d’offrir une pause fraîche.

## Fonctionnement

- carte de chaleur jour / nuit en six classes, construite avec les îlots officiels de l’Institut Paris Region ;
- recherche et portrait des 183 communes ;
- filtres pour les parcs et jardins, bibliothèques, points d’eau, piscines et bases de loisirs ;
- portrait départemental et présentation explicite des limites ;
- interface responsive conforme au gabarit des décryptages de l’Atlas.

Servir le dossier avec un serveur HTTP, par exemple `python3 -m http.server 8426`, puis ouvrir `http://localhost:8426/`.

## Données

Les données d’affichage sont versionnées dans `data/`. Le script `scripts/build_data.py` télécharge les données sources, les limite au Val-d’Oise, simplifie l’aléa sous forme de grille et produit les profils communaux. Il nécessite Python, Shapely et un accès réseau.

## Publication

Site statique compatible avec GitHub Pages. Le workflow `.github/workflows/pages.yml` publie la branche `main`.
