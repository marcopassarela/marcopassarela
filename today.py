import os
import re
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
    
    return {
        "repos": data["repositories"]["totalCount"],
        "stars": sum(repo["stargazerCount"] for repo in data["repositories"]["nodes"]),
        "commits": data["contributionsCollection"]["totalCommitContributions"],
        "followers": data["followers"]["totalCount"]
    }

def update_readme():
    stats = get_stats()
    print(f"Estatísticas coletadas: {stats}")

    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(r"<!-- REPOS -->\d+", f"<!-- REPOS -->{stats['repos']}", content)
        content = re.sub(r"<!-- STARS -->\d+", f"<!-- STARS -->{stats['stars']}", content)
        content = re.sub(r"<!-- COMMITS -->\d+", f"<!-- COMMITS -->{stats['commits']}", content)
        content = re.sub(r"<!-- FOLLOWERS -->\d+", f"<!-- FOLLOWERS -->{stats['followers']}", content)

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    update_readme()
