# Messagerie souveraine BF — équipe Stat~Tech

Messagerie instantanée chiffrée de bout en bout pour les agents de l'administration publique du Burkina Faso, hébergeable sur l'infrastructure de l'État. Projet du Sprint technique pré-hackathon 2026 (Hackathon 226).
Équipe : PERKOUMA Mouhamad Saadik, NIKIEMA Kiswendsida Rachelle, ZOU Assane Narcisse (Master 1 MIME-MISE, Université Thomas Sankara).

## Concept
Les agents échangent messages, groupes et fichiers dans des salons chiffrés. Le serveur ne peut lire aucun contenu. Seuls des agents enrôlés par l'administrateur entrent, et un agent révoqué est coupé immédiatement. Notre innovation : un tableau de bord statistique qui permet de piloter l'usage sans jamais lire un message.

## Architecture
- Synapse (serveur Matrix) + PostgreSQL + Element Web (client), lancés par Docker Compose.
- Chiffrement de bout en bout Olm/Megolm (protocole Matrix), forcé dans tous les salons. Aucune cryptographie écrite par l'équipe.
- Inscription libre désactivée, invités refusés, fédération désactivée (aucun serveur ni service tiers).
- `scripts/revoquer.sh` : désactive le compte, déconnecte les appareils, retire l'agent des salons.
- `scripts/tableau_de_bord.py` : statistiques agrégées, effectifs inférieurs à 3 masqués (secret statistique).

## Technologies et licences
| Composant | Licence | Lien |
|---|---|---|
| Synapse | AGPL-3.0 | https://github.com/element-hq/synapse |
| Element Web | AGPL-3.0 | https://github.com/element-hq/element-web |
| Olm/Megolm (protocole Matrix) | Apache-2.0 | https://matrix.org |
| PostgreSQL | PostgreSQL License | https://www.postgresql.org |
| Docker / Docker Compose | Apache-2.0 | https://www.docker.com |
Notre code : AGPL-3.0 (fichier LICENSE).

## Niveau d'engagement
**Étendre et adapter** : configuration de sécurité, scripts de révocation et de statistiques, habillage aux couleurs du Burkina.

## Installation (une commande)
Prérequis : Docker et Docker Compose.
1. `git clone https://github.com/saadikperkouma87-cyber/messagerie-souveraine-bf.git && cd messagerie-souveraine-bf`
2. Générer la configuration Synapse puis appliquer les réglages de sécurité (voir `docs/INSTALLATION.md`).
3. `docker-compose up -d`
4. Ouvrir http://localhost:8080

## Comptes de démonstration (fictifs)
admin / `Demo-Admin-2026!` — agent1 / `Demo-Agent1-2026!` (créés par l'administrateur, inscription libre refusée).

## Limites
Pas de double authentification (perspective). HTTP local sans TLS. Mot de passe de base de démonstration visible. Interface en langues nationales en perspective. Voir la note de sécurité.
