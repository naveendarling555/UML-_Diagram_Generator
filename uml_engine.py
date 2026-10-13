"""Rule-based NLP-inspired UML extraction engine.

This beginner-friendly implementation uses sentence splitting, noun-phrase-like
candidate extraction, action verb matching, and relationship cues. It is a
heuristic educational prototype, not a production-grade language model.
"""
import re
from collections import OrderedDict

STOP_CLASSES = {
    "system", "application", "software", "user", "users", "customer", "customers",
    "person", "people", "website", "platform", "module", "information", "data",
    "details", "feature", "features", "process", "processes", "page", "screen"
}
ACTION_VERBS = {
    "register": "register()", "login": "login()", "log in": "login()",
    "sign in": "login()", "search": "search()", "add": "add()", "create": "create()",
    "update": "update()", "edit": "update()", "delete": "delete()", "remove": "delete()",
    "view": "view()", "display": "display()", "manage": "manage()", "book": "book()",
    "pay": "makePayment()", "purchase": "purchase()", "track": "track()",
    "send": "send()", "generate": "generate()", "upload": "upload()",
    "download": "download()", "approve": "approve()", "submit": "submit()",
    "calculate": "calculate()", "check": "check()", "notify": "notify()",
}
RELATION_CUES = [
    (r"\bextends\b|\binherits from\b|\bis a type of\b", "inheritance"),
    (r"\bimplements\b", "implementation"),
    (r"\bcontains\b|\bconsists of\b|\bhas many\b|\bincludes\b", "composition"),
    (r"\buses\b|\buses the\b|\binteracts with\b|\bconnects to\b", "association"),
]
ATTR_CUES = {
    "name": "name: String", "email": "email: String", "password": "password: String",
    "phone": "phone: String", "address": "address: String", "date": "date: Date",
    "status": "status: String", "price": "price: Decimal", "amount": "amount: Decimal",
    "id": "id: Integer", "title": "title: String", "description": "description: String",
    "role": "role: String", "quantity": "quantity: Integer", "total": "total: Decimal",
}

def clean_name(value):
    value = re.sub(r"[^A-Za-z0-9 ]", " ", value)
    words = [w for w in value.split() if w.lower() not in {"a", "an", "the", "and", "or", "to", "of", "for", "with", "in", "on", "by", "is", "are", "can", "will", "should"}]
    return "".join(w.capitalize() for w in words[:3])

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]

def extract_classes(text):
    candidates = OrderedDict()
    # Capitalized concepts and common nouns near system-domain words
    for match in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b", text):
        name = clean_name(match.group(1))
        if name and name.lower() not in STOP_CLASSES and len(name) > 2:
            candidates[name] = True
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    domain_words = {
        "student", "teacher", "course", "payment", "order", "product", "admin",
        "doctor", "patient", "appointment", "vehicle", "service", "booking", "ticket",
        "employee", "department", "account", "report", "internship", "application",
        "registration", "quiz", "question", "answer", "library", "book", "maintenance",
        "customer", "invoice", "notification", "review", "cart", "user"
    }
    for word in words:
        if word in domain_words:
            name = word.capitalize()
            if name.lower() not in STOP_CLASSES:
                candidates[name] = True
    # Keep the first few meaningful domain concepts
    result = list(candidates.keys())[:8]
    if not result:
        result = ["MainEntity", "Service", "Report"]
    return result

def extract_methods(text):
    low = text.lower()
    found = []
    for cue, method in ACTION_VERBS.items():
        if re.search(r"\b" + re.escape(cue) + r"\b", low) and method not in found:
            found.append(method)
    return found[:6] or ["processRequest()"]

def extract_attributes(text):
    low = text.lower()
    attrs = []
    for cue, declaration in ATTR_CUES.items():
        if re.search(r"\b" + re.escape(cue) + r"\b", low):
            attrs.append(declaration)
    return attrs[:6] or ["id: Integer", "name: String"]

def extract_relationships(classes, text):
    rels = []
    low = text.lower()
    for pattern, kind in RELATION_CUES:
        if re.search(pattern, low) and len(classes) >= 2:
            symbol = {"inheritance": "--|>", "implementation": "..|>", "composition": "*--", "association": "--"}[kind]
            rels.append({"from": classes[0], "to": classes[1], "kind": kind, "symbol": symbol})
    # Add plausible associations when multiple concepts appear
    if not rels and len(classes) > 1:
        rels.append({"from": classes[0], "to": classes[1], "kind": "association", "symbol": "--"})
    return rels[:5]

def mermaid_class(classes, attrs, methods, rels):
    lines = ["classDiagram"]
    for i, cls in enumerate(classes):
        lines.append(f"class {cls} {{")
        for attr in attrs[:3]:
            lines.append("  +" + attr.replace(": ", ": "))
        for method in methods[:3]:
            lines.append("  +" + method)
        lines.append("}")
    for rel in rels:
        lines.append(f"{rel['from']} {rel['symbol']} {rel['to']} : {rel['kind']}")
    return "\n".join(lines)

def mermaid_usecase(classes, methods):
    lines = ["flowchart LR", "  actor([Actor / User])"]
    for i, method in enumerate(methods[:6]):
        label = method.replace("()", "").replace("makePayment", "Make payment")
        node = f"uc{i}"
        lines.append(f'  {node}(["{label.title()}"])')
        lines.append(f"  actor --> {node}")
    if not methods:
        lines += ['  uc0(["Use system"])', "  actor --> uc0"]
    return "\n".join(lines)

def mermaid_sequence(classes, methods):
    actor = "User"
    service = classes[0] if classes else "System"
    lines = ["sequenceDiagram", f"  actor {actor}", f"  participant S as {service}"]
    for method in methods[:5]:
        label = method.replace("()", "")
        lines.append(f"  {actor}->>S: {label.title()}")
        lines.append(f"  S-->>{actor}: Result / confirmation")
    return "\n".join(lines)

def mermaid_activity(methods):
    lines = ["flowchart TD", "  A([Start])"]
    previous = "A"
    for i, method in enumerate(methods[:6]):
        node = f"step{i}"
        lines.append(f'  {node}["{method.replace("()", "").title()}"]')
        lines.append(f"  {previous} --> {node}")
        previous = node
    lines += [f"  {previous} --> Z([End])"]
    return "\n".join(lines)

def mermaid_state():
    return "stateDiagram-v2\n  [*] --> New\n  New --> InProgress: request started\n  InProgress --> Completed: success\n  InProgress --> Failed: error\n  Failed --> InProgress: retry\n  Completed --> [*]"

def generate_uml(text):
    classes = extract_classes(text)
    methods = extract_methods(text)
    attrs = extract_attributes(text)
    rels = extract_relationships(classes, text)
    return {
        "summary": {
            "classes": len(classes), "methods": len(methods),
            "relationships": len(rels), "words": len(text.split())
        },
        "classes": classes,
        "methods": methods,
        "attributes": attrs,
        "relationships": rels,
        "diagrams": {
            "class": mermaid_class(classes, attrs, methods, rels),
            "usecase": mermaid_usecase(classes, methods),
            "sequence": mermaid_sequence(classes, methods),
            "activity": mermaid_activity(methods),
            "state": mermaid_state()
        }
    }
