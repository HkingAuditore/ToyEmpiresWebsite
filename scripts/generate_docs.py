#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "Data"
DOCS_DIR = BASE_DIR / "docs" / "数据"
SPECIAL_DIR = DOCS_DIR / "特殊系统"

SPRITE_MAP: Dict[str, str] = {
    "ATK": "攻击力",
    "DEF": "防御力",
    "Tech": "科技",
    "Policy": "政策",
    "Pdct": "生产力",
    "Maintain": "补给",
    "MainTain": "补给",
    "Gold": "黄金",
    "Food": "食物",
    "ActionPoint": "行政点",
    "Pop": "人口",
    "SPD": "速度",
    "HP": "生命值",
    "Tax": "税收",
    "NL_0": "未定等级",
    "NL_1": "王国",
    "NL_2": "帝国",
    "NL_3": "神圣帝国",
    "PolicySlot": "政策槽位",
}

STYLE_TAG_PATTERN = re.compile(r"<\/?style[^>]*>")
GENERIC_TAG_PATTERN = re.compile(r"<[^>]+>")
SPRITE_PATTERN = re.compile(r"<sprite name=\"([^\"]+)\">")

def clean_text(raw: str | None) -> str:
    if raw is None:
        return ""
    text = raw
    text = text.replace("<![CDATA[", "").replace("]]>", "")
    text = text.replace("\\n", "\n")
    text = text.replace("&lt;", "<").replace("&gt;", ">")
    text = STYLE_TAG_PATTERN.sub("", text)
    text = text.replace("</indent>", "")
    text = re.sub(r"<indent[^>]*>", "", text)
    text = text.replace("<br>", "\n")
    text = text.replace("<b>", "").replace("</b>", "")
    text = text.replace("<i>", "").replace("</i>", "")

    def sprite_repl(match: re.Match[str]) -> str:
        key = match.group(1)
        label = SPRITE_MAP.get(key, key)
        return f"【{label}】"

    text = SPRITE_PATTERN.sub(sprite_repl, text)
    text = GENERIC_TAG_PATTERN.sub("", text)
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        stripped = re.sub(r"^>+", "", stripped).strip()
        if stripped:
            lines.append(stripped)
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"【([^】]+)】\[\1\]", r"【\1】", cleaned)
    return cleaned.strip()


def format_cell(value: str) -> str:
    if not value:
        return ""
    return value.replace("|", "&#124;").replace("\n", "<br />")


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_overview() -> None:
    content = textwrap.dedent(
        """\
        ---
        title: 数据概览
        sidebar_position: 1
        ---
        # 数据概览

        本节文档依据项目 `Data` 目录下提供的最新游戏数据文件自动生成，涵盖政策、科技、单位、建筑、文明以及各势力的特殊系统设定，
        方便在不直接查阅原始 JSON/XML 文件的情况下了解数值与文字描述。
        """
    ).strip() + "\n"
    write_file(DOCS_DIR / "概览.mdx", content)


