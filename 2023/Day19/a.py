from operator import eq, gt, lt
from typing import Callable, Dict, List, TypedDict

TEST = False

if TEST:
    _raw = [
        "px{a<2006:qkq,m>2090:A,rfg}",
        "pv{a>1716:R,A}",
        "lnx{m>1548:A,A}",
        "rfg{s<537:gd,x>2440:R,A}",
        "qs{s>3448:A,lnx}",
        "qkq{x<1416:A,crn}",
        "crn{x>2662:A,R}",
        "in{s<1351:px,qqz}",
        "qqz{s>2770:qs,m<1801:hdj,R}",
        "gd{a>3333:R,R}",
        "hdj{m>838:A,pv}",
        "",
        "{x=787,m=2655,a=1222,s=2876}",
        "{x=1679,m=44,a=2067,s=496}",
        "{x=2036,m=264,a=79,s=2244}",
        "{x=2461,m=1339,a=466,s=291}",
        "{x=2127,m=1623,a=2188,s=1013}",
    ]
else:
    with open("./input.txt", "r") as txtin:
        _raw = [ln.strip() for ln in txtin]


def make_workflow(workflow_statement: str) -> Callable[Dict[str, str], str]:
    statements = workflow_statement.split(",")
    logic_statements = list(map(lambda _: _.split(":"), statements))

    def workflow(item: Dict[str, int]) -> str:
        for statement in logic_statements:
            # Final else clause -  this is the final else
            if len(statement) == 1:
                return statement[0]

            statement, output = statement

            splitter = "=" if "=" in statement else "<" if "<" in statement else ">"
            operator = eq if "=" in statement else lt if "<" in statement else gt
            attribute, result = statement.split(splitter)

            if operator(item.get(attribute), int(result)):
                return output

    return workflow


class DATA(TypedDict):
    workflows: Dict[str, Callable[Dict[str, str], str]]
    parts: List[Dict[str, int]]


def create_data_from_raw(_input: List[str]) -> DATA:
    data = {"workflows": {}, "parts": []}

    for ln in _input:
        if ln.startswith("{"):
            # It's a part
            part_array = [
                _.split("=") for _ in ln.replace("{", "").replace("}", "").split(",")
            ]
            part_spec = {_[0]: int(_[1]) for _ in part_array}

            data["parts"].append(part_spec)

        elif len(ln) > 0:
            name, rest = ln.split("{")
            data["workflows"][name] = make_workflow(rest.replace("}", ""))

    return data


data = create_data_from_raw(_raw)

resolved_items = []
for part in data["parts"]:
    result = data["workflows"]["in"](part)
    while result not in ("R", "A"):
        result = data["workflows"][result](part)
    resolved_items.append(result)

total_score = 0
for idx, resolution in enumerate(resolved_items):
    if resolution == "A":
        total_score += sum(data["parts"][idx].values())

print(f"Total score: {total_score}")
# 330820 is the correct answer
