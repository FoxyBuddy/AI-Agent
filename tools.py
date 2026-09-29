import re
import time

import requests

CROSSREF_API = "https://api.crossref.org/works"
MAILTO = "foxylikesraccoon@gmail.com"   # TODO(你): 换成你的真实邮箱——Crossref礼貌池，进入优先通道

HEADERS = {"User-Agent": "AI-Agent paper-search-tool (github: FoxyBuddy)"}

_seen_ids = set()        # 跨调用去重：见过的DOI不再返回
MIN_INTERVAL = 1.5       # 礼貌性限流间隔（秒）
_last_call = 0.0


def _rate_limit_sleep():
    """距上次调用不足间隔时睡满差额，避免触发服务端限流。"""
    global _last_call
    wait = MIN_INTERVAL - (time.time() - _last_call)
    if wait > 0:
        time.sleep(wait)
    _last_call = time.time()


def truncate(text: str, max_chars: int = 500) -> str:
    """截断长文本，控制上下文预算。"""
    return text[:max_chars] + ("..." if len(text) > max_chars else "")


def _clean_abstract(raw) -> str:
    """Crossref摘要带JATS XML标签（<jats:p>等），剥离后规整空白。"""
    if not raw:
        return "(无摘要)"
    return " ".join(re.sub(r"<[^>]+>", "", raw).split())


def search_papers(query: str, max_results: int = 8) -> list[dict]:
    """学术论文检索工具（Crossref后端）：限流休眠 + 按DOI去重 + 摘要截断。

    设计决策D2：原arXiv后端在本网络路径上被WAF不稳定拦截（多词查询/id_list均406），
    换用Crossref——工具接口不变，上层Agent无感。
    """
    _rate_limit_sleep()
    params = {
        "query": query,
        "rows": max_results * 2,                      # 多取一倍，给去重留余量
        "select": "DOI,title,abstract,URL,issued,container-title",
        "mailto": MAILTO,
    }
    resp = requests.get(CROSSREF_API, params=params, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    items = resp.json().get("message", {}).get("items", [])
    papers = []
    for it in items:
        doi = it.get("DOI", "")
        if doi in _seen_ids:                          # 去重：同一篇跨调用只出现一次
            continue
        _seen_ids.add(doi)
        year = ((it.get("issued", {}).get("date-parts") or [[None]])[0] or [None])[0]
        papers.append({
            "paper_id": doi,
            "title": " ".join(it.get("title") or ["(无标题)"]),
            "abstract": truncate(_clean_abstract(it.get("abstract"))),
            "url": it.get("URL", ""),
            "venue": " ".join(it.get("container-title") or [""]),
            "year": year,
        })
        if len(papers) >= max_results:
            break
    return papers


def execute_tool(name: str, args: dict):
    """工具分发器：ReAct循环的执行端。"""
    if name == "search_papers":
        return search_papers(**args)
    return f"未知工具: {name}"


TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "search_papers",
            "description": "按关键词检索学术论文，返回论文列表（标题、摘要、DOI链接、年份、期刊/会议）",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "英文检索词，如 point cloud adversarial attack"},
                    "max_results": {"type": "integer", "description": "返回篇数，默认8"},
                },
                "required": ["query"],
            },
        },
    }
]
