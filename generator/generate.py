import os
import yaml
import argparse

from jinja2 import Environment, FileSystemLoader

from utils import get_additional_parameters
from exceptions import MissingKeyError


def render_prop_mixin(
    env: Environment,
    name: str,
    properties: list,
    base_name: str,
    template_name: str = "mixins.py",
    path_prefix: str = "../webexteamssdk/models/mixins/",
) -> str:
    """Renders a simple property mixin for the SDK based on the
        information provided in the descriptor file.

    Args:
        env(Environment): The jinja environment to render under. Defines
            the templates that will be used.
        name(str): The name of our endpoint. Will be turned into the class
            name as {name}SimplePropertyMixin.
        properties(list): List of property extracted from the list.properties
            key in the descriptor file.
        base_name(str): Base name of the descriptor file. Used to generate
            the filenames.
        template_name(str): Name of the template to use. Default: mixins.py
        path_prefix(str): Path to the mixins folder.
            Default: ../webexteamssdk/models/mixins/

    Returns:
        str: Path to the generated
    """

    # Render template based on loaded properties
    tmpl = env.get_template(template_name)
    out = tmpl.render(name=name, properties=properties)

    target_path = os.path.join(path_prefix, f"{base_name}.py")

    with open(target_path, "w") as fh:
        fh.writelines(out)

    return target_path


def render_api_class(
    env: Environment,
    descr: dict,
    base_name: str,
    template_name: str = "api.py",
    path_prefix: str = "../webexteamssdk/api/",
) -> str:
    """Renders an API class based on the properties described in
        the descr file.

    Args:
        env(Environment): The jinja environment to render under. Defines
            the templates that will be used.
        descr(dict): Descriptor parsed from the yaml file defining the
            properties of the endpoint and target api model.
        base_name(str): Base name of the descriptor file. Used to generate
            the filenames.
        template_name(str): Name of the template to use. Default: api.py
        path_prefix(str): Path to the target api folder that the output will
            we placed in. Default: ../webexteamssdk/api/

    Returns:
        str: The path to the generated api class
    """
    create_parameters = get_additional_parameters(descr, "create")
    update_parameters = get_additional_parameters(descr, "update")

    additional_code = descr.get("additional_code", None)

    # Render template
    tpl = env.get_template(template_name)
    out = tpl.render(
        name=descr['name'],
        endpoint=descr['endpoint'],
        object_type=descr['object_type'],
        url_parameters=descr['url_parameters'],
        query_parameters=descr['query_parameters'],
        create_parameters=create_parameters,
        update_parameters=update_parameters,
        methods=descr['methods'],
        additional_code=additional_code,
    )

    target_path = os.path.join(path_prefix, f"{base_name}.py")

    with open(target_path, "w") as fh:
        fh.writelines(out)

    return target_path


def main():
    # Setup arg parser
    parser = argparse.ArgumentParser(
        description="Generate new endpoints for the SDK"
    )
    parser.add_argument(
        "-d",
        "--descriptor",
        help="Path to the descriptor .yaml file",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-t",
        "--template_dir",
        help="Path to the templates directory",
        type=str,
        default="templates",
        required=False,
    )
    args = parser.parse_args()

    # Setup jinja environment and load information from description file
    env = Environment(loader=FileSystemLoader(args.template_dir))

    descr_file = args.descriptor
    base_name = os.path.splitext(os.path.basename(descr_file))[0]

    descr = yaml.safe_load(open(descr_file))

    # Check that all required keys are present
    required_keys = [
        "name",
        "list.properties",
        "endpoint",
        "object_type",
        "query_parameters",
        "methods",
    ]

    for key in required_keys:
        # Check all keys - subkeys (i.e. d['list']['properties']
        # can be passed in dot notation, so list.properties)
        keys = key.split(".")

        d = descr
        for sub_key in keys:
            if sub_key not in d.keys():
                raise MissingKeyError(f"Missing required key '{key}'")
            else:
                d = d.get(sub_key)

    # Add empty url_parameters key if there are no URL parameters defined
    if 'url_parameters' not in descr.keys():
        descr['url_parameters'] = []

    mixin_path = render_prop_mixin(
        env=env,
        name=descr["name"],
        properties=descr["list"]["properties"],
        base_name=base_name,
    )
    print(f"Rendered mixin for {descr['name']} to {mixin_path}")

    api_path = render_api_class(env=env, descr=descr, base_name=base_name)
    print(f"Rendered api class for {descr['name']} to {api_path}")


if __name__ == "__main__":
    main()
