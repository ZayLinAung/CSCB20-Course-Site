CREATE TABLE IF NOT EXISTS "Person" (
        id INTEGER NOT NULL,
        username VARCHAR(20) NOT NULL,
        email VARCHAR(30) NOT NULL,
        password VARCHAR(20) NOT NULL,
        userType VARCHAR(20) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (username),
        UNIQUE (email)
);