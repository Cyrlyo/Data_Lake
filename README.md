## Preface
Minimum config: 16 Go of RAM

Recommanded config: 32 Go of RAM

Below 16 Go of RAM script will be very slow but it works.

For MongoDB imports you need to have installed mongoimport on your device!
An alternative exists in the script but it takes a huge amount of time.


## Instructions for running the script

Create an 3.9 python virtual environment using `python3.9 -m venv "venv_name"`. <br>
Activate your virtual environement, for Windows users use `./"venv_name"/Scripts/activate`. <br>
Download all required packages using *requirements.txt* file and this command `pip3 install -r requirements.txt`<br>
Make sur that MariaDB, MongoDB, Elastichsearch and Kibana are currently running on your computer.


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

### Launchs arguments exampes:

- `python main.py`: will execute all the code on *demo mode* (doesn't import data en elk)
- `python main.py`: will execute all the code on *demo mode* (import data en elk)
- `python main.py --demo`: will execute all the code (it takes about 1h30 in total)
- `python main.py -a -d -o -f`: will download, format and import the datas on MariaDB & MongoDB
- `python main.py -a --data_prep --demo`: will format data on MongoDB. This is one of the longest parts. We advise you not to do it if you only want to use the data on elasticsearch. The *posts_details_reduced* collection already has the data in the right format.
- `python main.py -a --enable_merge --sample 1000000 --demo`: Will merge 1,000,000 documents from the 3 collections *posts*, *profile*, *location* of the *Instagram* database. Requires downloading, formatting, importing and preparing the data on MongoDB.

### Launch options detailed:

Here are all the possible launch options and their usage:

- Download data only: `python file.py -a -d`
- Import data into MariaDB database only: `python file.py -a -i`
- Import data into MongoDB database only: `python file.py -a -m`
- Import data into both MariaDB and MongoDB databases: `python file.py -a -o`
- Format data (convert from CSV to JSON): `python file.py -a -f`
- Use Python loader to import data into MongoDB: `python file.py -a -p`
- Prepare Instagram data in MongoDB: `python file.py -a --data_prep`
- Prepare only a part of the data (full runtime: approximately 1 hour): `python file.py -a --quick_prep`
- Merge only data collections during preparation: `python file.py -a --only_merge`
- Enable merge of collections during data preparation: `python file.py -a --enable_merge`
- Prepare a sample of data with a specific number of documents: `python file.py -a --sample NUMBER (replace NUMBER with the desired number of documents)`
The options `-a`, `-d`, `-i`, `-m`, and `-o` are mutually exclusive and cannot be used together. The options `-f`, `-p`, `--data_prep`, `--quick_prep`, `--only_merge`, `--enable_merge`, and `--sample` can be used with the -a option. The `-a` option is required to use all of these options except for `--elk`.


## Miscellaneous infos

Software: 
- Python version: 3.9
- MariaDB version: 10.5
- Mongo shell version: 5.0
- Mongo server version: 5.0
- elasticsearch version: 8.4
- kibana version: 8.4
- Ubuntu 18.04 (WLS)
- Windows 10

Hardware: 
- CPU i7 6500U 2.5GHz, 16 Go RAM
- CPU i7 7700 3.6GHz, 32 Go RAM, GPU GTX 1050
- Ryzen 7 5800X 3.8GHz, 32 Go RAM, GPU RTX 3070 Ti

-----------------------------------------------------

Code by: Marin Mainka