CREATE TABLE profiles(
    sid INT NOT NULL UNIQUE PRIMARY KEY,
    profile_id FLOAT not NULL,
    profile_name VARCHAR(255),
    firstname_lastname VARCHAR(255),
    description VARCHAR(30),
    followers INT,
    n_posts INT,
    url VARCHAR(255),
    cts DATETIME2,
    is_business_account BOOLEAN
);