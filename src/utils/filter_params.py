def param_options(ranges: list, filters: list = None) -> str:
    # create filter param string
    terms = ""
    if filters is not None:
        for term in filters:
            for key, value in term.items():
                if isinstance(value, list):
                    s = tuple([j for j in value])
                    terms += f"{key} IN {s} AND "
                else:
                    terms += f"{key} IN ('{value}') AND "
        
    terms += f" DATE BETWEEN '{ranges[0]}' AND '{ranges[1]}'"

    return terms