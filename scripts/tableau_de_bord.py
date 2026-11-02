#!/usr/bin/env python3
"""Tableau de bord statistique : chiffres agrégés uniquement, aucun contenu lu."""
import subprocess, datetime

SEUIL = 3  # secret statistique : les petits effectifs sont masqués

def sql(q):
    r = subprocess.run(["docker-compose", "exec", "-T", "postgres", "psql", "-U", "synapse",
                        "-d", "synapse", "-At", "-F", "|", "-c", q],
                       capture_output=True, text=True, check=True)
    return [l.split("|") for l in r.stdout.strip().splitlines() if l]

def un(q):
    return int(sql(q)[0][0])

def masque(n):
    return "< %d" % SEUIL if 0 < n < SEUIL else str(n)

MS24H = "(extract(epoch from now())*1000 - 86400000)"
actifs = un("SELECT count(*) FROM users WHERE deactivated=0")
revoques = un("SELECT count(*) FROM users WHERE deactivated=1")
salons = un("SELECT count(*) FROM rooms")
salons_chiffres = un("SELECT count(DISTINCT room_id) FROM events WHERE type='m.room.encryption'")
msgs24 = un("SELECT count(*) FROM events WHERE type='m.room.encrypted' AND origin_server_ts > " + MS24H)
agents24 = un("SELECT count(DISTINCT sender) FROM events WHERE type='m.room.encrypted' AND origin_server_ts > " + MS24H)
jours = sql("SELECT to_char(to_timestamp(origin_server_ts/1000),'YYYY-MM-DD'), count(*) FROM events "
            "WHERE type='m.room.encrypted' AND origin_server_ts > (extract(epoch from now())*1000 - 604800000) "
            "GROUP BY 1 ORDER BY 1")
part = round(100 * salons_chiffres / salons) if salons else 0
mx = max([int(c) for _, c in jours] + [1])
barres = "".join(
    "<tr><td>%s</td><td><div class='b' style='width:%d%%'></div></td><td>%s</td></tr>"
    % (j, 100 * int(c) / mx, masque(int(c))) for j, c in jours)

page = """<!doctype html><html lang="fr"><meta charset="utf-8"><title>Tableau de bord</title>
<style>body{font-family:sans-serif;max-width:760px;margin:30px auto;padding:0 12px}
.k{display:inline-block;border:1px solid #ccc;border-radius:8px;padding:12px 18px;margin:6px;min-width:150px}
.k b{font-size:28px;display:block}.b{background:#0a7;height:16px}td{padding:3px 8px}</style>
<h1>Messagerie souveraine : tableau de bord</h1>
<p>Statistiques agrégées. Aucun message n'est lu. Effectifs inférieurs à 3 masqués. Généré le %s.</p>
<div class="k"><b>%s</b>agents actifs</div><div class="k"><b>%s</b>agents révoqués</div>
<div class="k"><b>%s</b>salons</div><div class="k"><b>%d %%</b>salons chiffrés</div>
<div class="k"><b>%s</b>messages chiffrés (24 h)</div><div class="k"><b>%s</b>agents actifs (24 h)</div>
<h2>Messages chiffrés par jour (7 jours)</h2><table>%s</table></html>""" % (
    datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), masque(actifs), masque(revoques),
    masque(salons), part, masque(msgs24), masque(agents24), barres)

open("tableau_de_bord.html", "w", encoding="utf-8").write(page)
print("Tableau de bord généré : tableau_de_bord.html")
