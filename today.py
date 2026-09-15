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
    
    # Arte ASCII gerada diretamente a partir da sua foto de perfil oficial
    ascii_art = [
        "0mu\\X#$@&0/tY0v[mY>zcZ&UwLmOOUbp0*zz0hUZ@@",
        "QoQ_-(k$@$#v-!_)\\UxmkjBZwX[YX*BokqY8o{z@$#",
        "JCuXdZO#$$$Bdt?>rLUfCz$$$c[8ZZBda*Z$c{d&#x",
        "M88pLx/-UB@$$$kjx$Wfvczjf-!Q*&k@&Bk8%$Mx(X",
        "QvrCJJLUuq$@@@$$wUk}\"     'ivph@8ho$on+~08",
        "!-CpoM#B@&$$$$@@$L!. ,i>:''  .Z$8W8Q)jLa$$",
        "?\\Qh$$$$@$$$$$$@@M^`?)|//|\\\\[.[%wt<;X%$@B@",
        "!+>}0%$$$@@$$$$@$0`]_<_{\\tfvY[iUt,/a$@@W#$",
        "`^!]jLh#M$$$@@@@M[+i    i->+(t_{[m$$@&B$$$",
        " `;-{][nYq*B$$$$z<{i   .]]   `_(p$WxLa8@$@",
        "'`~<-[})jjc0Zmd8t~{}]<;~(/`  ,Y%aqwkvmM%@@",
        "\"!?1{-{[-{\\)tvzm1!-]<!!:>_+~]xmQu[xM%@$$$@",
        " _i `:^!__|j/|tt~!>-,`i?}!,<(tdwn)\\C$$$B@$",
        "~-r{~+;',[(\\rn\\},;iii++-}[;>-{UU[][)ZqCXwm",
        "::[QJOc+_t}\\UYCc_',`^++-1\\~<-}{|[])(}?\\pO(",
        "^:.|jrv[/YunYzc|~i:' .,!~\";+]|f{{<i\\};<\\<^",
        ">`-()/XJLCJXuxr(<;i>:'.  '<;>\"-cc\\_[?+;i:,",
        ";[nXzzcXccvunxrrj(+i<~<<-]ru! '_vt11{[]}{-",
        "[zzuurzzccvvunxrfjr\\[??]})xwbX-'`\\c][11()-",
        "nnxnufYvvcczvvunnxrxnxxnuzUYQddC1,Uz`;~-[)",
        "jxurrnXnnvvzzcccvvvvvvvczzXYUCL0wL{uf}]><)",
        "frur/UufrvnuYzczzzzzzzzzzzXXYUCCJ0Y>tr(?<]",
        "ffu/rCrrxrxjUXvzXXYYXXzzzzzzXYYJLLJr?~i>!!",
        "jjr|UvrxttfnYvuzXYYYYXzcvvczXYUUJQYYnfxxnt",
        "jr\\rXxrttjrucuvXXYYJJYXcvuucYYYUCLYzx1(|t1",
        "rj|vxjfrxnnuuvcXYYUJJUXcunxuzXvXLQzcv}t\\/(",
        "r/|xfrxf/tjxuvcXYYUUJUXcnxrrncYJLOYuX|Cwbh"
    ]

    ascii_lines_html = ""
    start_y = 32
    line_height = 14
    for i, line in enumerate(ascii_art):
        escaped_line = html.escape(line).replace(" ", "&#160;")
        y_pos = start_y + (i * line_height)
        ascii_lines_html += f'    <text x="20" y="{y_pos}" class="ascii">{escaped_line}</text>\n'

    svg = f'''<svg fill="none" width="850" height="430" viewBox="0 0 850 430" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg {{ fill: #0d1117; rx: 8px; }}
    .ascii {{ font: 10px 'Courier New', monospace; fill: #58a6ff; white-space: pre; }}
    .title {{ font: bold 13px 'Courier New', monospace; fill: #58a6ff; }}
    .white {{ font: 12px 'Courier New', monospace; fill: #c9d1d9; }}
    .green {{ font: bold 12px 'Courier New', monospace; fill: #3fb950; }}
    .blue {{ font: 12px 'Courier New', monospace; fill: #58a6ff; }}
    .orange {{ font: 12px 'Courier New', monospace; fill: #d29922; }}
    .red {{ font: 12px 'Courier New', monospace; fill: #f85149; }}
    .line {{ font: 12px 'Courier New', monospace; fill: #30363d; }}
  </style>
  <rect width="100%" height="100%" class="bg" />
  
  <!-- ARTE ASCII DA FOTO DE PERFIL REAL -->
  <g>
{ascii_lines_html}  </g>

  <!-- PAINEL DE INFORMAÇÕES ALINHADO À DIREITA -->
  <g transform="translate(350, 0)">
    <text x="0" y="35" class="title">marco@passarela <tspan class="line">------------------------------------</tspan></text>
    
    <text x="0" y="65" class="white">. OS: <tspan class="line">................................</tspan> Windows 11, Linux</text>
    <text x="0" y="85" class="white">. Uptime: <tspan class="line">............................</tspan> 29 anos, 2 meses</text>
    <text x="0" y="105" class="white">. Host: <tspan class="line">..............................</tspan> Software Engineer</text>
    <text x="0" y="125" class="white">. IDE: <tspan class="line">...............................</tspan> VS Code, Cursor AI</text>
    
    <text x="0" y="165" class="blue">. Languages.Programming: <tspan class="line">.....</tspan> <tspan class="white">JavaScript, Python, TypeScript, C#</tspan></text>
    <text x="0" y="185" class="blue">. Languages.Computer: <tspan class="line">........</tspan> <tspan class="white">HTML, CSS, JSON, Markdown, YAML</tspan></text>
    <text x="0" y="205" class="blue">. Languages.Real: <tspan class="line">............</tspan> <tspan class="white">Português, English</tspan></text>
    
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
