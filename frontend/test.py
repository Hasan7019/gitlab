import urllib.request

url = "https://job-board.dexignzone.com/xhtml/jobs-my-resume.html"

response = urllib.request.urlopen(url)
html = response.read().decode('utf8')

print(html)