# Sources, licences et limites

Version préparée le **16 août 2026**.

| Lecture | Producteur | Référentiel | Millésime / consultation | Licence | Précaution |
|---|---|---|---|---|---|
| Îlots de chaleur | Institut Paris Region | IMU / LCZ, aléas et vulnérabilités à la chaleur | IMU 2012, publication 2021, consultation 16/08/2026 | Licence Ouverte 2.0 | Potentiel morphoclimatique, pas une température observée. |
| Refuges potentiels | Contributeurs OpenStreetMap | Parcs, jardins, bibliothèques, eau et baignade | consultation 16/08/2026 | ODbL | Inventaire indicatif ; ouverture, accessibilité et confort non garantis. |
| Limites territoriales | État / IGN | Communes et département | COG 2026 | Licence Ouverte 2.0 | Les profils utilisent le centroïde des îlots pour l’affectation communale. |
| Fond cartographique | OpenStreetMap / CARTO | Positron | continu | ODbL | Fond de contexte sans valeur réglementaire. |

## Traitements

- extraction des centroïdes d’îlots situés dans le Val-d’Oise ;
- agrégation sur une grille d’environ 350 à 400 mètres pour fluidifier la heatmap ;
- deux intensités distinctes construites avec les classes d’aléa de jour et de nuit ;
- affichage des géométries officielles des îlots morphologiques urbains à partir du zoom de quartier ;
- profils communaux calculés par appartenance du centroïde à la commune ;
- ressources OpenStreetMap filtrées par emprise départementale et réparties en trois familles ;
- exclusion de tout équipement déclaré `access=private` ou `access=no` ; une piscine doit être nommée et comporter un signal d’accès public, clients/adhérents ou un opérateur identifiable.

## Limites d’usage

La carte est un outil de repérage et de sensibilisation. Elle ne remplace ni une mesure météorologique, ni un diagnostic thermique local, ni un plan canicule communal. La qualification de « refuge climatique » demande une validation par le gestionnaire : horaires, gratuité, accessibilité, ombrage ou climatisation, eau potable et capacité d’accueil.

Source principale : [jeu de données ICU de l’Institut Paris Region](https://data.iledefrance.fr/explore/dataset/ilots-de-chaleur-urbains-icu-classification-des-imu-en-zone-climatique-locale-lc/).
