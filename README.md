# Running this project


TO run this project you need to have a postgres table called `test_table` containing mocked production values of real data. You also need create a json file inside the connector folder named `config.json` that contains your database connection configuration.
Here is a simple one:
`{
  "local": {
    "dbName": "postgres",
    "user": "postgres",
    "password": "somepassword",
    "host": "127.0.0.1",
    "port": 5432
  }
}`
Once this has been created you can run `code.py`

Alternatively you can do the following below which does not require a database instance as it is simulated in the file system.

To run this project you need to create a folder called `test_data`.
After this folder has been created run the following command `python3 test.py`


# What is this code doing.

Initially this repo was mean to be a place for helper python functions and thus the name.
It has now become the home of the `z_score` distribution of energy per mileage values.
What the code does, is calculate the `mileage until maintance`from the calculated `z_scores`.
Currently the `z_scores` are calculated from random generated data. In the future real data will be used.

### Code in depth

The `test.py` file has two main functions. The `logic` and `main` functions.
The `main` class will call the `helpers/start.py` file and generate an initial set of random data. This data, is currently being simulated. A simple database mock was created, by saving those entries from memory to disk in the file `__test__.json` located inside the `test_data/` folder. It is important to create this empty folder before running this program, else the script will be unaware of where to save the file.
If streaming data is wished to be simulated, line 82 `asyncio.ensure_future...` can be uncommented. This will periodically (depending on the values of the variables set) read and add new data to the `__test__.json` file.

The code will then generate random data and calculate the `z_scores` from this data. It will then calculate the `mileage until maintance`from the calculated `z_scores`. I left many commented out print statements inside the `logic` function as examples of the data that can be generated, calculated and printed to the console.

### Maintainers
[Naragod](https://www.github.com/naragod)