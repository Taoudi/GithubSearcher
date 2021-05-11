import os
import re

from github import Github


class GithubScraper:
    def __init__(self, token, filename="javaurls"):
        self.g = Github(token)
        self.filename = filename

    def get_content(self, repo, path):
        contents = repo.get_contents(path)
        for content in contents:
            if content.type == 'dir':
                contents.extend(repo.get_contents(content.path))

            elif content.type == 'file':
                if re.match(r'^.*\.java$', content.name):
                    if os.path.exists(self.filename):
                        append_write = 'a'  # append if already exists
                    else:
                        append_write = 'w'  # make a new file if not
                    f = open(self.filename, append_write)
                    f.write(content.download_url + '\n')
                    f.close()
                    print(content.download_url)

    def get_repos_by_uname(self, username):
        user = self.g.get_user(username)
        avatar = user.avatar_url
        for repo in user.get_repos():
            print(repo)
            try:
                self.get_content(repo, "")
            except Exception as e:
                print(e)

    def mass_search(self):
        repos = self.g.search_repositories(query='language:java, created:>=2021-01-01')
        for repo in repos:
            print(repo)
            print(repo.owner)
            self.get_content(repo, "")


if __name__ == "__main__":
    f = open("credentials", "r")
    git = GithubScraper(f.readline(), filename="javaurls6")
    git.mass_search()
