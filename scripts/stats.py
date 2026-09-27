"""Builds assets/stats.svg and assets/langs.svg (black · white · blue, like pepesx231.github.io) from the GitHub API.
Runs in GitHub Actions (see .github/workflows/stats.yml) — no outside stats service needed."""
import json, os, urllib.request, html

USER = os.environ.get("GH_USER", "PepesX231")
TOKEN = os.environ["GITHUB_TOKEN"]
Q = """query($login:String!){ user(login:$login){
  followers{totalCount}
  repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){ totalCount nodes{ stargazerCount
    languages(first:10,orderBy:{field:SIZE,direction:DESC}){ edges{ size node{ name color } } } } }
  contributionsCollection{ totalCommitContributions restrictedContributionsCount totalPullRequestContributions
    contributionCalendar{ totalContributions } } } }"""
req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": Q, "variables": {"login": USER}}).encode(),
                             headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"})
u = json.load(urllib.request.urlopen(req))["data"]["user"]
repos = u["repositories"]["nodes"]
stars = sum(r["stargazerCount"] for r in repos)
cc = u["contributionsCollection"]
langs = {}
for r in repos:
    for e in r["languages"]["edges"]:
        n = e["node"]["name"]; langs.setdefault(n, [0, e["node"]["color"] or "#4da3ff"]); langs[n][0] += e["size"]
top = sorted(langs.items(), key=lambda x: -x[1][0])[:6]
tot = sum(v[0] for _, v in top) or 1

FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,Menlo,monospace"
def card(w, h, title, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>.t{{font:700 18px {FONT};fill:#4da3ff}}.l{{font:500 13px {MONO};fill:#8a8a90;letter-spacing:1px}}.v{{font:800 26px {FONT};fill:#f6f6f3}}.n{{font:600 13px {FONT};fill:#c9c9cd}}
.in{{animation:in .8s ease both}}@keyframes in{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}</style>
<rect width="{w}" height="{h}" rx="14" fill="#0b0b0c"/><rect x="24" y="24" width="10" height="10" fill="#4da3ff"/><text class="t" x="44" y="34">{title}</text>{body}</svg>"""

items = [("CONTRIBUTIONS (1Y)", cc["contributionCalendar"]["totalContributions"]), ("COMMITS (1Y)", cc["totalCommitContributions"] + cc["restrictedContributionsCount"]),
         ("PUBLIC REPOS", u["repositories"]["totalCount"]), ("STARS", stars), ("PULL REQUESTS", cc["totalPullRequestContributions"]), ("FOLLOWERS", u["followers"]["totalCount"])]
body = ""
for i, (lab, val) in enumerate(items):
    x, y = 24 + (i % 3) * 150, 78 + (i // 3) * 70
    body += f'<g class="in" style="animation-delay:{i*.08:.2f}s"><text class="v" x="{x}" y="{y}">{val:,}</text><text class="l" x="{x}" y="{y+20}">{lab}</text></g>'
open("assets/stats.svg", "w").write(card(470, 200, "GitHub · PepesX231", body))

body, x = "", 24
bar = ""
for n, (s, c) in top:
    w = 422 * s / tot; bar += f'<rect x="{x:.1f}" y="56" width="{max(w,2):.1f}" height="10" fill="{c}"/>'; x += w
body += f'<clipPath id="r"><rect x="24" y="56" width="422" height="10" rx="5"/></clipPath><g clip-path="url(#r)">{bar}</g>'
for i, (n, (s, c)) in enumerate(top):
    cx, cy = 24 + (i % 2) * 215, 100 + (i // 2) * 30
    body += f'<g class="in" style="animation-delay:{i*.08:.2f}s"><rect x="{cx}" y="{cy-10}" width="10" height="10" fill="{c}"/><text class="n" x="{cx+18}" y="{cy}">{html.escape(n)}</text><text class="l" x="{cx+190}" y="{cy}" text-anchor="end">{100*s/tot:.1f}%</text></g>'
open("assets/langs.svg", "w").write(card(470, 200, "Top languages", body))
print("ok", items, [n for n, _ in top])
