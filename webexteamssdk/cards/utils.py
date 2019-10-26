def set_if_not_none(property_name, property, export):
    if property is not None:
        export[property_name] = property.to_dict()
