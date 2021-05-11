import urllib.request
from pathlib import Path


class Converter:


    def get_urls(self, filename="urls/javaurls6"):
        ##Pulling the urls from url file
        urls = []
        with open(filename, 'r') as fp:
            for url in fp:
                urls.append(url)
        return urls

    def convert_everything(self):
        urls = self.get_urls() 
        print(len(urls), "urls")
        for i,url in enumerate(urls):
            if i%100 == 0:
                print(i)
            try:
                self.url_to_file(url)
            except urllib.error.HTTPError:
                print("HTTP ERROR", url)
                continue
            except UnicodeDecodeError:
                print("UNICODEDECODEERROR", url)
                continue
            except UnicodeEncodeError:
                print("UNICODEENCODEERROR", url)
                continue


        
    def url_to_file(self,url):
        response = urllib.request.urlopen(url)
        code = response.read().decode("utf-8")
        clean_url = url.split(".com/")[1]
        #part_url = clean_url.split("/")
        #username = part_url[0]
        #repo = part_url[1]
        clean_url = clean_url.replace("/",'').replace("\n",'').replace(".java","")
        #javafilename = part_url[len(part_url) - 1].replace(".java", "")
        #javafilename = javafilename.replace("\n","")
        #print(clean_url)
        while True:
            my_file = Path("data/"+clean_url)
            if my_file.is_file():
                clean_url+='1'
                print(clean_url)
            else: 
                break

        with open("data/"+clean_url,'w') as fp:
            fp.write(url)
            fp.write(code)


if __name__ == "__main__":
    conv = Converter()
    conv.convert_everything()