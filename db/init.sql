CREATE DATABASE IF NOT EXISTS pubmed CHARACTER SET utf8 COLLATE utf8_general_ci;
USE pubmed;
CREATE TABLE Articles(Id INT PRIMARY KEY, Title TEXT, Keywords TEXT, Abstract TEXT, DateArticle DATE, DateSave DATE, FULLTEXT (Abstract), FULLTEXT (Title));
DELIMITER $$
CREATE PROCEDURE `insertarticle` (IN artid INT, IN arttitle TEXT, IN artkeywords TEXT, IN artabstract TEXT, IN artdate DATE)
BEGIN
   INSERT IGNORE INTO Articles(Id, Title, Keywords, Abstract, DateArticle)
   VALUES
      (
         artid, arttitle, artkeywords, artabstract, artdate
      );
END;
$$
DELIMITER $$
CREATE PROCEDURE `getarticle` (IN artword VARCHAR(255), IN artdatebefore DATE, IN artdateafter DATE)
BEGIN
   SELECT
      *
   FROM
      Articles
   WHERE artword LIKE CONCAT('%', Abstract , '%');
END;
$$