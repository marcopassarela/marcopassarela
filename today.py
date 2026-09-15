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

def fill_dashes(prefix, font_size, target_px, char_ratio=0.6):
    """Calcula quantos '-' cabem para a linha ir até target_px (em px do viewBox)."""
    char_px = font_size * char_ratio
    used_px = len(prefix) * char_px
    remaining_px = max(0.0, target_px - used_px)
    count = int(remaining_px / char_px)
    return "-" * count

def generate_svg():
    stats = get_stats()

    svg_width = 500
    svg_height = 440
    panel_x = 30
    right_margin = 15
    target_px = svg_width - panel_x - right_margin  # até onde as linhas devem chegar

    title_size = 12  # fonte um pouco menor que antes (era 13)
    text_size = 11   # fonte um pouco menor que antes (era 12)

    header_main = "@marcopassarela " + fill_dashes("@marcopassarela ", title_size, target_px)
    header_contact = "- Contact " + fill_dashes("- Contact ", title_size, target_px)
    header_stats = "- GitHub Stats " + fill_dashes("- GitHub Stats ", title_size, target_px)

    svg = f'''<svg fill="none" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg {{ fill: #0d1117; rx: 8px; }}
    .title {{ font: bold {title_size}px 'Courier New', monospace; fill: #58a6ff; }}
    .white {{ font: {text_size}px 'Courier New', monospace; fill: #c9d1d9; }}
    .green {{ font: bold {text_size}px 'Courier New', monospace; fill: #3fb950; }}
    .blue {{ font: {text_size}px 'Courier New', monospace; fill: #58a6ff; }}
    .orange {{ font: {text_size}px 'Courier New', monospace; fill: #d29922; }}
    .red {{ font: {text_size}px 'Courier New', monospace; fill: #f85149; }}
    .line {{ font: {text_size}px 'Courier New', monospace; fill: #30363d; }}
  </style>
  <rect width="100%" height="100%" class="bg" />

  <!-- PAINEL TERMINAL -->
  <g transform="translate({panel_x}, 0)">
    <text x="0" y="35" class="title">{header_main}</text>
    <text x="0" y="65" class="white">. OS: <tspan class="line">................................</tspan> Windows 11, Linux</text>
    <text x="0" y="85" class="white">. Uptime: <tspan class="line">............................</tspan> 29 anos, 2 meses</text>
    <text x="0" y="105" class="white">. Host: <tspan class="line">..............................</tspan> Software Engineer</text>
    <text x="0" y="125" class="white">. IDE: <tspan class="line">...............................</tspan> VS Code, Cursor AI</text>

    <text x="0" y="165" class="blue">. Languages.Programming: <tspan class="line">.....</tspan> <tspan class="white">JavaScript, Python, TypeScript, C#</tspan></text>
    <text x="0" y="185" class="blue">. Languages.Computer: <tspan class="line">........</tspan> <tspan class="white">HTML, CSS, JSON, MySQL</tspan></text>
    <text x="0" y="205" class="blue">. Languages.Real: <tspan class="line">............</tspan> <tspan class="white">Português, English Basic</tspan></text>

    <text x="0" y="245" class="title">{header_contact}</text>
    <text x="0" y="270" class="orange">. Email: <tspan class="line">...............................</tspan> <tspan class="blue">marcopassarela@gmail.com</tspan></text>
    <text x="0" y="290" class="orange">. LinkedIn: <tspan class="line">............................</tspan> <tspan class="blue">marcopassarela</tspan></text>
    <text x="0" y="310" class="orange">. GitHub: <tspan class="line">..............................</tspan> <tspan class="blue">marcopassarela</tspan></text>

    <text x="0" y="350" class="title">{header_stats}</text>
    <text x="0" y="375" class="orange">. Repos: <tspan class="line">....</tspan> <tspan class="green">{stats['repos']}</tspan> <tspan class="line">|</tspan> <tspan class="orange">Stars:</tspan> <tspan class="line">..........</tspan> <tspan class="green">{stats['stars']}</tspan></text>
    <text x="0" y="395" class="orange">. Commits: <tspan class="line">..</tspan> <tspan class="green">{stats['commits']}</tspan> <tspan class="line">|</tspan> <tspan class="orange">Followers:</tspan> <tspan class="line">......</tspan> <tspan class="green">{stats['followers']}</tspan></text>
    <text x="0" y="415" class="orange">. Lines of Code: <tspan class="green">{stats['loc']}</tspan> ( <tspan class="green">{stats['loc_add']}++</tspan>, <tspan class="red">{stats['loc_del']}--</tspan> )</text>
  </g>
</svg>'''

    with open("terminal.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_svg()
