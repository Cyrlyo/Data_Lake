Minimum config: 16 Go of RAM

Recommanded config: 32 Go of RAM

Below 16 Go of RAM script will be very slow but it works.

For MongoDB imports you need to have installed mongoimport on your device!
An alternative exists in the script but it takes a huge amount of time.

## Launchs arguments & options
- -h, --help            : show this help message and exit
- -a, --init_manually   : Download data & import them on databaes
- -d, --download        : Only download data
- -i, --maria_import    : Only import datas on MariaDB database
- -m, --mongo_import    : Only import data on MongoDB database
- -o, --database_import : Import on MariaDB & MongoDB
- -f, --format_data     : Format data (csv to json)
- -p, --python_loader   : Use python loader for MongoDB datas. USE ONLY IF NECESSARY! IT'S VERY LONG! About 30 min to 1 hour per document!
- --data_prep           : Prepare instagram data on MongoDB
- --quick_prep          : Only prepare some data (full takes 1h to run)
- --only_merge          : Only merge collections as data preparation
- --enable_merge        : Enable merge collections while preparing datas
- --sample SAMPLE       : Number of document to merge
- --demo                : Disable demo mode
- --elk                 : Only import on elk