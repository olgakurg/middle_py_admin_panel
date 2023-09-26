SELECT "content"."film_work"."id", 
"content"."film_work"."created", 
"content"."film_work"."modified", 
"content"."film_work"."title", 
"content"."film_work"."description", 
"content"."film_work"."creation_date", 
"content"."film_work"."rating", 
"content"."film_work"."type", 
COUNT("content"."person_film_work"."person_id") AS "actors" 
FROM
    "content"."film_work" INNER JOIN "content"."person_film_work" 
                                ON ("content"."film_work"."id" = "content"."person_film_work"."film_work_id") 
WHERE UPPER("content"."person_film_work"."role"::text) LIKE UPPER(%a%) 
GROUP BY "content"."film_work"."id"



SELECT 
  "content"."film_work"."id", 
  "content"."film_work"."created", 
  "content"."film_work"."modified", 
  "content"."film_work"."title", 
  "content"."film_work"."description", 
  "content"."film_work"."creation_date", 
  "content"."film_work"."rating", 
  "content"."film_work"."type", 
  COUNT(
    "content"."person_film_work"."person_id"
  ) AS "actors" 
FROM 
  "content"."film_work" 
  INNER JOIN "content"."person_film_work" ON (
    "content"."film_work"."id" = "content"."person_film_work"."film_work_id"
  ) 
WHERE 
  UPPER(
    "content"."person_film_work"."role" :: text
  ) LIKE UPPER(% a %) 
GROUP BY 
  "content"."film_work"."id"
