def param_options():
    filter_fields = [{"Name": "Tina"}]
    date_range = ["2022-12-10", "2022-12-18"]

    terms = ""
    for term in filter_fields:
        for key, value in term.items():
            if isinstance(value, list):
                s = tuple([j for j in value])
                terms += f"{key} IN {s} AND "
            else:
                terms += f"{key} IN ('{value}') AND "
        
    terms += f" DATE BETWEEN '{date_range[0]}' AND '{date_range[1]}'"

    return terms