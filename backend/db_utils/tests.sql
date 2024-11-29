SELECT * FROM Listing WHERE price < 50 AND price > 40



SELECT * FROM User
SELECT * FROM UserFavoriteListing

DELETE FROM USER


SELECT l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at,
GROUP_CONCAT(t.name) AS tags
FROM Listing l
LEFT JOIN ListingTag lt ON l.id = lt.listing_id
LEFT JOIN Tag t ON lt.tag_id = t.id
WHERE 1=1 --AND condition = "Fair"
--AND title LIKE "%textbook%" AND t.name LIKE "%Math%"
GROUP BY l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at
order by price ASC;