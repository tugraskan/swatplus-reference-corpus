"""Render pages: expand fact markers and symbol references at build time.

Pages contain `<!-- facts:NAME -->` markers and inline `[sym:name]`
references. Both are resolved against the *current* fact store, so source
links and line numbers are always correct for the pinned SWAT+ ref without
being stored in any page.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from ..parser.facts import FactStore, Symbol
from ..source.config import Config
from .pages import Page, load_all, page_dir

FACT_MARKER_RX = re.compile(r"<!--\s*facts:([a-z_]+)\s*-->")
SYM_REF_RX = re.compile(r"\[sym:([A-Za-z_]\w*)\]")


def table_cell(value, default: str = "") -> str:
    if value is None:
        return default
    text = str(value)
    if not text:
        return default
    return text.replace("\n", "<br>").replace("|", "&#124;")


def code_cell(value, default: str = "—") -> str:
    text = table_cell(value)
    return f"`{text}`" if text else default


def split_units_description(doc: str) -> tuple[str, str]:
    if "|" not in doc:
        return "", doc.strip()
    units, desc = doc.split("|", 1)
    return units.strip(), desc.strip()


class Renderer:
    def __init__(self, cfg: Config, store: FactStore, pages: list[Page], rich=None):
        self.cfg = cfg
        self.store = store
        self.pages = pages
        self.rich = rich
        self.page_by_symbol = {p.symbol: p for p in pages if p.symbol}
        self.page_paths = {p.path.resolve() for p in pages}

    # -- link helpers ------------------------------------------------------

    def source_url(self, sym: Symbol, line: int | None = None) -> str:
        base = f"{self.cfg.source_link_base}/{sym.file}"
        if line:
            return f"{base}#L{line}"
        return f"{base}#L{sym.start_line}-L{sym.end_line}"

    def source_location_url(self, path: str, line: int) -> str:
        return f"{self.cfg.source_link_base}/{path}#L{line}"

    def page_href(self, from_page: Page, sym_name: str) -> str | None:
        target = self.page_by_symbol.get(sym_name)
        if target is None:
            return None
        rel_from = from_page.path.parent
        try:
            docs_dir = self.cfg.abs_docs_dir
            rel = Path(
                *([".."] * len(rel_from.relative_to(docs_dir).parts))
            ) / target.path.relative_to(docs_dir)
            return rel.as_posix()
        except ValueError:
            return target.path.name

    def link_symbol(self, from_page: Page, name: str) -> str:
        """Best link for a symbol: its page if one exists, else its source."""
        name = name.lower()
        href = self.page_href(from_page, name)
        if href:
            return f"[`{name}`]({href})"
        sym = self.store.get(name)
        if sym:
            return f"[`{name}`]({self.source_url(sym)})"
        return f"`{name}`"

    @staticmethod
    def mermaid_label(value: str) -> str:
        """Keep source text safe inside a quoted Mermaid node label."""

        return (
            value.replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("|", "&#124;")
        )

    def call_graph(self, sym: Symbol) -> str:
        callers = self.store.callers_of(sym.name)
        callees = [self.store.get(name) for name in sym.calls]
        callees = [callee for callee in callees if callee is not None]
        if not callers and not callees:
            return ""

        records: dict[str, Symbol] = {sym.name: sym}
        records.update({caller.name: caller for caller in callers})
        records.update({callee.name: callee for callee in callees})
        node_ids = {name: f"call_{index}" for index, name in enumerate(sorted(records))}
        lines = ["### Call graph", "", "```mermaid", "flowchart LR"]
        for name, record in sorted(records.items()):
            node = node_ids[name]
            label = self.mermaid_label(
                f"{record.name}<br/>{record.file}:L{record.start_line}"
            )
            lines.append(f'    {node}["{label}"]')
            lines.append(
                f'    click {node} "{self.source_url(record, record.start_line)}" '
                f'"Open {record.name} on GitHub" _blank'
            )
        for caller in callers:
            lines.append(f"    {node_ids[caller.name]} --> {node_ids[sym.name]}")
        for callee in callees:
            lines.append(f"    {node_ids[sym.name]} --> {node_ids[callee.name]}")
        lines += ["```", ""]
        return "\n".join(lines)

    def control_flow_outline(self, sym: Symbol) -> str:
        if self.rich is None:
            return ""
        rich_proc = self.rich.get_of_kind(sym.name, sym.kind, file=sym.file)
        steps = getattr(rich_proc, "control_steps", None) if rich_proc else None
        if not steps:
            return ""

        # Very large routines remain usable in the browser while the omitted
        # count stays explicit. This is an ordered structural outline, not a
        # claim that every branch rejoins linearly.
        limit = 40
        shown = steps[:limit]
        lines = [
            "### Control-flow outline",
            "",
            "Source-order outline of parsed control statements. Select a node to open its exact source line.",
            "",
            "```mermaid",
            "flowchart TD",
        ]
        previous = None
        for index, step in enumerate(shown):
            node = f"flow_{index}"
            label = self.mermaid_label(
                f"{step.kind}: {step.summary}<br/>L{step.location.line}"
            )
            lines.append(f'    {node}["{label}"]')
            lines.append(
                f'    click {node} "{self.source_url(sym, step.location.line)}" '
                f'"Open line {step.location.line} on GitHub" _blank'
            )
            if previous is not None:
                lines.append(f"    {previous} --> {node}")
            previous = node
        if len(steps) > limit:
            omitted = len(steps) - limit
            lines.append(f'    flow_more["{omitted} additional parsed steps"]')
            if previous is not None:
                lines.append(f"    {previous} --> flow_more")
        lines += ["```", ""]
        return "\n".join(lines)

    # -- fact blocks -------------------------------------------------------

    def render_page(self, page: Page) -> str:
        sym = self.store.get(page.symbol) if page.symbol else None
        body = SYM_REF_RX.sub(
            lambda m: self.link_symbol(page, m.group(1)), page.body
        )
        body = FACT_MARKER_RX.sub(
            lambda m: self.fact_block(page, sym, m.group(1)), body
        )
        _status_notes = {
            "stale": "The source for this symbol changed after this page was "
            "written; prose may lag the code.",
            "affected": "A symbol this page calls or is called by changed; this "
            "page's own source did not, but its prose may lag — review.",
            "todo": "This page has not been written yet; only extracted facts "
            "are shown.",
        }
        badge = ""
        if page.status != "filled":
            note = _status_notes.get(page.status, "")
            badge = f"\n> **Status: {page.status}.** {note}\n"
        title = page.title or page.name
        return f"# {title}\n{badge}\n{body}\n"

    def fact_block(self, page: Page, sym: Symbol | None, name: str) -> str:
        fn = getattr(self, f"block_{name}", None)
        if fn is None:
            return f"<!-- unknown facts block: {name} -->"
        if sym is None and name != "toc":
            return f"*(no symbol `{page.symbol}` in the fact store)*"
        return fn(page, sym)

    def block_header(self, page: Page, sym: Symbol) -> str:
        rows = [
            f"**Kind:** {sym.kind}",
            f"**Source:** [`{sym.file}:{sym.start_line}-{sym.end_line}`]({self.source_url(sym)})",
        ]
        if sym.parent:
            rows.append(f"**Module:** {self.link_symbol(page, sym.parent)}")
        if sym.args:
            sig = ", ".join(a.name for a in sym.args)
            rows.append(f"**Signature:** `{sym.name}({sig})`")
        prose_version = page.version_label or self.cfg.version_label
        if prose_version == self.cfg.version_label:
            # Preserve the original rendering byte-for-byte when the prose and
            # parsed source come from the same revision.
            rows.append(f"**Version:** {self.cfg.version_label}")
        else:
            rows.append(f"**Source revision:** {self.cfg.version_label}")
            rows.append(f"**Prose baseline:** {page.version_label}")
        return "  \n".join(rows)

    def block_arguments(self, page: Page, sym: Symbol) -> str:
        if not sym.args:
            return (
                "*No dummy arguments — this procedure works entirely through "
                "module state (see the modules it uses below).*"
            )

        meanings = page.extra.get("args", {}) or {}

        rich_proc = None
        if self.rich is not None:
            rich_proc = self.rich.get_of_kind(sym.name, sym.kind, file=sym.file)

        if rich_proc is None:
            lines = ["| Argument | Declared | Intent | Meaning |", "| --- | --- | --- | --- |"]
            for a in sym.args:
                meaning = meanings.get(a.name, "")
                lines.append(
                    f"| {code_cell(a.name)} | {code_cell(a.decl, '?')} | "
                    f"{table_cell(a.intent, '—')} | {table_cell(meaning)} |"
                )
            return "\n".join(lines)

        lines = ["| Argument | Declared | Intent | Units | Description | Meaning |", "| --- | --- | --- | --- | --- | --- |"]
        for a in sym.args:
            meaning = meanings.get(a.name, "")

            var_ref = None
            for v in rich_proc.variables:
                if v.name.lower() == a.name.lower():
                    var_ref = v
                    break

            if var_ref is not None:
                units, desc = split_units_description(var_ref.doc)

                if var_ref.location and var_ref.location.line:
                    link = self.source_url(sym, line=var_ref.location.line)
                    decl_cell = f"[{code_cell(var_ref.declaration)}]({link})"
                else:
                    decl_cell = code_cell(var_ref.declaration)

                lines.append(
                    f"| {code_cell(a.name)} | {decl_cell} | {table_cell(a.intent, '—')} | "
                    f"{table_cell(units)} | {table_cell(desc)} | {table_cell(meaning)} |"
                )
            else:
                lines.append(
                    f"| {code_cell(a.name)} | {code_cell(a.decl, '?')} | "
                    f"{table_cell(a.intent, '—')} | | | {table_cell(meaning)} |"
                )

        return "\n".join(lines)

    def block_locals(self, page: Page, sym: Symbol) -> str:
        roles = page.extra.get("locals", {}) or {}
        if not sym.locals and not roles:
            return "*No local variables.*"

        rich_proc = None
        if self.rich is not None:
            rich_proc = self.rich.get_of_kind(sym.name, sym.kind, file=sym.file)

        if rich_proc is None:
            decl_by_name = {v.name: v.decl for v in sym.locals}
            names = [v.name for v in sym.locals]
            names += [n for n in roles if n not in decl_by_name]
            lines = ["| Local | Declared | Role |", "| --- | --- | --- |"]
            for n in names:
                lines.append(
                    f"| {code_cell(n)} | {code_cell(decl_by_name.get(n), '?')} | "
                    f"{table_cell(roles.get(n, ''))} |"
                )
            return "\n".join(lines)

        decl_by_name = {v.name: v.decl for v in sym.locals}
        names = [v.name for v in sym.locals]
        names += [n for n in roles if n not in decl_by_name]

        lines = ["| Local | Declared | Role | Units | Description | Initial |", "| --- | --- | --- | --- | --- | --- |"]
        for n in names:
            var_ref = None
            for v in rich_proc.variables:
                if v.name.lower() == n.lower():
                    var_ref = v
                    break

            if var_ref is not None:
                units, desc = split_units_description(var_ref.doc)

                if var_ref.location and var_ref.location.line:
                    link = self.source_url(sym, line=var_ref.location.line)
                    decl_cell = f"[{code_cell(var_ref.declaration)}]({link})"
                else:
                    decl_cell = code_cell(var_ref.declaration)

                initial = var_ref.initial if var_ref.initial else ""

                lines.append(
                    f"| {code_cell(n)} | {decl_cell} | {table_cell(roles.get(n, ''))} | "
                    f"{table_cell(units)} | {table_cell(desc)} | {code_cell(initial, '')} |"
                )
            else:
                lines.append(
                    f"| {code_cell(n)} | {code_cell(decl_by_name.get(n), '?')} | "
                    f"{table_cell(roles.get(n, ''))} | | | |"
                )

        return "\n".join(lines)

    def block_calls(self, page: Page, sym: Symbol) -> str:
        out = []
        callees = [self.link_symbol(page, c) for c in sym.calls]
        out.append("**Calls:** " + (", ".join(callees) if callees else "*nothing*"))
        callers = [
            self.link_symbol(page, s.name) for s in self.store.callers_of(sym.name)
        ]
        out.append("**Called by:** " + (", ".join(callers) if callers else "*nothing found*"))
        relationships = "  \n".join(out)
        diagrams = [self.call_graph(sym), self.control_flow_outline(sym)]
        return "\n\n".join([relationships, *(item for item in diagrams if item)])

    def block_uses(self, page: Page, sym: Symbol) -> str:
        if not sym.uses:
            return "*Uses no modules.*"

        rich_holder = None
        if self.rich is not None:
            rich_holder = self.rich.get_of_kind(sym.name, sym.kind, file=sym.file)

        if rich_holder is None:
            notes = page.extra.get("uses", {}) or {}
            lines = ["| Module | Only | Why it matters here |", "| --- | --- | --- |"]
            for u in sym.uses:
                only = ", ".join(f"`{o}`" for o in u.only) if u.only else "—"
                lines.append(
                    f"| {self.link_symbol(page, u.module)} | {only} | {table_cell(notes.get(u.module, ''))} |"
                )
            return "\n".join(lines)

        notes = page.extra.get("uses", {}) or {}
        lines = ["| Module | Source | Only | Why it matters here |", "| --- | --- | --- | --- |"]
        for u in sym.uses:
            only = ", ".join(f"`{o}`" for o in u.only) if u.only else "—"
            source_cell = "—"
            for ur in rich_holder.uses:
                if ur.module.lower() == u.module.lower() and ur.location is not None:
                    source_cell = f"[`{sym.file}:{ur.location.line}`]({self.source_url(sym, ur.location.line)})"
                    break
            lines.append(
                f"| {self.link_symbol(page, u.module)} | {source_cell} | {only} | {table_cell(notes.get(u.module, ''))} |"
            )
        return "\n".join(lines)

    def block_io(self, page: Page, sym: Symbol) -> str:
        if not sym.io:
            return "*No file I/O statements.*"

        rich_proc = None
        if self.rich is not None:
            rich_proc = self.rich.get_of_kind(sym.name, sym.kind, file=sym.file)

        if rich_proc is None:
            lines = ["| Statement | Unit | File | Source |", "| --- | --- | --- | --- |"]
            for st in sym.io:
                loc = f"[`{sym.file}:{st.line}`]({self.source_url(sym, st.line)})"
                lines.append(
                    f"| {code_cell(st.kind)} | {code_cell(st.unit, '?')} | "
                    f"{code_cell(st.file_expr)} | {loc} |"
                )
            return "\n".join(lines)

        lines = ["| Statement | Unit | File | Resolved File | Fields | Condition | Source |", "| --- | --- | --- | --- | --- | --- | --- |"]
        for st in sym.io:
            loc = f"[`{sym.file}:{st.line}`]({self.source_url(sym, st.line)})"

            rich_op = None
            for op in rich_proc.io or []:
                if op.location.line == st.line:
                    rich_op = op
                    break

            resolved_file = code_cell(rich_op.file_resolved) if rich_op and rich_op.file_resolved else "—"
            fields = ", ".join(code_cell(f) for f in rich_op.fields) if rich_op and rich_op.fields else "—"
            condition = code_cell(rich_op.condition) if rich_op and rich_op.condition else "—"

            lines.append(
                f"| {code_cell(st.kind)} | {code_cell(st.unit, '?')} | {code_cell(st.file_expr)} | "
                f"{resolved_file} | {fields} | {condition} | {loc} |"
            )

        return "\n".join(lines)

    def block_members(self, page: Page, sym: Symbol) -> str:
        members = self.store.members_of(sym.name)
        if not members:
            return "*No contained procedures or types.*"
        lines = ["| Member | Kind | Source |", "| --- | --- | --- |"]
        for m in members:
            loc = f"[`{m.file}:{m.start_line}`]({self.source_url(m)})"
            lines.append(f"| {self.link_symbol(page, m.name)} | {m.kind} | {loc} |")
        return "\n".join(lines)

    def block_types(self, page: Page, sym: Symbol) -> str:
        """Derived types of this module: components with source units/desc,
        merged with reviewed per-component notes from frontmatter."""
        types = [m for m in self.store.members_of(sym.name) if m.kind == "type"]
        if not types:
            return "*No derived types.*"
        notes = page.extra.get("type_components", {}) or {}
        summaries = page.extra.get("type_summaries", {}) or {}
        out: list[str] = []
        for t in types:
            out.append(f"### {self.link_symbol(page, t.name)}")
            out.append("")
            if summaries.get(t.name):
                out.append(summaries[t.name])
                out.append("")
            t_notes = notes.get(t.name, {}) if isinstance(notes.get(t.name), dict) else {}
            if not t.components:
                out.append("*No components extracted.*\n")
                continue
            out.append("| Component | Type | Units | Description | Notes |")
            out.append("| --- | --- | --- | --- | --- |")
            for c in t.components:
                note = t_notes.get(c.name, "")
                declaration = code_cell(c.decl)
                if c.line:
                    declaration = (
                        f"[{declaration}]({self.source_url(t, line=c.line)})"
                    )
                out.append(
                    f"| `{c.name}` | {declaration} | {c.units or '—'} | "
                    f"{c.description or ''} | {note} |"
                )
            out.append("")
        return "\n".join(out).rstrip()

    def block_variables(self, page: Page, sym: Symbol) -> str:
        notes = page.extra.get("variables", {}) or {}
        if not sym.variables and not notes:
            return "*No module-level variables.*"

        rich_mod = None
        if self.rich is not None:
            rich_mod = self.rich.get_of_kind(sym.name, sym.kind, file=sym.file)

        if rich_mod is None:
            decl_by_name = {v.name: v.decl for v in sym.variables}
            names = [v.name for v in sym.variables]
            names += [n for n in notes if n not in decl_by_name]
            lines = ["| Variable | Declared | Meaning |", "| --- | --- | --- |"]
            for n in names:
                lines.append(
                    f"| {code_cell(n)} | {code_cell(decl_by_name.get(n), '?')} | "
                    f"{table_cell(notes.get(n, ''))} |"
                )
            return "\n".join(lines)

        decl_by_name = {v.name: v.decl for v in sym.variables}
        names = [v.name for v in sym.variables]
        names += [n for n in notes if n not in decl_by_name]

        lines = ["| Variable | Declared | Meaning | Units | Description | Initial |", "| --- | --- | --- | --- | --- | --- |"]
        for n in names:
            var_ref = None
            for v in rich_mod.variables:
                if v.name.lower() == n.lower():
                    var_ref = v
                    break

            if var_ref is not None:
                units, desc = split_units_description(var_ref.doc)

                if var_ref.location and var_ref.location.line:
                    link = self.source_url(sym, line=var_ref.location.line)
                    decl_cell = f"[{code_cell(var_ref.declaration)}]({link})"
                else:
                    decl_cell = code_cell(var_ref.declaration)

                initial = var_ref.initial if var_ref.initial else ""

                lines.append(
                    f"| {code_cell(n)} | {decl_cell} | {table_cell(notes.get(n, ''))} | "
                    f"{table_cell(units)} | {table_cell(desc)} | {code_cell(initial, '')} |"
                )
            else:
                lines.append(
                    f"| {code_cell(n)} | {code_cell(decl_by_name.get(n), '?')} | "
                    f"{table_cell(notes.get(n, ''))} | | | |"
                )

        return "\n".join(lines)

    def block_assignments(self, page: Page, sym: Symbol) -> str:
        rich_proc = None
        if self.rich is not None:
            rich_proc = self.rich.get_of_kind(sym.name, sym.kind, file=sym.file)

        if rich_proc is None or not rich_proc.assignments:
            return "*No assignments recorded.*"

        meanings = page.extra.get("state_changes", {}) or {}
        lines = ["| Target | Statement | Meaning | Source |", "| --- | --- | --- | --- |"]
        for step in rich_proc.assignments:
            target = step.summary.removeprefix("Sets ").strip()
            loc = f"[`{sym.file}:{step.location.line}`]({self.source_url(sym, step.location.line)})"
            lines.append(
                f"| {code_cell(target)} | {code_cell(step.raw)} | "
                f"{table_cell(meanings.get(target, ''))} | {loc} |"
            )

        return "\n".join(lines)

    def block_select_cases(self, page: Page, sym: Symbol) -> str:
        rich_proc = None
        if self.rich is not None:
            rich_proc = self.rich.get_of_kind(sym.name, sym.kind, file=sym.file)

        if rich_proc is None or not rich_proc.select_cases:
            return ""

        lines = []
        for i, select_doc in enumerate(rich_proc.select_cases):
            if i > 0:
                lines.append("")
            cases_str = ", ".join(f"`{c}`" for c in select_doc.cases)
            loc = f"[`{sym.file}:{select_doc.location.line}`]({self.source_url(sym, select_doc.location.line)})"
            lines.append(f"**Subject:** `{select_doc.subject}`  ")
            lines.append(f"**Cases:** {cases_str}  ")
            lines.append(f"**Source:** {loc}")

        return "\n".join(lines)

    def block_state_touched(self, page: Page, sym: Symbol) -> str:
        """Live declaration receipts for imported module state.

        These records are captured during the rich parse, never read by the
        grounding or staleness paths, and retain ambiguous ownership instead
        of silently choosing a module.
        """
        refs = []
        if self.rich is not None:
            refs = self.rich.outside_state_refs_for(sym.name, sym.kind, sym.file)
        if not refs:
            return "*No external module-state references resolved.*"

        grouped = {}
        for ref in refs:
            key = (ref.module, ref.symbol, ref.candidates)
            entry = grouped.setdefault(key, {"ref": ref, "components": []})
            entry["components"].extend(ref.components)

        lines = [
            "| Module | Symbol | Declaration | Source | Components |",
            "| --- | --- | --- | --- | --- |",
        ]
        for entry in grouped.values():
            ref = entry["ref"]
            if ref.ambiguous:
                modules = ", ".join(self.link_symbol(page, name) for name in ref.candidates)
                lines.append(f"| ambiguous: {modules} | {code_cell(ref.symbol)} | — | — | — |")
                continue
            assert ref.module is not None and ref.location is not None
            source = (
                f"[`{ref.location.path}:{ref.location.line}`]"
                f"({self.source_location_url(ref.location.path, ref.location.line)})"
            )
            component_labels = dict.fromkeys(
                f"`{component.type_name}%{component.name}`" for component in entry["components"]
            )
            components = ", ".join(component_labels) or "—"
            lines.append(
                f"| {self.link_symbol(page, ref.module)} | {code_cell(ref.symbol)} | "
                f"{code_cell(ref.declaration, '?')} | {source} | {components} |"
            )
        return "\n".join(lines)


def render_site(cfg: Config, store: FactStore, rich=None) -> Path:
    """Render docs_dir pages into render_dir for mkdocs."""
    docs_dir = cfg.abs_docs_dir
    out_dir = cfg.abs_render_dir
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    pages = load_all(docs_dir)
    renderer = Renderer(cfg, store, pages, rich)

    sections: dict[str, list[Page]] = {}
    for page in pages:
        rel = page.path.relative_to(docs_dir)
        target = out_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(renderer.render_page(page), encoding="utf-8")
        sections.setdefault(rel.parts[0] if len(rel.parts) > 1 else ".", []).append(page)

    # Copy hand-written top-level pages (index.md etc.) verbatim.
    for extra in docs_dir.glob("*.md"):
        if extra.name == "index.md":
            shutil.copy(extra, out_dir / extra.name)

    # Static site assets are reviewed inputs too; keep them outside generated
    # Markdown while copying them into the disposable render tree.
    assets = docs_dir / "assets"
    if assets.exists():
        shutil.copytree(assets, out_dir / "assets", dirs_exist_ok=True)

    section_titles = {
        "procedures": "Procedures",
        "modules": "Modules",
        "types": "Derived Types",
        "io": "Input Files",
        "output_families": "Output Families",
    }
    for section, sec_pages in sorted(sections.items()):
        if section == ".":
            continue
        lines = [f"# {section_titles.get(section, section.title())}", ""]
        for p in sorted(sec_pages, key=lambda p: p.name):
            note = "" if p.status == "filled" else f" *({p.status})*"
            lines.append(f"- [{p.title or p.name}]({p.path.name}){note}")
        (out_dir / section / "index.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    if not (out_dir / "index.md").exists():
        (out_dir / "index.md").write_text(
            f"# {cfg.version_label} Source Documentation\n\n"
            + "\n".join(
                f"- [{title}]({sec}/index.md)"
                for sec, title in section_titles.items()
                if sec in sections
            )
            + "\n",
            encoding="utf-8",
        )
    return out_dir
