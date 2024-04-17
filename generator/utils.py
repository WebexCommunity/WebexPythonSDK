from typing import Union
from exceptions import ActionNotFoundError, PropertyNotFoundError


def create_property_struct_from_entry(
    prop: Union[str, dict], prop_mapping: dict, is_optional: bool = False
) -> dict:
    if isinstance(prop, str):
        if prop not in prop_mapping.keys():
            raise PropertyNotFoundError(
                f"Simple property {prop} is not part of the objects "
                f"properties. Add it or specify it as a dict."
            )

        tmp = prop_mapping.get(prop).copy()
        tmp["optional"] = is_optional

        return tmp
    elif isinstance(prop, dict):
        # ToDo: Add check that all required properties are present
        tmp = prop.copy()
        tmp["optional"] = is_optional

        return tmp


def get_additional_parameters(descr: dict, action_key: str):
    # Create property mapping of parameters included in the list
    prop_mapping = {}
    for prop in descr["list"]["properties"]:
        prop_mapping[prop["name"]] = prop

    # Find all additional parameters that are not included in prop mapping
    if action_key not in descr.keys():
        raise ActionNotFoundError(
            f"'{action_key}' is missing from your description file"
        )

    addt_parameters = []

    for p in descr.get(action_key).get("required", []):
        addt_param = create_property_struct_from_entry(p, prop_mapping, False)
        addt_parameters.append(addt_param)

    for p in descr.get(action_key).get("optional", []):
        addt_param = create_property_struct_from_entry(p, prop_mapping, True)
        addt_parameters.append(addt_param)

    return addt_parameters
