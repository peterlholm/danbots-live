# danbots-live
Danbots Live site for controling scannings etc

The following fixtures initiate a new db

demo.json:

## Users

danbots/Danwand1: Django admin
sysadm/Sysa1111: general system administration
clinicadm1/Clin1111: a administrator at the clinic
dentist1/Dent1111: a dentist

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
