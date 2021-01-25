-- 1. How many movies are in top 250 list where made each year over the past 30 years?
SELECT Year, COUNT(*) AS  Number_of_movies
FROM movies
GROUP BY Year
HAVING Year BETWEEN 1990 AND 2020
ORDER BY Year ASC;

-- 2. List all the directors who directed a 'Drama' movie.
SELECT Movie, Director
FROM movies
WHERE Genre LIKE '%Drama%';

-- 3. How many directors are in top 250 movies have directed a movie more than twice?
SELECT Director, COUNT(*) AS Total_Appearance
FROM movies
GROUP BY Director
HAVING COUNT(Director) > 2
ORDER BY Total_Appearance DESC;

-- 4. What is average ratings of Star Wars series?
SELECT ROUND(AVG(reviews.Rating), 3) AS Average_Rating
FROM movies
	INNER JOIN
		reviews ON movies.ID=reviews.movie_id
WHERE Movie LIKE 'Star Wars%';

-- 5. What movie is the highest rating of Lord of the Rings sequel?
SELECT Movie, MAX(Rating) AS Best_of_the_Sequel
FROM movies 
	INNER JOIN
		reviews ON movies.ID=reviews.movie_id
WHERE Movie LIKE 'The Lord of the Rings%';

-- 6. List top 10 highest grossing movies with heir rating and show relase year 
-- on movie column. 	  

SELECT CONCAT(Movie, ' (', Year, ')') AS Movie, Rating, Gross_Total
FROM movies
	INNER JOIN 
		reviews ON movies.id = reviews.movie_id
	INNER JOIN
		gross_total ON reviews.movie_id = gross_total.movie_id
GROUP BY ID
ORDER BY Gross_Total DESC
LIMIT 10;

SELECT * FROM imdbtop250.movies
WHERE Year = (SELECT MIN(Year) FROM movies)
	AND 
	  Year <= (SELECT Year FROM movies WHERE Year <= '1950');

-- 7. Find the movies made from 1950 and 1960. What's their gross total, number of reviews, and ratings?

SELECT Movie, Year, Gross_Total, Total_Rate, Rating
FROM movies
	INNER JOIN 
		reviews ON movies.id = reviews.movie_id
	INNER JOIN
		gross_total ON reviews.movie_id = gross_total.movie_id
WHERE Year BETWEEN 1950 AND 1960 
GROUP BY ID
ORDER BY Year;