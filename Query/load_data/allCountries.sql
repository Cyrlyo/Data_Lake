CREATE TABLE allcountries(geonameid BIGINT NOT NULL UNIQUE PRIMARY KEY,
name VARCHAR(200) COLLATE utf8_general_ci, asciiname VARCHAR(200), slug VARCHAR(10000),
lat FLOAT, lng FLOAT, feature_class CHAR(1), feature_code VARCHAR(10), cd VARCHAR(255),
cc2 VARCHAR(255), admin1_code VARCHAR(20), admin2_code VARCHAR(80), admin3_code VARCHAR(20), admin4_code VARCHAR(20),
population BIGINT, elevation FLOAT, dem INT, timezone VARCHAR(40), modification_date DATE);
