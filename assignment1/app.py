from flask import Flask
from github import Github
from flask import abort
from sys import argv
from base64 import b64decode
from json import dumps
from yaml import load

app = Flask(__name__)
repo = ""

@app.route("/")
def dummy():
    return r.size # should always be 1

@app.route("/v1/<filename>")
def retrieve(filename):
    if filename.endswith("yml"):
        content = get_content(filename)
        print filename
        
        if content:
            return content
        else:
            abort(404)
    elif filename.endswith("json"):
        filename = filename[:-5] + ".yml"
        print "json filename changed to {}".format(filename)
        content = get_content(filename)
        print "Retrieved content is {}".format(content)
        if content :
            return dumps(load(content))
        else:
            abort(404)
    else:
        abort(404)

def get_content(filename):
    filelist = r.get_file_contents("/")
    for file in filelist:
        if file.name == filename:
            return "{}".format(b64decode(r.get_file_contents(filename).content))
    return None

if __name__ == "__main__":
    path = argv[1]
    site = "github.com"
    i = path.find(site)
    if i >= 0:
        i += len(site) + 1
        repo = path[i:]
        g = Github()
        r = g.get_repo(repo)
        try:
            s = r.size
            if s > 0:
                app.run(debug=True,host='0.0.0.0')
        except Exception as e:
            print "Error loading repo: {}".format(e)
    else:
        print "Only github.com supported"
