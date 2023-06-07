import csv
import time

import requests
from bs4 import BeautifulSoup

#allows the user to enter a desired tag for quotes
enter_tag = input("Tag: ")

#checks whether the tag is valid or not
if not enter_tag[0].isalpha() or not enter_tag[-1].isalpha() or "_" in enter_tag:
    print("Invalid Tag")
else:
    enter_tag = enter_tag.replace(" ", '-')
    url = f"http://quotes.toscrape.com/tag/{enter_tag}"
    page = requests.get(url)
    
    if page.status_code != 200:
        print(f"Error {page.status_code}")
    else:
        soup = BeautifulSoup(page.content, "html.parser")
        all_quote = soup.find_all("span", class_="text")
        all_author = soup.find_all("small", class_="author")
        quotes = [quote.text for quote in all_quote]
        authors = [author.text for author in all_author]
        
        #checks if there is a next page
        next_page = soup.find("li", class_="next")

        while next_page:
            # makes a delay to avoid overwhelming the server.
            time.sleep(50)
            
            href = next_page.find("a")["href"]
            url = f"http://quotes.toscrape.com/{href}"
            page = requests.get(url)
            if page.status_code != 200:
                print(f"Error {page.status_code}")
                break
            soup = BeautifulSoup(page.content, "html.parser")
            all_quote_next = soup.find_all("span", class_="text")
            all_author_next = soup.find_all("small", class_="author")
            for quote_next in all_quote_next:
                quotes.append(quote_next.text)
            for author_next in all_author_next:
                authors.append(author_next.text)
            next_page = soup.find("li", class_="next")
          
        #checks if the provided tag has information or not
        if not quotes and not authors:
            print(f"No quotes were found for the tag: {enter_tag}")
        else:
            #creates a CSV file to write appropiate quoutes and authors
            with open(f"{enter_tag}_quotes.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Quote", "Author"])
                writer.writerows(zip(quotes, authors))
                print("CSV file successfully created")
