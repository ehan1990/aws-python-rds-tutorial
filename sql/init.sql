#
# TABLE STRUCTURE FOR: wallstreet
#

DROP DATABASE IF EXISTS wallstreet;
CREATE DATABASE wallstreet;
USE wallstreet;

DROP TABLE IF EXISTS stocks;

CREATE TABLE stocks (
    ticker varchar(100) NOT NULL,
    name varchar(100) NOT NULL,
    PRIMARY KEY (ticker)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
