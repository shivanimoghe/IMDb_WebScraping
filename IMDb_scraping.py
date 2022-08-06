#Here we would be extracting the top 250 movies of all time from the IMDb website, We basically, would fetch rank, name, year of release and IMDb ratings and transfer it into an Excel file.

# Import the Libraries
from bs4 import BeautifulSoup
import requests
import openpyxl

# Creation of excel file
excel = openpyxl.Workbook()                                                                         
sheet = excel.active                                                                                # to make sure that you are working with the "active" sheet
sheet.title = "Top Rated Movies"                                                                    # Change the title of the active sheet
sheet.append(['Movie Rank', 'Movie Name', 'Year of release', 'Ratings Received'])                   # Column Header


#URL of the website
url = "https://www.imdb.com/chart/top/"

# Code (within try & except block)  

try:
    source = requests.get(url)
    source.raise_for_status                                                                            # If url is incorrect it returns an error
    
    soup = BeautifulSoup(source.text, 'html.parser')                                                   #After receiving all the 'text' present in the website, we now want the tag which consist of movies table
    movies_table = soup.find('tbody', class_ = "lister-list")                                          #through the inspect we got to know that the content we are looking for is in the 'tbody' tag having a class = lister-list
    movies_list = movies_table.find_all('tr')                                                          #since all the contents of movies are present in individual 'tr' tags, we might want to use the find_all function to get the list of all 250 <tr> tags to get the 250 movies.
    
    for movie in movies_list:                                                                         # To get the individual elements from 'movie_list'
        name = movie.find('td', class_ = "titleColumn").a.text                                        # tag details where the name of movie is, "a" returns only the content of a attribute present ".text" returns only the text present within 'that' attribute
        rank = movie.find('td', class_ = "titleColumn").get_text(strip = True).split('.')[0]          # using get_text function because otherwise it'd return rank, name and year in an unorderly way, strip() is used as an argument to make the unnecessary spaces diminish, to get only the rank use split() to split against the dot, it returns list, we only want the rank so write the index [0]
        year = movie.find('td', class_ = "titleColumn").span.text.strip('()')                         # year is in span tag as its text of same td tag, so the same method till there after which to remove parentheses use strip() which removes whatever you mention in its argument
        rating = movie.find('td', class_ = "ratingColumn imdbRating").strong.text                     # identify the tags and write them
        print(rank, name, year, rating)

        sheet.append([rank, name, year, rating])                                                      # After each iteration of the loop the Movies will be uploaded to this sheet.
        
except Exception as e:
    print(e)

excel.save('IMDb Movie Ratings.xlsx')