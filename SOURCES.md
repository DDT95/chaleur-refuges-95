# Sources, licences et limites

Version préparée le **16 août 2026**.

| Lecture | Producteur | Référentiel | Millésime / consultation | Licence | Précaution |
|---|---|---|---|---|---|
| Îlots de chaleur | Institut Paris Region | IMU / LCZ, aléas et vulnérabilités à la chaleur | IMU 2012, publication 2021, consultation 16/08/2026 | Licence Ouverte 2.0 | Potentiel morphoclimatique, pas une température observée. |
| Refuges potentiels | Contributeurs OpenStreetMap | Parcs, jardins, bibliothèques, eau et baignade | consultation 16/08/2026 | ODbL | Inventaire indicatif ; ouverture, accessibilité et confort non garantis. |
| Mesures de température | Météo-France | Données climatologiques de base horaires, dép. 95 | juillet 2020-2026, consultation 17/08/2026 | Licence Ouverte 2.0 | Six stations seulement, plusieurs en bordure de plateforme aéroportuaire. |
| Limites territoriales | État / IGN | Communes et département | COG 2026 | Licence Ouverte 2.0 | Les profils utilisent le centroïde des îlots pour l’affectation communale. |
| Fond cartographique | OpenStreetMap / CARTO | Positron | continu | ODbL | Fond de contexte sans valeur réglementaire. |

## Traitements

- extraction des centroïdes d’îlots situés dans le Val-d’Oise ;
- deux lectures distinctes construites avec les classes d’aléa de jour et de nuit ;
- affichage des 28 105 géométries officielles des îlots morphologiques urbains à toutes les échelles ;
- palette divergente en six classes, stable pendant le zoom : fraîcheur, faible, modéré, marqué, fort et très fort ;
- profils communaux calculés par appartenance du centroïde à la commune ;
- ressources OpenStreetMap filtrées par emprise départementale et réparties en trois familles ;
- exclusion de tout équipement déclaré `access=private` ou `access=no` ; une piscine doit être nommée et comporter un signal d’accès public, clients/adhérents ou un opérateur identifiable ;
- pour les six stations Météo-France du Val-d’Oise, moyenne des températures horaires de juillet (2020-2026) sur la tranche nocturne (22h-5h, heure UTC) et sur l’après-midi (12h-18h, heure UTC), après filtrage des mesures dont l’indicateur qualité Météo-France signale un doute ;
- emprise bâtie contextuelle estimée dans un rayon de 2 km autour de chaque station, par moyenne pondérée par la surface des îlots morphologiques de l’Institut Paris Region qui l’entourent.

## Limites d’usage

La carte est un outil de repérage et de sensibilisation. Elle ne remplace ni une mesure météorologique, ni un diagnostic thermique local, ni un plan canicule communal. La qualification de « refuge climatique » demande une validation par le gestionnaire : horaires, gratuité, accessibilité, ombrage ou climatisation, eau potable et capacité d’accueil.

Le réseau officiel Météo-France du Val-d’Oise ne compte que six stations, et deux d’entre elles (Le Bourget, Roissy) sont installées en bordure de piste d’aéroport : leur température ne représente pas le tissu urbain résidentiel environnant. L’écart mesuré entre la station la plus chaude et la plus fraîche la nuit donne un ordre de grandeur départemental réel de l’îlot de chaleur urbain — comparable à des travaux publiés à partir du même type de croisement stations Météo-France / zones climatiques locales — mais ne permet pas de cartographier l’intensité par commune ou par quartier.

Sources principales : [jeu de données ICU de l’Institut Paris Region](https://data.iledefrance.fr/explore/dataset/ilots-de-chaleur-urbains-icu-classification-des-imu-en-zone-climatique-locale-lc/) et [données climatologiques de base horaires de Météo-France](https://meteo.data.gouv.fr/).
