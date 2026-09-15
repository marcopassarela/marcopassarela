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
        "               g@M%@%%@N%Nw, ,",
        "         ,M*|  |*%gNM=]mM%g||%N,",
        "        p!` ` '! |``` '''|||jhlj%w",
        "     ,@L `     ,,        ''!`|j%M]%M",
        "    ]j'` .,wp@pw,      `    '''|%Wg",
        "  /{[|]@@@@@@@@@@pp.           |||||",
        "` ` ']@@@@@@@@@@@@@@p      ,, `",
        " , :]% %@ @@@%%%%%%k%h '*||mkr      *",
        "   j%M`      |jkk'   ~nrn=|i   ;`",
        " !  jrr*^`              `\"!  L'':!",
        " j  lp;;.  ,/ @@    ;;\\nmy \"   ,~",
        "i r @@@@mmHM @@@@ `^*****M*,p ;",
        "| ]@@@@HHH]g@M%%%%%H,jmgpmb%  j",
        " ;;%%%%%k%@[,.n|;.;j%%k|%k%%', [",
        "  H|%%k%%%j%k||,;;j;!!'%ij}]@",
        "  \"djjmkL,\"]] [,,,,wwxw;|#kjk`",
        "    %;%km%%%%M%M|%%jkkii|||[",
        "     kjj%%kkkl!|||||||j|||\"",
        "      |jm%H@@@b%%kkmk%i|!,[",
        "      @p|j%%%%jkk||j*'` ;j[",
        "     ]@@@g|'''~''' `  ,j%k",
        "     @@@@@mgmp;,,,,:;jj%%k%",
        "     @@@@@@@@@%%kgki|jjjj%k%@",
        ". ^['' %@@@@HH%b%k{illljkjj%%%",
        "=[' ` . %HH%%%%%H@gkilljjj%kk%\"."
    ]

    ascii_lines_html = ""
    start_y = 35
    line_height = 15
    for i, line in enumerate(ascii_art):
        escaped_line = html.escape(line).replace(" ", "&#160;")
        y_pos = start_y + (i * line_height)
        ascii_lines_html += f'    <text x="20" y="{y_pos}" class="ascii">{escaped_line}</text>\n'

    svg = f'''<svg fill="none" width="850" height="430" viewBox="0 0 850 430" xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)">
  <style>
    .bg {{ fill: #0d1117; rx: 8px; }}
    .ascii {{ font: 11px 'Courier New', monospace; fill: #58a6ff; white-space: pre; }}
    .title {{ font: bold 13px 'Courier New', monospace; fill: #58a6ff; }}
    .white {{ font: 12px 'Courier New', monospace; fill: #c9d1d9; }}
    .green {{ font: bold 12px 'Courier New', monospace; fill: #3fb950; }}
    .blue {{ font: 12px 'Courier New', monospace; fill: #58a6ff; }}
    .orange {{ font: 12px 'Courier New', monospace; fill: #d29922; }}
    .red {{ font: 12px 'Courier New', monospace; fill: #f85149; }}
    .line {{ font: 12px 'Courier
