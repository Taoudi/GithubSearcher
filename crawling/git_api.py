import requests, re
from github import Github

"""
 for p in content.path.split("\n"):
                    ##print(p)
                    #new_path = path + "\\" + p
                    #print(new_path)
                    #contents.extend(repo.get_contents(file_content.path))
                    #self.get_content(repo,new_path)"""

class GithubScraper:
    def __init__(self,token):
        self.g = Github(token)



    def get_content(self,repo,path):
        contents = repo.get_contents(path)
        for content in contents:
            if content.type == 'dir':
                contents.extend(repo.get_contents(content.path))
               
            elif content.type == 'file':
                if  re.match(r'^.*\.java$',content.name):
                    print(content)
                    #print(content.decoded_content)

    def get_repos(self, username):
        url = f"https://api.github.com/users/{username}"
        #user_data = requests.get(url).json()
        #print(user_data['avatar_url'])

        user = self.g.get_user(username)
        avatar = user.avatar_url
        for repo in user.get_repos():
            print(repo)
            try: 
               self.get_content(repo,"")
            except Exception as e:
                print("Empty Repository")
                print(e)

            print("-------------------------------")



if __name__ == "__main__":
    f = open("credentials", "r")
    git = GithubScraper(f.readline())
    git.get_repos("Taoudi")




    #for i, repo in enumerate(g.search_repositories("language:python")):
    #    print(repo)