def generate_policies() -> None:
    tree = ET.parse(DATA_DIR / "Policy" / "PolicyData0.xml")
    root = tree.getroot()
    type_map = {"0": "通用", "1": "经济", "2": "军事", "3": "特殊"}
    rows: List[Tuple[str, str, str, str, str]] = []
    for policy in root.findall("Policy"):
        pid = policy.get("PID", "")
        type_label = type_map.get(policy.get("Type", ""), policy.get("Type", ""))
        occupancy = policy.get("Occupancy", "")
        name = clean_text("".join(element.text or "" for element in policy.findall("Name")))
        effect = clean_text("".join(element.text or "" for element in policy.findall("Content")))
        rows.append((pid, name, type_label, occupancy, effect))
    rows.sort(key=lambda item: item[0])
    lines = [
        "---",
        "title: 政策数据",
        "sidebar_position: 2",
        "---",
        "# 政策",
        "",
        "数据来源：`Data/Policy/PolicyData0.xml`。",
        "",
        "| ID | 名称 | 类别 | 占用槽位 | 效果 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for pid, name, type_label, occupancy, effect in rows:
        lines.append(
            f"| {pid} | {name} | {type_label} | {occupancy} | {format_cell(effect)} |"
        )
    write_file(DOCS_DIR / "政策.mdx", "\n".join(lines) + "\n")


def generate_techs() -> None:
    tree = ET.parse(DATA_DIR / "Tech" / "TechData0.xml")
    root = tree.getroot()
    rows: List[Tuple[str, str, str]] = []
    for tech in root.findall("Tech"):
        tid = tech.get("TID", "")
        name = clean_text("".join(element.text or "" for element in tech.findall("Name")))
        desc = clean_text("".join(element.text or "" for element in tech.findall("Content")))
        rows.append((tid, name, desc))
    rows.sort(key=lambda item: item[0])
    lines = [
        "---",
        "title: 科技数据",
        "sidebar_position: 3",
        "---",
        "# 科技",
        "",
        "数据来源：`Data/Tech/TechData0.xml`。",
        "",
        "| ID | 名称 | 效果 |",
        "| --- | --- | --- |",
    ]
    for tid, name, desc in rows:
        lines.append(f"| {tid} | {name} | {format_cell(desc)} |")
    write_file(DOCS_DIR / "科技.mdx", "\n".join(lines) + "\n")


def generate_units() -> None:
    tree = ET.parse(DATA_DIR / "Unit" / "UnitData0.xml")
    root = tree.getroot()
    rows: List[Tuple[str, str, str, str]] = []
    for unit in root.findall("Unit"):
        uid = unit.get("UID", "")
        file_name = unit.get("fileName", "")
        name = clean_text("".join(element.text or "" for element in unit.findall("Name")))
        desc = clean_text("".join(element.text or "" for element in unit.findall("Content")))
        rows.append((uid, name, file_name, desc))
    rows.sort(key=lambda item: item[0])
    lines = [
        "---",
        "title: 单位数据",
        "sidebar_position: 4",
        "---",
        "# 单位",
        "",
        "数据来源：`Data/Unit/UnitData0.xml`。",
        "",
        "| ID | 名称 | 资源名 | 描述 |",
        "| --- | --- | --- | --- |",
    ]
    for uid, name, file_name, desc in rows:
        lines.append(
            f"| {uid} | {name} | {file_name} | {format_cell(desc)} |"
        )
    write_file(DOCS_DIR / "单位.mdx", "\n".join(lines) + "\n")


def generate_buildings() -> None:
    tree = ET.parse(DATA_DIR / "Buildings" / "BuildingsData0.xml")
    root = tree.getroot()
    rows: List[Tuple[str, str, str, str, List[str]]] = []
    for building in root.findall("Building"):
        bid = building.get("BID", "")
        name = clean_text("".join(element.text or "" for element in building.findall("Name")))
        file_name = building.get("fileName", "")
        desc = clean_text("".join(element.text or "" for element in building.findall("Content")))
        upgrades = [
            clean_text(upgrade.text or "") for upgrade in building.findall("Upgrades/Upgrade")
        ]
        rows.append((bid, name, file_name, desc, upgrades))
    rows.sort(key=lambda item: item[0])
    lines = [
        "---",
        "title: 建筑数据",
        "sidebar_position: 5",
        "---",
        "# 建筑",
        "",
        "数据来源：`Data/Buildings/BuildingsData0.xml`。",
        "",
        "| ID | 名称 | 资源名 | 说明 | 升级方向 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for bid, name, file_name, desc, upgrades in rows:
        upgrade_text = "、".join(filter(None, upgrades)) or "—"
        lines.append(
            f"| {bid} | {name} | {file_name} | {format_cell(desc)} | {format_cell(upgrade_text)} |"
        )
    write_file(DOCS_DIR / "建筑.mdx", "\n".join(lines) + "\n")


def generate_civilizations() -> Dict[str, str]:
    tree = ET.parse(DATA_DIR / "Civilizations" / "CivsData0.xml")
    root = tree.getroot()
    cid_to_name: Dict[str, str] = {}
    lines = [
        "---",
        "title: 文明数据",
        "sidebar_position: 6",
        "---",
        "# 文明",
        "",
        "数据来源：`Data/Civilizations/CivsData0.xml`。",
        "",
    ]
    for civ in root.findall("Civilization"):
        cid = civ.get("CID", "")
        name = clean_text("".join(element.text or "" for element in civ.findall("Name")))
        cid_to_name[cid] = name or cid
        content_fragments = [clean_text(element.text or "") for element in civ.findall("Content")]
        level_tips = [clean_text(level_tip.text or "") for level_tip in civ.findall("LevelTip")]
        lines.append(f"## {name or cid} ({cid})")
        if content_fragments:
            lines.append("")
            for fragment in content_fragments:
                if fragment:
                    lines.append(fragment)
                    lines.append("")
        if level_tips:
            lines.append("**等级提示**")
            for tip in level_tips:
                lines.append(f"- {tip}")
            lines.append("")
    write_file(DOCS_DIR / "文明.mdx", "\n".join(lines).strip() + "\n")
    return cid_to_name


def generate_nation_levels(cid_to_name: Dict[str, str]) -> None:
    tree = ET.parse(DATA_DIR / "Civilizations" / "NationLevel" / "NationLevelData0.xml")
    root = tree.getroot()
    lines = [
        "---",
        "title: 国家等级",
        "sidebar_position: 7",
        "---",
        "# 国家等级",
        "",
        "数据来源：`Data/Civilizations/NationLevel/NationLevelData0.xml`。",
        "",
    ]
    for civ in root.findall("Civilization"):
        cid = civ.get("CID", "")
        name = cid_to_name.get(cid, cid)
        lines.append(f"## {name} ({cid})")
        lines.append("")
        lines.append("| 等级ID | 名称 | 效果 |")
        lines.append("| --- | --- | --- |")
        level_rows: List[str] = []
        for level in civ.findall("Level"):
            lid = level.get("LID", "")
            level_name = clean_text("".join(element.text or "" for element in level.findall("Name")))
            desc = clean_text("".join(element.text or "" for element in level.findall("Content")))
            level_rows.append(f"| {lid} | {level_name} | {format_cell(desc)} |")
        lines.extend(level_rows)
        lines.append("")
    write_file(DOCS_DIR / "国家等级.mdx", "\n".join(lines).strip() + "\n")


def generate_byzantine_special() -> None:
    item_tree = ET.parse(DATA_DIR / "SpecSys" / "Byzantine" / "ItemData.xml")
    quest_tree = ET.parse(DATA_DIR / "SpecSys" / "Byzantine" / "QuestData.xml")
    item_rows: List[Tuple[str, str, str, str]] = []
    for item in item_tree.getroot().findall("Item"):
        item_id = item.get("ID", "")
        name = item.get("Name", "")
        cost = item.get("Cost", "")
        detail = clean_text("".join(item.itertext()))
        item_rows.append((item_id, name, cost, detail))
    item_rows.sort(key=lambda value: value[0])
    quest_rows: List[Tuple[str, str, str, str]] = []
    for quest in quest_tree.getroot().findall("Quest"):
        quest_id = quest.get("ID", "")
        name = quest.get("Name", "")
        prestige = quest.get("ImperialPrestige", "")
        detail = clean_text("".join(element.text or "" for element in quest.findall("Detail")))
        reward = clean_text("".join(element.text or "" for element in quest.findall("Reward")))
        quest_rows.append((quest_id, name, prestige, detail, reward))
    quest_rows.sort(key=lambda value: value[0])
    lines = [
        "---",
        "title: 拜占庭特殊系统",
        "sidebar_position: 1",
        "---",
        "# 拜占庭特殊系统",
        "",
        "数据来源：`Data/SpecSys/Byzantine` 目录。",
        "",
        "## 物品与加成",
        "",
        "| ID | 名称 | 花费 | 效果 |",
        "| --- | --- | --- | --- |",
    ]
    for item_id, name, cost, detail in item_rows:
        lines.append(
            f"| {item_id} | {name} | {cost} | {format_cell(detail)} |"
        )
    lines.extend([
        "",
        "## 帝国任务",
        "",
        "| ID | 名称 | 帝国声望 | 条件 | 奖励 |",
        "| --- | --- | --- | --- | --- |",
    ])
    for quest_id, name, prestige, detail, reward in quest_rows:
        lines.append(
            f"| {quest_id} | {name} | {prestige} | {format_cell(detail)} | {format_cell(reward)} |"
        )
    write_file(SPECIAL_DIR / "拜占庭.mdx", "\n".join(lines) + "\n")


def generate_daming_special() -> None:
    clique_tree = ET.parse(DATA_DIR / "SpecSys" / "DaMing" / "CliqueData.xml")
    daxueshi_tree = ET.parse(DATA_DIR / "SpecSys" / "DaMing" / "DaXueShiData.xml")
    order_tree = ET.parse(DATA_DIR / "SpecSys" / "DaMing" / "GovernmentOrderData.xml")
    clique_rows: List[Tuple[str, str, str]] = []
    clique_name_map: Dict[str, str] = {}
    for clique in clique_tree.getroot().findall("Clique"):
        cid = clique.get("ID", "")
        name = clique.get("Name", "")
        detail = clean_text("".join(clique.itertext()))
        clique_rows.append((cid, name, detail))
        clique_name_map[cid] = name
    clique_rows.sort(key=lambda value: value[0])
    daxueshi_rows: List[Tuple[str, str, str, str, str]] = []
    for scholar in daxueshi_tree.getroot().findall("DaXueShi"):
        sid = scholar.get("ID", "")
        name = scholar.get("Name", "")
        clique_id = scholar.get("Clique", "")
        clique_name = clique_name_map.get(clique_id, clique_id)
        salary = scholar.get("Salary", "")
        hire_cost = scholar.get("HireCostActionPoint", "")
        detail = clean_text("".join(scholar.itertext()))
        daxueshi_rows.append((sid, name, clique_name, salary, hire_cost, detail))
    daxueshi_rows.sort(key=lambda value: value[0])
    order_rows: List[Tuple[str, str, str, str]] = []
    for order in order_tree.getroot().findall("GovernmentOrder"):
        oid = order.get("ID", "")
        name = order.get("Name", "")
        cost = order.get("CostGold", "")
        detail = clean_text("".join(order.itertext()))
        order_rows.append((oid, name, cost, detail))
    order_rows.sort(key=lambda value: value[0])
    lines = [
        "---",
        "title: 大明特殊系统",
        "sidebar_position: 2",
        "---",
        "# 大明特殊系统",
        "",
        "数据来源：`Data/SpecSys/DaMing` 目录。",
        "",
        "## 派系",
        "",
        "| ID | 派系 | 效果 |",
        "| --- | --- | --- |",
    ]
    for cid, name, detail in clique_rows:
        lines.append(f"| {cid} | {name} | {format_cell(detail)} |")
    lines.extend([
        "",
        "## 大学士",
        "",
        "| ID | 姓名 | 所属派系 | 薪俸 | 招募所需行政点 | 效果 |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for sid, name, clique_name, salary, hire_cost, detail in daxueshi_rows:
        lines.append(
            f"| {sid} | {name} | {clique_name} | {salary} | {hire_cost} | {format_cell(detail)} |"
        )
    lines.extend([
        "",
        "## 政令",
        "",
        "| ID | 名称 | 黄金消耗 | 条件与效果 |",
        "| --- | --- | --- | --- |",
    ])
    for oid, name, cost, detail in order_rows:
        lines.append(f"| {oid} | {name} | {cost} | {format_cell(detail)} |")
    write_file(SPECIAL_DIR / "大明.mdx", "\n".join(lines) + "\n")


def generate_france_special() -> None:
    state_tree = ET.parse(DATA_DIR / "SpecSys" / "France" / "StateData.xml")
    lines = [
        "---",
        "title: 法兰西特殊系统",
        "sidebar_position: 3",
        "---",
        "# 法兰西特殊系统",
        "",
        "数据来源：`Data/SpecSys/France/StateData.xml`。",
        "",
    ]
    for state in state_tree.getroot().findall("State"):
        sid = state.get("ID", "")
        name = state.get("Name", "")
        loyal = clean_text("".join(state.findtext("Loyal") or ""))
        loyal_name = state.find("Loyal").get("Name", "") if state.find("Loyal") is not None else ""
        rebel = clean_text("".join(state.findtext("Rebel") or ""))
        rebel_name = state.find("Rebel").get("Name", "") if state.find("Rebel") is not None else ""
        request = [clean_text(buff.text or "") for buff in state.findall("Request/Buff")]
        satisfied = [clean_text(buff.text or "") for buff in state.findall("Satisfied/Buff")]
        please = [clean_text(buff.text or "") for buff in state.findall("Please/Buff")]
        lines.append(f"## {name} ({sid})")
        if loyal:
            lines.append(f"- **忠诚加成（{loyal_name}）**：{loyal}")
        if rebel:
            lines.append(f"- **叛乱惩罚（{rebel_name}）**：{rebel}")
        if request:
            lines.append("- **通常诉求**：")
            for item in request:
                lines.append(f"  - {item}")
        if satisfied:
            lines.append("- **满足诉求后的奖励**：")
            for item in satisfied:
                lines.append(f"  - {item}")
        if please:
            lines.append("- **讨好额外奖励**：")
            for item in please:
                lines.append(f"  - {item}")
        lines.append("")
    write_file(SPECIAL_DIR / "法兰西.mdx", "\n".join(lines).strip() + "\n")


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    SPECIAL_DIR.mkdir(parents=True, exist_ok=True)
    generate_overview()
    generate_policies()
    generate_techs()
    generate_units()
    generate_buildings()
    cid_to_name = generate_civilizations()
    generate_nation_levels(cid_to_name)
    generate_byzantine_special()
    generate_daming_special()
    generate_france_special()


if __name__ == "__main__":
    main()
