### MySQL Connection to Python and Creating DB with Scraping Top 250 Movies Page on IMDB

 - Scrap the page with BeautifulSoup and insert the data into Database
 - Making queries on MySQL Workbench
 - Making queries with Pandas package on Python
 - Load MySQL database tables into Pandas dataframe 
 - EDA and visualization with Matplotlib 

### Web Scraping

Using BeautifulSoup package to scrape top 250 movies and got the following:

 - Movie ID
 - Movie Title
 - Release Year
 - Run Time
 - Genre
 - Rating
 - Director and Actors
 - Votes
 - Gross
 
### Data Cleaning
 
After scraping the data, it needed to clean up so that it was usable for our model. Following changes made:
 
  - Some values in Year column scrapped as string values so converted to integer.
  - Run Time values scrapped as 'xxx min' so dropped the 'min' then converted to integer.
  - Actors and Genre column values scraped as one raw string so values splitted.
  - Gross column also stored as string and some string values like 'mil' so dropped the string values<br>
    then converted to integer.
    
### EDA

Below are few highlights from analysis.

<img src="https://github.com/oneofthemdata/MySQL-Python-Web-Scraping/blob/main/images/Box%20Office%20Total%20by%20Genre.png" width="500" height="300">
<img src="https://github.com/oneofthemdata/MySQL-Python-Web-Scraping/blob/main/images/Top%2020%20Directors%20by%20Their%20Movies'%20Gross%20Total.png" width="500" height="300">

### ER Diagram

  ![](https://github.com/oneofthemdata/MySQL-Python-Web-Scraping/blob/main/images/ER%20Diagram.png)
  
  
