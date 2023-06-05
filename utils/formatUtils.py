import copy
import hashlib
import json
import time
import uuid

from ruamel import yaml


def reset_yaml_file(yaml_path):
    with open(yaml_path, "r", encoding="utf8") as yaml_file:
        yaml_obj = yaml.safe_load(yaml_file)
        return reset_yaml_content(yaml_obj)


def reset_yaml_stream(yaml_stream):
    try:
        yaml_obj = yaml.safe_load(bytes(yaml_stream))
        return reset_yaml_content(yaml_obj)
    except Exception as e:
        print(e)


def reset_yaml_content(yaml_obj):
    proxies_md5_dict = dict()
    proxies_md5_name_dict = dict()
    proxy_names_set = set()

    with open("template.json", "r", encoding="utf8") as template_file:
        template = json.load(template_file)

    proxies = yaml_obj.get("proxies")
    merged_proxy = dict()
    for proxy in proxies:
        proxy["port"] = int(proxy.get("port"))
        proxy_copy = copy.deepcopy(proxy)
        proxy_copy.pop("name")
        data_md5 = hashlib.md5(
            json.dumps(proxy_copy, sort_keys=True).encode(
                "utf-8"
            )
        ).hexdigest()
        if data_md5 not in proxies_md5_dict:
            if proxy.get("name") in proxy_names_set:
                proxy["name"] = (
                        proxy.get("name")
                        + "_"
                        + str(round(time.time() * 1000))
                        + str(uuid.uuid4())
                )
            proxy_names_set.add(proxy.get("name"))
            proxies_md5_dict[data_md5] = proxy
            proxies_md5_name_dict[
                data_md5
            ] = proxy.get("name")
        merged_proxy[
            proxy.get("name")
        ] = proxies_md5_name_dict.get(data_md5)

    template_proxy_groups = template.get("proxy-groups")

    proxy_groups = dict()
    for group in template_proxy_groups:
        group_name = group.get("name")
        if group_name == 'URL-TEST' or group_name == 'LOAD-BALANCE' or group_name == 'SELECT':
            group["proxies"] = list(proxies_md5_dict.values())
        proxy_groups[group_name] = group

    if len(proxy_groups) > 0:
        template["proxy-groups"] = list(proxy_groups.values())

    template["proxies"] = list(proxies_md5_dict.values())

    return template
