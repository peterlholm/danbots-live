# danbots-live
Danbots Live site for controling scannings etc

The following fixtures initiate a new db

sysuser.json:

sysadm: general system administration
clinicadm1: a administrator at the clinic
dentist1/Danbots1: a dentist

peter: superuser



groups:

sysadm: general administrators
clinicadm: local administrators

installation:

1. make folder
2. make venv
3. clone project
4. chown www-data
5. chgrp peter db.sqlite3
6. make migrations, migrate
7. 
