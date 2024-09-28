USE `fishing` ;

SELECT * FROM moon ORDER BY date DESC;
SELECT * FROM sun ORDER BY date DESC;
SELECT * FROM tide ORDER BY date DESC;
SELECT * FROM rainfall ORDER BY date DESC;
SELECT * FROM rainfall_possibility ORDER BY date DESC;
SELECT * FROM swell ORDER BY date DESC;
SELECT * FROM wind ORDER BY date DESC;
SELECT * FROM temperature ORDER BY date DESC;

-- DELETE FROM moon WHERE date >= '2024-09-28';
-- DELETE FROM sun WHERE date >= '2024-09-28';
-- DELETE FROM tide WHERE date >= '2024-09-28';
-- DELETE FROM rainfall WHERE date >= '2024-09-28';
-- DELETE FROM rainfall_possibility WHERE date >= '2024-09-28';
-- DELETE FROM swell WHERE date >= '2024-09-28';
-- DELETE FROM wind WHERE date >= '2024-09-28';
-- DELETE FROM temperature WHERE date >= '2024-09-28';
