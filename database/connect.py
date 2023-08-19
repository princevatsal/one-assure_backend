from pymongo import MongoClient
import csv
import certifi
import os
client = MongoClient(os.getenv("MONGO_DB_URI"),tlsCAFile=certifi.where())
db = client["Insurance"]
collection = db["Data"]


def fillDatabase():
    try:
        csv_file = open("raw_data.csv", "r")
        reader = csv.DictReader(csv_file)
    except Exception as e:
        print(e)
        exit(1)
    jsondata = []
    for row in reader:
        jsondata.append(row)

    data = {}
    i = 0
    
    for row in jsondata:
        tier_id = row["TierID"]
        sum_insured = row["SumInsured"]
        tenure = row["Tenure"]
        age = row["Age"]
        rate = row["Rate"]

        if "tier_id" not in data:
            data["tier_id"] = {}

        if tier_id not in data["tier_id"]:
            data["tier_id"][tier_id] = {}

        if "sum_insured" not in data["tier_id"][tier_id]:
            data["tier_id"][tier_id]["sum_insured"] = {}

        if sum_insured not in data["tier_id"][tier_id]["sum_insured"]:
            data["tier_id"][tier_id]["sum_insured"][sum_insured] = {}

        if "tenure" not in data["tier_id"][tier_id]["sum_insured"][sum_insured]:
            data["tier_id"][tier_id]["sum_insured"][sum_insured]["tenure"] = {}
        if tenure not in data["tier_id"][tier_id]["sum_insured"][sum_insured]["tenure"]:
            data["tier_id"][tier_id]["sum_insured"][sum_insured]["tenure"][tenure] = {}
        if (
            "age_rate"
            not in data["tier_id"][tier_id]["sum_insured"][sum_insured]["tenure"][
                tenure
            ]
        ):
            data["tier_id"][tier_id]["sum_insured"][sum_insured]["tenure"][tenure][
                "age_rate"
            ] = {}
        if (
            age
            not in data["tier_id"][tier_id]["sum_insured"][sum_insured]["tenure"][
                tenure
            ]["age_rate"]
        ):
            data["tier_id"][tier_id]["sum_insured"][sum_insured]["tenure"][tenure][
                "age_rate"
            ][age] = {}
        data["tier_id"][tier_id]["sum_insured"][sum_insured]["tenure"][tenure][
            "age_rate"
        ][age]["rate"] = rate

    try:
        collection.insert_one(data)
    except Exception as e:
        print("Data exists",e)

fillDatabase()