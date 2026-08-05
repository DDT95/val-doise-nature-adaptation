# Sources, licences et limites

Version préparée le **5 août 2026**.

| Lecture | Producteur | Référentiel | Millésime / consultation | Licence | Précaution |
|---|---|---|---|---|---|
| Couvert végétalisé | IGN | BD TOPO `zone_de_vegetation` | extraction 30/07/2026 | Licence Ouverte 2.0 | Décrit des objets végétalisés, pas leur accessibilité ni leur qualité écologique. |
| Réservoirs de nature | INPN / PatriNat et IGN | ZNIEFF I-II et espaces naturels protégés | extraction 30/07/2026 | Licence Ouverte 2.0 | Une ZNIEFF est un inventaire de connaissance, pas une protection réglementaire. Les géométries sont dissoutes avant calcul. |
| Continuités écologiques | Région Île-de-France / Institut Paris Region | Connexions écologiques du SDRIF-E | SDRIF-E adopté en 2024, approuvé en 2025 | Licence Ouverte 2.0 | Lecture prévue au 1:150 000, non parcellaire. |
| Eau | IGN / services de l’État | Réseau des cours d’eau | extraction DDT 95, 2026 | Licence Ouverte 2.0 | Longueur géométrique, sans appréciation de débit, d’état écologique ou de permanence. |
| Observations naturalistes | GeoNat’îdF / ARB Île-de-France | Observations agrégées par maille | consultation 30/07/2026 | Selon charte SINP / GeoNat’îdF | La valeur reflète aussi l’effort de prospection ; absence de donnée ≠ absence d’espèce. |
| Limites territoriales | État / IGN | Communes et EPCI | COG 2026 | Licence Ouverte 2.0 | Les EPCI débordant le département sont limités à leur partie val-d’oisienne. |
| Fond cartographique | OpenStreetMap | Tuiles standard | continu | ODbL | Fond de contexte sans valeur réglementaire. |

## Appuis potentiels de fraîcheur

Cette lecture croise, de manière relative à l’échelle choisie, la part végétalisée (70 %) et la densité du réseau hydrographique (30 %). Elle sert à repérer des supports territoriaux possibles. Elle ne constitue ni une température de surface, ni une mesure d’exposition de la population, ni une délimitation réglementaire d’îlots de fraîcheur.

## Traitements

- calculs géométriques en Lambert-93 (EPSG:2154) ;
- surfaces exprimées en hectares ;
- longueurs exprimées en kilomètres ;
- union géométrique des ZNIEFF et espaces protégés afin de supprimer les doubles comptes ;
- profils EPCI construits uniquement avec les communes du Val-d’Oise ;
- valeurs arrondies pour l’affichage, données calculées conservées avec une décimale ou deux selon l’indicateur.

