CREATE ROLE ravindu WITH LOGIN PASSWORD 'ravi';
CREATE DATABASE smartgrader WITH OWNER = ravindu;
GRANT ALL PRIVILEGES ON DATABASE smartgrader TO ravindu;

/* registered users watch*/
SELECT * FROM auth_user;

GRANT CREATE ON DATABASE smartgrader TO ravindu;