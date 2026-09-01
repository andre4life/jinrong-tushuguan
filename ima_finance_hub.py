# -*- coding: utf-8 -*-
"""
金融图书馆 - Tencent ima 知识库直连与本地联合检索引擎
"""
import os, sys, json, urllib.request, urllib.error

BASE_URL = "https://ima.qq.com/openapi/wiki/v1"

def get_config():
    local_cfg = os.path.join(os.path.dirname(__file__), "config.json")
    hermes_cfg = r"D:\Hermes输出\ima接入\config.json"
    cfg = {
        "client_id": os.environ.get("IMA_CLIENT_ID", "3a93bc1ccc5f54d6b1103a0ba4824f6f"),
        "api_key": os.environ.get("IMA_API_KEY", "fUIfBMuEGBIB8/DtJjxo2kj6Nj164RnWCMMpbuZqTdn4MlTIJc3S3T4vy9yrOkBf6+uCXYeKsw=="),
        "kb_id": os.environ.get("IMA_KB_ID", "gy0q242S12_lBTcUH4QADLEnE2GcM-JKps7Jv5cg75g=")
    }
    for p in [local_cfg, hermes_cfg]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as fp:
                    cfg.update(json.load(fp))
                    break
            except Exception:
                pass
    return cfg

def ima_api(path, payload, cfg):
    url = BASE_URL + path
    headers = {
        "Content-Type": "application/json",
        "ima-openapi-clientid": cfg.get("client_id", ""),
        "ima-openapi-apikey": cfg.get("api_key", "")
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"code": e.code, "msg": f"HTTP {e.code}: {e.read().decode('utf-8')}"}
    except Exception as e:
        return {"code": -1, "msg": str(e)}

def search_ima(query, cfg=None):
    if cfg is None: cfg = get_config()
    kb_id = cfg.get("kb_id", "")
    if not kb_id: return []
    res = ima_api("/search_knowledge", {"query": query, "cursor": "", "knowledge_base_id": kb_id}, cfg)
    if res.get("code") == 0:
        return res.get("data", {}).get("info_list", [])
    return []

def search_local(query, base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    results = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".md"):
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                        if query.lower() in content.lower() or query.lower() in f.lower():
                            rel_path = os.path.relpath(fpath, base_dir)
                            idx = content.lower().find(query.lower())
                            snippet = ""
                            if idx != -1:
                                start = max(0, idx - 40)
                                end = min(len(content), idx + 80)
                                snippet = content[start:end].replace("\n", " ").strip()
                            else:
                                snippet = content[:100].replace("\n", " ").strip()
                            results.append({
                                "file": rel_path,
                                "title": f[:-3],
                                "snippet": snippet
                            })
                except Exception:
                    pass
    return results

def hybrid_search(query):
    cfg = get_config()
    print("=" * 60)
    print(f"🔍 联合检索关键词: 【{query}】")
    print("=" * 60 + "\n")
    
    local_hits = search_local(query)
    print(f"📚 [本地金融图书馆] 命中 {len(local_hits)} 篇精品文献:")
    for i, h in enumerate(local_hits[:8], 1):
        print(f"  {i}. 📄 {h['file']}")
        print(f"     ↳ ...{h['snippet']}...\n")
    
    cloud_hits = search_ima(query, cfg)
    print(f"☁️ [腾讯 ima 云端知识库] 命中 {len(cloud_hits)} 条云端记录:")
    for i, h in enumerate(cloud_hits[:8], 1):
        hl = (h.get("highlight_content") or "").replace("\n", " ").strip()
        print(f"  {i}. 🏷️ [{h.get('media_id', 'N/A')}] {h.get('title')}")
        if hl:
            print(f"     ↳ {hl[:100]}...\n")
    print("=" * 60)

def list_kbs():
    cfg = get_config()
    res = ima_api("/get_addable_knowledge_base_list", {"cursor": "", "limit": 50}, cfg)
    if res.get("code") == 0:
        print("✅ 腾讯 ima 已直连知识库列表:")
        for kb in res.get("data", {}).get("addable_knowledge_base_list", []):
            is_cur = " ⭐ [当前生效]" if kb["id"] == cfg.get("kb_id") else ""
            print(f"  - 📚 [{kb['id']}]{is_cur} : {kb['name']}")
    else:
        print(f"❌ 获取知识库失败: {res.get('msg')}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("金融图书馆 - Tencent ima 联动引擎")
        print("用法:")
        print("  python ima_finance_hub.py list              # 列出已连接的 ima 知识库")
        print("  python ima_finance_hub.py search <关键词>   # 联合检索本地金融图书馆与 ima")
    else:
        cmd = sys.argv[1]
        if cmd == "list":
            list_kbs()
        elif cmd == "search" and len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            hybrid_search(query)
        else:
            hybrid_search(cmd)
