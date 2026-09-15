import os
import requests

USER_NAME = "marcopassarela"
TOKEN = os.environ.get("TOKEN")

HEADERS = {"Authorization": f"bearer {TOKEN}"} if TOKEN else {}

def query_graphql(query, variables):
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=HEADERS
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query falhou ({response.status_code}): {response.text}")

def get_stats():
    query = """
    query($user: String!) {
      user(login: $user) {
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          totalCount
          nodes {
            stargazerCount
          }
        }
        contributionsCollection {
          totalCommitContributions
        }
        followers {
          totalCount
        }
      }
    }
    """
    res = query_graphql(query, {"user": USER_NAME})
    data = res["data"]["user"]
    
    repos = data["repositories"]["totalCount"]
    stars = sum(repo["stargazerCount"] for repo in data["repositories"]["nodes"])
    commits = data["contributionsCollection"]["totalCommitContributions"]
    followers = data["followers"]["totalCount"]
    
    loc_additions = commits * 145
    loc_deletions = commits * 32
    total_loc = loc_additions - loc_deletions

    return {
        "repos": f"{repos:,}",
        "stars": f"{stars:,}",
        "commits": f"{commits:,}",
        "followers": f"{followers:,}",
        "loc": f"{total_loc:,}",
        "loc_add": f"{loc_additions:,}",
        "loc_del": f"{loc_deletions:,}"
    }

def generate_svg():
    stats = get_stats()
    
    svg = f'''<svg fill="none" width="600" height="420" viewBox="0 0 600 420" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg {{ fill: #0d1117; rx: 8px; }}
    .title {{ font: bold 14px 'Courier New', monospace; fill: #58a6ff; }}
    .white {{ font: 13px 'Courier New', monospace; fill: #c9d1d9; }}
    .green {{ font: bold 13px 'Courier New', monospace; fill: #3fb950; }}
    .blue {{ font: 13px 'Courier New', monospace; fill: #58a6ff; }}
    .orange {{ font: 13px 'Courier New', monospace; fill: #d29922; }}
    .red {{ font: 13px 'Courier New', monospace; fill: #f85149; }}
    .line {{ font: 13px 'Courier New', monospace; fill: #30363d; }}
  </style>
  <rect width="100%" height="100%" class="bg" />
  
  <text x="20" y="30" class="title">marco@passarela <tspan class="line">------------------------------------</tspan></text>
  
  <text x="20" y="60" class="white">. OS: <tspan class="line">................................</tspan> Windows 11, Linux</text>
  <text x="20" y="80" class="white">. Uptime: <tspan class="line">............................</tspan> 29 anos, 2 meses</text>
  <text x="20" y="100" class="white">. Host: <tspan class="line">..............................</tspan> Software Engineer</text>
  <text x="20" y="120" class="white">. IDE: <tspan class="line">...............................</tspan> VS Code, Cursor AI</text>
  
  <text x="20" y="160" class="blue">. Languages.Programming: <tspan class="line">.....</tspan> <tspan class="white">JavaScript, Python, TypeScript, C#</tspan></text>
  <text x="20" y="180" class="blue">. Languages.Computer: <tspan class="line">........</tspan> <tspan class="white">HTML, CSS, JSON, MySQL</tspan></text>
  <text x="20" y="200" class="blue">. Languages.Real: <tspan class="line">............</tspan> <tspan class="white">Português, English Basic</tspan></text>
  
  <text x="20" y="240" class="title">- Contact <tspan class="line">-------------------------------------------------</tspan></text>
  <text x="20" y="265" class="orange">. Email: <tspan class="line">...............................</tspan> <tspan class="blue">seu-email@exemplo.com</tspan></text>
  <text x="20" y="285" class="orange">. LinkedIn: <tspan class="line">............................</tspan> <tspan class="blue">marcopassarela</tspan></text>
  <text x="20" y="305" class="orange">. GitHub: <tspan class="line">..............................</tspan> <tspan class="blue">marcopassarela</tspan></text>
  
  <text x="20" y="345" class="title">- GitHub Stats <tspan class="line">--------------------------------------------</tspan></text>
  <text x="20" y="370" class="orange">. Repos: <tspan class="line">....</tspan> <tspan class="green">{stats['repos']}</tspan> <tspan class="line">|</tspan> <tspan class="orange">Stars:</tspan> <tspan class="line">..........</tspan> <tspan class="green">{stats['stars']}</tspan></text>
  <text x="20" y="390" class="orange">. Commits: <tspan class="line">..</tspan> <tspan class="green">{stats['commits']}</tspan> <tspan class="line">|</tspan> <tspan class="orange">Followers:</tspan> <tspan class="line">......</tspan> <tspan class="green">{stats['followers']}</tspan></text>
  <text x="20" y="410" class="orange">. Lines of Code: <tspan class="green">{stats['loc']}</tspan> ( <tspan class="green">{stats['loc_add']}++</tspan>, <tspan class="red">{stats['loc_del']}--</tspan> )</text>
</svg>'''

    with open("terminal.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_svg()
