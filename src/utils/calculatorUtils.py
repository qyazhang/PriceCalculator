import json

def getCurrencyRate():
    with open("./resource/currency.json", "r") as currency_file:
        currency_text = currency_file.read()
        currency_data = json.loads(currency_text)

    with open("./resource/config.json", "r") as config_file:
        config_text = config_file.read()
        config_data = json.loads(config_text)
        key = config_data["fixer"]["key"]

    last_modify_time = currency_data["lastModifyTime"]
    current_time = time.time()
    if (float(current_time) - float(last_modify_time) > 3600):
        currency_data["lastModifyTime"] = current_time

        currency_response = requests.get(
            'http://data.fixer.io/api/latest?access_key=' + key + '&format=1')
        currency_res = currency_response.json()
        print(currency_res)
        if (currency_res["success"] == False):
            print("error to update currency")
        else:
            currency_data["data"] = currency_res
            with open("./resource/currency.json", "w") as currency_file:
                json.dump(currency_data, currency_file)

    jpy_currency = currency_data["data"]["rates"]["JPY"]
    cny_currency = currency_data["data"]["rates"]["CNY"]
    original_rate = 100 / (jpy_currency / cny_currency)
    pay_rate = round(original_rate + 0.8, 1)
    return pay_rate