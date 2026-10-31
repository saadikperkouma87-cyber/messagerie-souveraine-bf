#!/bin/bash
# Usage : ./scripts/revoquer.sh agent1 MOT_DE_PASSE_ADMIN
# Révoque un agent : déconnecte ses appareils, le retire des salons, désactive le compte.
set -e
USER_ID="@$1:localhost"
API="http://localhost:8008"
TOKEN=$(curl -s -X POST $API/_matrix/client/v3/login -H "Content-Type: application/json" \
  -d "{\"type\":\"m.login.password\",\"identifier\":{\"type\":\"m.id.user\",\"user\":\"admin\"},\"password\":\"$2\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
curl -s -X POST "$API/_synapse/admin/v1/deactivate/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"erase": false}'
echo
echo "Agent $USER_ID révoqué : compte désactivé, appareils déconnectés, retiré des salons."
