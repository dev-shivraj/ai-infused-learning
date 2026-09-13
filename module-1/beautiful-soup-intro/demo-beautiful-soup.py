from bs4 import BeautifulSoup

html = """
<html>
  <body>
    <h1>My Website</h1>
    <p>Hello Shivraj</p>
    <p>Welcome to my website</p>
  </body>
</html>
"""


# soup = BeautifulSoup(html, "html.parser")
soup = BeautifulSoup(html, "html.parser")
print(soup.h1.text)


