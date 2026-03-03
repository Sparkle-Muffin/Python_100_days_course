from pathlib import Path
import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent
movies_file_path = BASE_DIR / "movies.txt"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0"
}
response = requests.get(
    "https://www.empireonline.com/movies/features/best-movies-2/",
    headers=headers,
    timeout=10
)
website = response.text

soup = BeautifulSoup(website, "html.parser")
movies = soup.select("span.content_content__i0P3p h2 strong")

movie_list = []
for m in movies:
    movie = str(m.get_text())
    if ")" in movie:
        movie_list.append(movie)

movie_list = movie_list[::-1]
movie_string = "\n".join(movie_list)
movie_string = movie_string.strip()
with open(movies_file_path, mode="w") as file:
    file.write(movie_string)