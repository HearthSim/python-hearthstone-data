import argparse
import io
import json
import sys
import xml.etree.ElementTree
from typing import Dict, Any, Union
from xml.etree.ElementTree import ElementTree, Element


BLACKLISTED_TAGS = ["FLAVORTEXT", "ARTISTNAME"]


def tag_xml_to_json(tag_xml: Element) -> Dict[str, Any]:
    value: Union[str, Dict[str, str], int, bool]
    tag_type = tag_xml.attrib["type"]

    if tag_type in ["Int", "Card"]:
        value = int(tag_xml.attrib["value"])
    elif tag_type == "LocString":
        value = {t.tag: t.text for t in tag_xml}
    elif tag_type == "String":
        value = tag_xml.text
    else:
        raise ValueError("Unexpected tag type " + tag_type)

    return {
        "name": tag_xml.attrib.get("name"),
        "enum_id": int(tag_xml.attrib["enumID"]),
        "value": value
    }


def carddefs_xml_to_json(carddefs_xml: ElementTree) -> Dict[str, Any]:
    root = carddefs_xml.getroot()
    ret = {"build": root.attrib["build"], "entities": []}

    for entity in root:
        assert entity.tag == "Entity"

        tags = []
        referenced_tags = []
        for t in entity:
            if t.tag == "Tag":
                tags.append(t)
            elif t.tag == "ReferencedTag":
                referenced_tags.append(t)

        entity_json = {
            "card_id": entity.attrib["CardID"],
            "id": entity.attrib["ID"],
            "tags": [tag_xml_to_json(t) for t in tags if t.attrib.get("name") not in BLACKLISTED_TAGS],
        }

        if referenced_tags:
            entity_json["referenced_tags"] = [tag_xml_to_json(r) for r in referenced_tags]

        ret["entities"].append(entity_json)

    return ret


def bountydefs_xml_to_json(bountydefs_xml: ElementTree) -> Dict[str, Any]:
    pass


def mecenarydefs_xml_to_json(mercenarydefs_xml: ElementTree) -> Dict[str, Any]:
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", nargs="?")

    args = parser.parse_args()

    if args.format == "carddefs":
        etree = ElementTree()
        etree.parse(source=sys.stdin)
        ret = carddefs_xml_to_json(etree)
        print(json.dumps(ret, ensure_ascii=False))
