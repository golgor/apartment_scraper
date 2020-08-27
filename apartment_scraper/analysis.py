import pandas as pd
import copy


def read_data(file):
    return pd.read_csv(file, index_col=0)


def round_values(data, columns):
    data[columns] = round(data[columns])
    return data


def calculate_rent_per_sqm(data):
    data['rent/sqm'] = round(data['rent'] / data['area'], 3)
    return data


def get_size_class(data):
    data['size_class'] = round(data['area'], -1)
    return data


def drop_na_values(data):
    return data.dropna(0)


def main():
    # TODO: Mean/Min/Max/Std price per Bezirk
    raw = read_data("apartments.csv")
    data = copy.deepcopy(raw)
    data = drop_na_values(data)
    data = round_values(data, ["rent", "area", "rooms"])
    data = calculate_rent_per_sqm(data)
    data = get_size_class(data)
    print(data.head())
    print(len(raw))
    data.to_excel("apps.xlsx")


if __name__ == "__main__":
    main()
