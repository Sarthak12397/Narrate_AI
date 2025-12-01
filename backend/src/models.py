from datetime import datetime

def now():
    return datetime.utcnow()

def to_camel_id(doc):
    if not doc:
        return doc
    doc = doc.copy()
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc
