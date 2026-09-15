import os
import requests
import html

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
    
    ascii_art = [
        " 0k%@@@B%hn]<;;/cvc+xv{*@@8&|,UbLuOMdJmWuQ8",
        " [</m%@@@@@*Qj<1ohq)fnnULzXv~^[OCwqOWkm@mm*",
        " j|[{L8@@@@@@@Munoa/i!`     .^\"[OMhcM&oWL0M",
        " OqkqL*@@@@@@@@Bz_[;   .''.      \"_b@%mOw%#",
        " @@@%&B@@@@@@@@@BX. .,>+_-_<!!>:^..[@MaqLx>",
        " @@@@@@@@@@@@@@@@j ^~?][}{))))|||_`\"pY/!`^<",
        " @@@@@@@@@@@@@@@W*>`_!\"^`\"!-[[{)frr<`)f|![0&",
        " QwZd8@@@@@@@@@p)^_!      .<i^^,<]{!?><c&@#",
        " _|tuJmkWB@@@@@n!~->'     \"{<     ^><tO8%m|",
        " _-1/)fnUCCOZkM1;__-+>:^^>_1)'    ,fo8hqZUZ",
        " }?+_]1}]{/jfuQ[,><++>!;:^:>+~,,,_tUCx(--no",
        " ,;>>>-)1){(fffi:;;<>.'^,;+;,;,+}1tLUXc{?|j",
        " '`\";<-[}1{}-__,,::;!,::!~?-:'\"'_+1Um|~_<[|",
        " +\".;][[1tjnf/?\"`,,,^:<>>>~_[~,>i~-1//]_]_>",
        " r-,})[+}nurnz|]````.':;!<_[];:!i]-??+<;+-1",
        " t?[juujjxrff1<,;;,^   `^\",\"'`:>_~1)}]1+,:-",
        " nczvunxrf/||)[>,,:;:^'     ';!^;,.:/jf)->+",
        " jxjjjjftt/|((((1_!,:!i!!;i+_[n):   `[x(_]]",
        " nrfjjfjttt/||)))|)}_<>>><+_?{xO0v_'  `[x|~",
        " ujfjjtrjfftt/|||((|/|()1)(|fxuuzZmQn_' >Ur",
        " jftjffjrjjjfjftttttttttfjjrxrxnuvczUCJx-1Y",
        " /|||fj/jxjjjjrjjjjjjjjjjjjjrrxxnuvcvucUY~;",
        " ()(|tt|(nxjjjrrrrrrrrrrjjjrrrrrxxnuvccvcz_",
        " ||/|)|))nujfjrxxxxxxxxrrjjjjjjrrxxxnuczzjx",
        " ||){1))txrttjrxxxxnnxxrjjjffjjjrxxnnuuczn|",
        " |11))(/tjjtfjrxxxxuuunxrjfffffjxxnuuuvccx/"
    ]

    ascii_lines_html = ""
    start_y = 30
    line_height = 14
    for i, line in enumerate(ascii_art):
        escaped_line = html.escape(line).replace(" ", "&#160;")
        y_pos = start_y + (i * line_height)
        ascii_lines_html += f'    <text x="15" y="{y_pos}" class="ascii-gray">{escaped_line}</text>\n'

    svg = f'''<svg fill="none" width="850" height="420" viewBox="0 0 850 420" xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)">
  <style>
    .bg {{ fill: #0d1117; rx: 8px; }}
    .ascii-gray {{ font: 10px 'Courier New', monospace; fill: #8b949e; white-space: pre; }}
    .title {{ font: bold 13px 'Courier New', monospace; fill: #58a6ff; }}
    .white {{ font: 12px 'Courier New', monospace; fill: #c9d1d9; }}
    .green {{ font: bold 12px 'Courier New', monospace; fill: #3fb950; }}
    .blue {{ font: 12px 'Courier New', monospace; fill: #58a6ff; }}
    .orange {{ font: 12px 'Courier New', monospace; fill: #d29922; }}
    .red {{ font: 12px 'Courier New', monospace; fill: #f85149; }}
    .line {{ font: 12px 'Courier New', monospace; fill: #30363d; }}
  </style>
  <rect width="100%" height="100%" class="bg" />
  
  <!-- FOTO DE PERFIL ASCII CINZA -->
  <g>
{ascii_lines_html}  </g>

  <!-- PAINEL TERMINAL -->
  <g transform="translate(350, 0)">
    <text x="0" y="35" class="title">marco@passarela <tspan class="line">------------------------------------</tspan></text>
    <text x="0" y="65" class="white">. OS: <tspan class="line">................................</tspan> Windows 11, Linux</text>
    <text x="0" y="85" class="white">. Uptime: <tspan class="line">............................</tspan> 29 anos, 2 meses</text>
    <text x="0" y="105" class="white">. Host: <tspan class="line">..............................</tspan> Software Engineer</text>
    <text x="0" y="125" class="white">. IDE: <tspan class="line">...............................</tspan> VS Code, Cursor AI</text>
    
    <text x="0" y="165" class="blue">. Languages.Programming: <tspan class="line">.....</tspan> <tspan class="white">JavaScript, Python, TypeScript, C#</tspan></text>
    <text x="0" y="185" class="blue">. Languages.Computer: <tspan class="line">........</tspan> <tspan class="white">HTML, CSS, JSON, MySQL</tspan></text>
    <text x="0" y="205" class="blue">. Languages.Real: <tspan class="line">............</tspan> <tspan class="white">Português, English Basic</tspan></text>
    
    <text x="0" y="245" class="title">- Contact <tspan class="line">-------------------------------------------------</tspan></text>
    <text x="0" y="270" class="orange">. Email: <tspan class="line">...............................</tspan> <tspan class="blue">marcopassarela@gmail.com</tspan></text>
    <text x="0" y="290" class="orange">. LinkedIn: <tspan class="line">............................</tspan> <tspan class="blue">marcopassarela</tspan></text>
    <text x="0" y="310" class="orange">. GitHub: <tspan class="line">..............................</tspan> <tspan class="blue">marcopassarela</tspan></text>
    
    <text x="0" y="350" class="title">- GitHub Stats <tspan class="line">--------------------------------------------</tspan></text>
    <text x="0" y="375" class="orange">. Repos: <tspan class="line">....</tspan> <tspan class="green">{stats['repos']}</tspan> <tspan class="line">|</tspan> <tspan class="orange">Stars:</tspan> <tspan class="line">..........</tspan> <tspan class="green">{stats['stars']}</tspan></text>
    <text x="0" y="395" class="orange">. Commits: <tspan class="line">..</tspan> <tspan class="green">{stats['commits']}</tspan> <tspan class="line">|</tspan> <tspan class="orange">Followers:</tspan> <tspan class="line">......</tspan> <tspan class="green">{stats['followers']}</tspan></text>
    <text x="0" y="415" class="orange">. Lines of Code: <tspan class="green">{stats['loc']}</tspan> ( <tspan class="green">{stats['loc_add']}++</tspan>, <tspan class="red">{stats['loc_del']}--</tspan> )</text>
  </g>
</svg>'''

    with open("terminal.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_svg()
