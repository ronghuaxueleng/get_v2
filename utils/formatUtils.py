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
    filtered_rules = list()
    proxies_md5_dict = dict()
    proxies_md5_name_dict = dict()
    proxy_names_set = set()
    proxy_group_names = set()
    proxy_groups_test_set = set()
    proxy_groups = dict()

    with open("template.json", "r", encoding="utf8") as template_file:
        template = json.load(template_file)

    rules = yaml_obj.get("rules")
    proxies = yaml_obj.get("proxies")
    filtered_rules.extend(rules)
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
    template_proxy_groups = yaml_obj.get("proxy-groups")

    for index, group in enumerate(template_proxy_groups):
        group_name = group.get("name")
        proxy_group_names.add(group_name)
        if group.get("type") == "url-test":
            proxy_groups_test_set.add(group_name)
            group["name"] = "♻️ 自动选择"
            template_proxy_groups[index] = group

    for group in template_proxy_groups:
        group_name = group.get("name")
        proxy_group_names.add(group_name)
        saved_group = proxy_groups.get(group_name, dict())
        saved_proxies = saved_group.get("proxies", list())
        proxies = group.get("proxies")
        for proxy in proxies:
            if (
                    proxy not in saved_proxies
                    and proxy in proxy_names_set
            ):
                for one in proxy_groups_test_set:
                    proxy = proxy.replace(one, "♻️ 自动选择")
                saved_proxies.append(
                    merged_proxy.get(proxy, proxy)
                )
        group["proxies"] = (
            saved_proxies
            if len(saved_proxies) > 0
            else ["DIRECT", "REJECT"]
        )
        proxy_groups[group_name] = group

    if len(proxy_groups) > 0:
        template["proxy-groups"] = list(proxy_groups.values())

    filtered_rules_set = set()
    for item in filtered_rules:
        for one_group in proxy_group_names:
            if one_group in item:
                filtered_rules_set.add(item)
        for one in proxy_groups_test_set:
            filtered_rules_set.add(item.replace(one, "♻️ 自动选择"))

    template["proxies"] = list(proxies_md5_dict.values())
    template["rules"] = list(filtered_rules_set)

    return template
