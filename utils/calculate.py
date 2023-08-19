from pymongo import MongoClient
import os
client = MongoClient(os.getenv("MONGO_DB_URI"))
db = client["Insurance"]
collection = db["Data"]

def premium_calculator(age_list,city_tier,sum_insured,tenure):
    rates = []
    age_list.sort()
    for age in age_list:
        data = collection.find_one(
            {},
            {
                f"tier_id.{city_tier}.sum_insured.{sum_insured}.tenure.{tenure}.age_rate.{age}": 1
            },
        )
        rate = data["tier_id"][f"{city_tier}"]["sum_insured"][f"{sum_insured}"]["tenure"][f"{tenure}"]["age_rate"][f"{age}"]["rate"]
        rates.append(int(rate))
    premium = 0
    for i in range(len(rates) - 1):
        rates[i] = rates[i] / 2
    for rate in rates:
        premium += rate
    return premium