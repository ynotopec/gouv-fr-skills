#!/usr/bin/env python3
"""Test, validation et dashboard des skills fr-gov."""
import json, os, re, yaml

BASE_PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(BASE_PARENT, "skills")

def load_skill(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"_error": str(e), "content": ""}
    fm_end = content.find('---', 3)
    if fm_end <= 0:
        return {"_error": "No frontmatter", "content": content}
    try:
        fm = yaml.safe_load(content[3:fm_end].strip())
    except yaml.YAMLError as e:
        fm = {"_yaml_error": str(e)}
    body = content[fm_end+3:].strip()
    sections = re.findall(r'^#{1,6}\s+(.+)$', body, re.MULTILINE)
    return {"frontmatter": fm, "body": body, "sections": sections, "content": content}

def test_skill_dir(skill_path):
    files = []
    for root, _, filenames in os.walk(skill_path):
        for fn in filenames:
            files.append({"name": fn, "path": os.path.relpath(os.path.join(root, fn), skill_path), "size": os.path.getsize(os.path.join(root, fn))})
    return files

def run_all_tests():
    results = []
    errors = []
    for cat_root in sorted(os.listdir(SKILLS_DIR)):
        cat_path = os.path.join(SKILLS_DIR, cat_root)
        if not os.path.isdir(cat_path):
            continue
        for sub_root in sorted(os.listdir(cat_path)):
            sub_path = os.path.join(cat_path, sub_root)
            if not os.path.isdir(sub_path):
                continue
            for skill_root in sorted(os.listdir(sub_path)):
                skill_path = os.path.join(sub_path, skill_root)
                if not os.path.isdir(skill_path):
                    continue
                full_path = os.path.join(BASE_PARENT, "skills", cat_root, sub_root, skill_root)
                skill_md = os.path.join(full_path, "SKILL.md")
                if not os.path.exists(skill_md):
                    errors.append({"skill": skill_root, "error": "No SKILL.md"})
                    continue
                info = load_skill(skill_md)
                fm = info.get("frontmatter", {})
                checks = []
                errs = []
                checks.append({"name": "frontmatter.name", "pass": bool(fm.get("name")), "detail": str(fm.get("name"))})
                if not fm.get("name"): errs.append("missing name")
                checks.append({"name": "frontmatter.description", "pass": bool(fm.get("description")), "detail": str(fm.get("description"))[:80]})
                if not fm.get("description"): errs.append("missing description")
                checks.append({"name": "frontmatter.version", "pass": bool(fm.get("version")), "detail": str(fm.get("version"))})
                checks.append({"name": "frontmatter.license", "pass": bool(fm.get("license")), "detail": str(fm.get("license"))})
                checks.append({"name": "frontmatter.author", "pass": bool(fm.get("author")), "detail": str(fm.get("author"))})
                checks.append({"name": "frontmatter.platforms", "pass": bool(fm.get("platforms")), "detail": str(fm.get("platforms"))})
                checks.append({"name": "frontmatter.metadata", "pass": "metadata" in fm})
                checks.append({"name": "body.has_quand_utiliser", "pass": any("Quand utiliser" in s for s in info.get("sections", []))})
                checks.append({"name": "body.has_content", "pass": len(info.get("body", "")) > 50, "detail": str(len(info.get("body", ""))) + "B"})
                code_blocks = len(re.findall(r'```', info.get("content", "")))
                checks.append({"name": "body.has_code_blocks", "pass": code_blocks >= 2, "detail": str(code_blocks // 2) + " blocks"})
                files = test_skill_dir(full_path)
                scripts = [f for f in files if f["name"].endswith((".sh", ".py", ".rb", ".js", ".ts"))]
                checks.append({"name": "files.scripts_count", "pass": True, "detail": str(len(scripts))})
                for s in scripts:
                    checks.append({"name": "file:" + s["name"], "pass": s["size"] > 0, "detail": str(s["size"]) + "B"})
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', info.get("content", ""))
                checks.append({"name": "body.has_links", "pass": len(links) > 0, "detail": str(len(links))})
                todos = re.findall(r'(TODO|FIXME|HACK|XXX)', info.get("content", ""))
                checks.append({"name": "body.no_todos", "pass": len(todos) == 0, "detail": str(len(todos))})
                secrets = re.findall(r'(password|secret|token|api_key)\s*[:=]\s*["\']?[A-Za-z0-9]{8,}', info.get("content", ""), re.I)
                checks.append({"name": "body.no_secrets", "pass": len(secrets) == 0, "detail": str(len(secrets))})
                passed = sum(1 for c in checks if c["pass"])
                total = len(checks)
                results.append({"skill": skill_root, "category": cat_root, "subcategory": sub_root, "status": "PASS" if not errs else "FAIL", "passed": passed, "total": total, "score": round(passed / total * 100, 1) if total > 0 else 0, "checks": checks, "errors": errs, "file_count": len(files), "section_count": len(info.get("sections", []))})
                if errs:
                    errors.append({"skill": skill_root, "errors": errs})
    total = len(results)
    passed_count = sum(1 for r in results if r["status"] == "PASS")
    avg_score = round(sum(r["score"] for r in results) / total, 1) if total > 0 else 0
    # Compute passed_checks for global progress bar
    passed_checks_total = sum(r["passed"] for r in results)
    total_checks_total = sum(r["total"] for r in results)
    return {"total_skills": total, "passed": passed_count, "failed": total - passed_count, "average_score": avg_score, "passed_checks_total": passed_checks_total, "total_checks_total": total_checks_total, "errors": errors}, results

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f172a;color:#e2e8f0;padding:2rem}
h1{font-size:2rem;margin-bottom:.5rem;background:linear-gradient(135deg,#3b82f6,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.subtitle{color:#94a3b8;margin-bottom:2rem;font-size:.9rem}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin-bottom:2rem}
.kpi-card{background:#1e293b;border-radius:12px;padding:1.5rem;border:1px solid #334155}
.kpi-value{font-size:2.5rem;font-weight:700;line-height:1;margin-bottom:.25rem}
.kpi-label{color:#94a3b8;font-size:.85rem}
.kpi-value.pass{color:#22c55e}
.kpi-value.fail{color:#ef4444}
.kpi-value.avg{color:#3b82f6}
.kpi-value.total{color:#a78bfa}
.global-progress{background:#1e293b;border-radius:12px;padding:1.5rem;margin-bottom:2rem;border:1px solid #334155}
.pbar-bg{background:#334155;border-radius:999px;height:12px;overflow:hidden;margin-top:.75rem}
.pbar-fill{height:100%;border-radius:999px}
.pbar-fill.green{background:linear-gradient(90deg,#22c55e,#4ade80)}
.categories-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:1.5rem;margin-bottom:2rem}
.category-card{background:#1e293b;border-radius:12px;padding:1.5rem;border:1px solid #334155}
.category-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem}
.category-name{font-size:1.1rem;font-weight:600}
.category-badge{background:#334155;padding:.25rem .75rem;border-radius:999px;font-size:.8rem;font-weight:600}
.category-badge.pass{background:rgba(34,197,94,.2);color:#4ade80}
.category-badge.partial{background:rgba(251,191,36,.2);color:#fbbf24}
.skill-list{list-style:none}
.skill-item{display:flex;justify-content:space-between;align-items:center;padding:.5rem 0;border-bottom:1px solid #1a2332;font-size:.9rem}
.skill-item:last-child{border-bottom:none}
.skill-name{display:flex;align-items:center;gap:.5rem}
.score-bar{width:60px;height:6px;background:#334155;border-radius:999px;overflow:hidden}
.score-bar-fill{height:100%;border-radius:999px}
.score-bar-fill.high{background:#22c55e}
.score-bar-fill.mid{background:#fbbf24}
.score-bar-fill.low{background:#ef4444}
.details-section{background:#1e293b;border-radius:12px;padding:1.5rem;border:1px solid #334155;margin-bottom:2rem;overflow-x:auto}
.details-section h2{margin-bottom:1rem;font-size:1.2rem}
table{width:100%;border-collapse:collapse;font-size:.85rem}
th,td{text-align:left;padding:.75rem;border-bottom:1px solid #334155}
th{color:#94a3b8;font-weight:500}
tr:hover{background:#253347}
.status-pass{color:#22c55e;font-weight:600}
.status-fail{color:#ef4444;font-weight:600}
footer{text-align:center;color:#475569;font-size:.8rem;margin-top:2rem}
@media(max-width:768px){body{padding:1rem}.categories-grid{grid-template-columns:1fr}}
"""

def generate_dashboard(summary, results):
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)
    cat_stats = {}
    for cat, skills in categories.items():
        tc = sum(s["total"] for s in skills)
        pc = sum(s["passed"] for s in skills)
        sc = [s["score"] for s in skills]
        pr = round(len([s for s in skills if s["status"] == "PASS"]) / len(skills) * 100, 1)
        cat_stats[cat] = {"count": len(skills), "avg_score": round(sum(sc) / len(sc), 1), "total_checks": tc, "passed_checks": pc, "pass_rate": pr}
    subtitle_parts = []
    for cat in sorted(cat_stats):
        subtitle_parts.append(cat + ": " + str(cat_stats[cat]["pass_rate"]) + "%")
    subtitle = " \\u2022 ".join(subtitle_parts)

    # Category cards
    cat_cards = []
    for cat in sorted(cat_stats):
        st = cat_stats[cat]
        sks = categories[cat]
        bc = "pass" if st["pass_rate"] == 100 else "partial"
        bt = "✅ " + str(st["pass_rate"]) + "%" if st["pass_rate"] == 100 else "⚠️ " + str(st["pass_rate"]) + "%"
        items = []
        for s in sorted(sks, key=lambda x: x["score"], reverse=True):
            sc2 = "high" if s["score"] >= 90 else ("mid" if s["score"] >= 80 else "low")
            icon = "✅" if s["status"] == "PASS" else "❌"
            items.append(
                '<li class="skill-item">'
                + '<div class="skill-name"><span>' + icon + '</span><span>' + s["skill"] + '</span></div>'
                + '<div style="display:flex;align-items:center;gap:.5rem">'
                + '<div class="score-bar"><div class="score-bar-fill ' + sc2 + '" style="width:' + str(s["score"]) + '%"></div></div>'
                + '<span style="font-family:monospace;font-size:.85rem;color:#94a3b8">' + str(s["score"]) + '%</span>'
                + '</div></li>'
            )
        card = (
            '<div class="category-card">'
            + '<div class="category-header"><div class="category-name">' + cat + '</div><div class="category-badge ' + bc + '">' + bt + '</div></div>'
            + '<div style="font-size:.8rem;color:#94a3b8;margin-bottom:1rem">' + str(st["count"]) + ' skills \\u2022 ' + str(st["passed_checks"]) + '/' + str(st["total_checks"]) + ' checks \\u2022 Moy. ' + str(st["avg_score"]) + '%</div>'
            + '<div class="pbar-bg" style="margin-bottom:1rem"><div class="pbar-fill green" style="width:' + str(st["avg_score"]) + '%"></div></div>'
            + '<ul class="skill-list">' + ''.join(items) + '</ul></div>'
        )
        cat_cards.append(card)

    # Details table rows
    rows = []
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        cls = "status-pass" if r["status"] == "PASS" else "status-fail"
        rows.append(
            '<tr><td>' + r["skill"] + '</td>'
            + '<td>' + r["category"] + '/' + r["subcategory"] + '</td>'
            + '<td>' + str(r["passed"]) + '/' + str(r["total"]) + '</td>'
            + '<td>' + str(r["score"]) + '%</td>'
            + '<td>' + str(r["file_count"]) + '</td>'
            + '<td>' + str(r["section_count"]) + '</td>'
            + '<td class="' + cls + '">' + r["status"] + '</td></tr>'
        )

    # Error section
    if summary["errors"]:
        error_items = []
        for err in summary["errors"]:
            error_items.append(
                '<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:8px;padding:1rem;margin-bottom:.75rem;font-size:.9rem">'
                + '<strong style="color:#ef4444">' + err["skill"] + '</strong>'
                + '<div style="color:#94a3b8;margin-top:.25rem">' + ', '.join(err["errors"]) + '</div></div>'
            )
        error_html = '<div style="background:#1e293b;border-radius:12px;padding:1.5rem;border:1px solid #334155;margin-bottom:2rem"><h2 style="color:#ef4444;margin-bottom:1rem">\\u274c Erreurs</h2>' + ''.join(error_items) + '</div>'
    else:
        error_html = '<div style="background:rgba(34,197,94,.05);border:1px solid rgba(34,197,94,.2);border-radius:12px;padding:1.5rem;margin-bottom:2rem"><h2 style="color:#22c55e;margin-bottom:.5rem">\\u2705 Aucune erreur</h2><p style="color:#94a3b8">Toutes les skills ont pass\\u00e9 les checks.</p></div>'

    total_checks_all = summary["total_checks_total"]

    html = (
        '<!DOCTYPE html>\n'
        '<html lang="fr">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>Dashboard Tests Skills fr-gov</title>\n'
        '<style>' + CSS + '</style>\n'
        '</head>\n'
        '<body>\n'
        '<h1>\\ud83d\\udcca Dashboard Tests Skills fr-gov</h1>\n'
        '<p class="subtitle">Validation automatique de ' + str(summary["total_skills"]) + ' skills \\u2022 ' + subtitle + '</p>\n'
        + '<div class="kpi-grid">\n'
        + '  <div class="kpi-card"><div class="kpi-value total">' + str(summary["total_skills"]) + '</div><div class="kpi-label">Skills analys\\u00e9es</div></div>\n'
        + '  <div class="kpi-card"><div class="kpi-value pass">' + str(summary["passed"]) + '</div><div class="kpi-label">Valid\\u00e9es</div></div>\n'
        + '  <div class="kpi-card"><div class="kpi-value fail">' + str(summary["failed"]) + '</div><div class="kpi-label">\\u00c9checs</div></div>\n'
        + '  <div class="kpi-card"><div class="kpi-value avg">' + str(summary["average_score"]) + '%</div><div class="kpi-label">Score moyen</div></div>\n'
        + '</div>\n'
        + '<div class="global-progress">\n'
        + '  <div style="display:flex;justify-content:space-between;align-items:center">\n'
        + '    <span>Taux de r\\u00e9ussite global</span>\n'
        + '    <span style="font-weight:700;font-size:1.2rem;color:#22c55e">' + str(summary["average_score"]) + '%</span>\n'
        + '  </div>\n'
        + '  <div class="pbar-bg"><div class="pbar-fill green" style="width:' + str(summary["average_score"]) + '%"></div></div>\n'
        + '  <div style="margin-top:.75rem;font-size:.8rem;color:#94a3b8">' + str(summary["passed_checks_total"]) + ' checks globaux satisfaisants sur ' + str(total_checks_all) + '</div>\n'
        + '</div>\n'
        + '<h2 style="margin-bottom:1rem">Cat\\u00e9gories</h2>\n'
        + '<div class="categories-grid">\n' + '\n'.join(cat_cards) + '\n' + '</div>\n'
        + '<div class="details-section">\n'
        + '  <h2>\\ud83d\\udccb D\\u00e9tail par skill</h2>\n'
        + '  <table>\n'
        + '    <thead><tr><th>Skill</th><th>Cat\\u00e9gorie</th><th>Checks</th><th>Score</th><th>Fichiers</th><th>Sections</th><th>Statut</th></tr></thead>\n'
        + '    <tbody>' + '\n'.join(rows) + '\n'
        + '    </tbody>\n'
        + '  </table>\n'
        + '</div>\n'
        + error_html
        + '<footer>G\\u00e9n\\u00e9r\\u00e9 automatiquement \\u2022 ' + str(total_checks_all) + ' checks ex\\u00e9cut\\u00e9s</footer>\n'
        + '</body>\n</html>'
    )
    return html


if __name__ == "__main__":
    summary, results = run_all_tests()
    with open(os.path.join(os.path.dirname(__file__), "test-results.json"), "w") as f:
        json.dump({"summary": summary, "results": results}, f, indent=2, ensure_ascii=False)
    print("Tests : " + str(summary["total_skills"]) + " skills, " + str(summary["passed"]) + " PASS, " + str(summary["failed"]) + " FAIL, " + str(summary["average_score"]) + "% avg")

    dashboard = generate_dashboard(summary, results)
    with open(os.path.join(os.path.dirname(__file__), "dashboard.html"), "w") as f:
        f.write(dashboard)
    print("Dashboard généré : " + os.path.dirname(__file__) + "/dashboard.html")
    print("Taille : " + str(len(dashboard)) + " bytes")
