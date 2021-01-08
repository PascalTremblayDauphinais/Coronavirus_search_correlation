from new_cases import get_countries


def sort_countries(dcountries):
    lcountries = []
    for ele in dcountries:
        lcountries.append(ele)
    return sorted(lcountries)


print(sort_countries(get_countries()))
