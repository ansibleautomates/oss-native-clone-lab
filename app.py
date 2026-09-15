SOURCE_MARKER = "FORK_CODE_V1"

def add(a, b):
    return a + b

def contributor_probe():
    import os, json
    print(json.dumps({"contributor_code_executed": True, "canary_readable_by_contributor_code": os.environ.get("POC_SYNTHETIC_CANARY", "").startswith("synthetic-only-")}))
