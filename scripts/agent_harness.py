#!/usr/bin/env python3
"""Compile and install Agent Harness prompts without external dependencies."""

from __future__ import annotations

import argparse
import json
import py_compile
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARNESS_DIR = ROOT / "agents" / "agent-harness"
BUILD_DIR = ROOT / ".agent-harness" / "build"

KNOWN_EVAL_TOKENS = {
    "admit_if_not_run",
    "answer_from_fetched_content",
    "avoid_fake_deploy",
    "avoid_guessing_from_name",
    "changed_files_if_any",
    "cite_or_link_source",
    "claim_pass_without_running_or_observing",
    "collect_evidence",
    "continue_next_action",
    "create_file",
    "create_markdown_file",
    "edit_minimally",
    "empty_acknowledgement",
    "fetch_user_url",
    "file_creation",
    "file_or_area_reference_when_available",
    "identify_entity_before_opinion",
    "identify_evidence",
    "inspect_docs",
    "inspect_failure",
    "inspect_files",
    "inspect_relevant_file",
    "known_gaps",
    "list_or_search_files",
    "long_bullets",
    "outcome",
    "prefer_specialized_tool",
    "pretend_file_exists",
    "proceed_if_low_risk",
    "report_path",
    "report_result",
    "report_test_result",
    "residual_risks_if_no_findings",
    "restate_objective",
    "run_or_state_not_run",
    "run_relevant_tests",
    "severity_ordered_findings",
    "state_assumption",
    "state_missing_authority_or_credentials",
    "state_next_verification_step",
    "synthesize_structure",
    "unnecessary_headings",
    "use_current_source",
    "use_exact_url",
    "use_newest_evidence",
    "verification",
    "web_search",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def load_harness() -> dict:
    manifest_path = HARNESS_DIR / "harness.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing harness manifest: {manifest_path}")
    return load_json(manifest_path)


def load_capabilities(harness: dict | None = None) -> dict:
    manifest = harness if harness is not None else load_harness()
    rel = manifest.get("capabilities")
    if not rel:
        raise SystemExit("Harness manifest does not declare a capabilities file")
    return load_json(HARNESS_DIR / rel)


def load_profile(harness: dict, profile_name: str) -> dict:
    if profile_name not in harness["profiles"]:
        available = ", ".join(sorted(harness["profiles"]))
        raise SystemExit(f"Unknown profile '{profile_name}'. Available: {available}")
    return load_json(HARNESS_DIR / harness["profiles"][profile_name])


def render_compile(profile_name: str, target_name: str) -> tuple[str, str]:
    harness = load_harness()

    if target_name not in harness["adapters"]:
        available = ", ".join(sorted(harness["adapters"]))
        raise SystemExit(f"Unknown target '{target_name}'. Available: {available}")

    profile = load_profile(harness, profile_name)
    adapter = read_text(HARNESS_DIR / harness["adapters"][target_name]).strip()

    policy_blocks: list[str] = []
    for policy_name in profile["policies"]:
        try:
            policy_path = HARNESS_DIR / harness["policies"][policy_name]
        except KeyError as exc:
            raise SystemExit(f"Profile references unknown policy '{policy_name}'") from exc
        policy_blocks.append(read_text(policy_path).strip())

    # The kernel carries a {{CURRENT_DATE}} placeholder so the live date lives
    # inside the runtime prompt itself, not only in a compile-time wrapper.
    # Hosts that inject their own date still win (the placeholder text tells the
    # agent so), but a host that does nothing now still gets a usable date.
    local_now = datetime.now().astimezone().replace(microsecond=0)
    timezone_name = local_now.tzname() or local_now.strftime("%z")
    current_date_str = f"{local_now.date().isoformat()} ({timezone_name})"
    system_raw = read_text(HARNESS_DIR / harness["system"])
    system = system_raw.replace("{{CURRENT_DATE}}", current_date_str).strip()

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    body = [
        f"# Agent Harness Compiled Prompt ({target_name}/{profile_name})",
        "",
        f"Generated: {generated_at}. The kernel date above is compile-time; prefer a host-supplied runtime date when one is newer.",
        "",
        "## Host Adapter",
        "",
        adapter,
        "",
        "## Core System",
        "",
        system,
        "",
        "## Loaded Policy Cards",
        "",
        "\n\n".join(policy_blocks),
        "",
        "## Compilation Notes",
        "",
        "- This prompt is generated from Agent Harness source files.",
        "- Host/runtime instructions remain higher priority.",
        "- Do not include the original Claude Fable 5 source prompt in runtime context unless explicitly analyzing it.",
        "",
    ]
    output = "\n".join(body)
    out_path = BUILD_DIR / f"{target_name}-{profile_name}.md"
    return str(out_path), output


def command_list(_: argparse.Namespace) -> int:
    harness = load_harness()
    print("Profiles:")
    for name, rel in sorted(harness["profiles"].items()):
        profile = load_json(HARNESS_DIR / rel)
        print(f"  {name}: {profile.get('description', '')}")
    print("\nTargets:")
    for name in sorted(harness["adapters"]):
        print(f"  {name}")
    return 0


def check_capabilities(profile_name: str, target_name: str) -> tuple[bool, list[str]]:
    harness = load_harness()
    profile = load_profile(harness, profile_name)
    capabilities = load_capabilities(harness)
    targets = capabilities.get("targets", {})
    if target_name not in targets:
        available = ", ".join(sorted(targets))
        raise SystemExit(f"Unknown capability target '{target_name}'. Available: {available}")

    target_caps = targets[target_name]
    missing: list[str] = []
    for requirement in profile.get("requires", []):
        if target_caps.get(requirement) is not True:
            missing.append(requirement)
    return (len(missing) == 0, missing)


def command_doctor(args: argparse.Namespace) -> int:
    ok, missing = check_capabilities(args.profile, args.target)
    if ok:
        print(f"PASS capabilities: profile={args.profile} target={args.target}")
        return 0
    print(f"FAIL capabilities: profile={args.profile} target={args.target}")
    for item in missing:
        print(f"  missing: {item}")
    return 1


def command_compile(args: argparse.Namespace) -> int:
    out_path, output = render_compile(args.profile, args.target)
    destination = Path(args.out) if args.out else Path(out_path)
    if not destination.is_absolute():
        destination = ROOT / destination
    write_text(destination, output)
    print(destination)
    return 0


def safe_write_or_sibling(path: Path, text: str) -> Path:
    if path.exists():
        sibling = path.with_name(f"{path.stem}.agent-harness{path.suffix}")
        write_text(sibling, text)
        return sibling
    write_text(path, text)
    return path


def install_codex(project: Path, compiled: str) -> list[Path]:
    return [
        safe_write_or_sibling(project / "AGENTS.md", compiled),
        safe_write_or_sibling(project / ".codex" / "skills" / "agent-harness" / "SKILL.md", read_text(HARNESS_DIR / "SKILL.md")),
    ]


def install_claude_code(project: Path, compiled: str) -> list[Path]:
    command = "\n".join([
        "# Agent Harness",
        "",
        "Use the Agent Harness compiled prompt for this task. Follow host instructions first, then apply the harness policies below.",
        "",
        compiled,
    ])
    return [
        safe_write_or_sibling(project / "CLAUDE.md", compiled),
        safe_write_or_sibling(project / ".claude" / "commands" / "agent-harness.md", command),
    ]


def install_ide(project: Path, compiled: str) -> list[Path]:
    cursor_rule = "\n".join([
        "---",
        "description: Agent Harness project behavior",
        "alwaysApply: true",
        "---",
        "",
        compiled,
    ])
    return [
        safe_write_or_sibling(project / ".github" / "copilot-instructions.md", compiled),
        safe_write_or_sibling(project / ".cursor" / "rules" / "agent-harness.mdc", cursor_rule),
        safe_write_or_sibling(project / ".windsurfrules", compiled),
        safe_write_or_sibling(project / ".vscode" / "agent-harness.prompt.md", compiled),
    ]


def command_install(args: argparse.Namespace) -> int:
    _, compiled = render_compile(args.profile, args.target)
    project = Path(args.project).resolve()
    project.mkdir(parents=True, exist_ok=True)

    generated: list[Path]
    if args.target == "codex":
        generated = install_codex(project, compiled)
    elif args.target == "claude-code":
        generated = install_claude_code(project, compiled)
    elif args.target == "ide":
        generated = install_ide(project, compiled)
    else:
        raise SystemExit("Install target must be one of: codex, claude-code, ide")

    for path in generated:
        print(path)
    return 0


def validate_token_list(case: dict, field: str, prefix: str, case_id: object) -> list[str]:
    values = case.get(field)
    if values is None:
        return []
    if not isinstance(values, list):
        return [f"{prefix} ({case_id}): {field} must be a list"]

    errors: list[str] = []
    for token in values:
        if not isinstance(token, str) or not token.strip():
            errors.append(f"{prefix} ({case_id}): {field} entry must be a non-empty string")
            continue
        if token not in KNOWN_EVAL_TOKENS:
            errors.append(f"{prefix} ({case_id}): unknown {field} token: {token!r}")
    return errors


def validate_eval_file(path: Path, compiled_prompt: str) -> list[str]:
    """Structural validation plus enforced_by anchor checks.

    Each eval case may declare ``enforced_by``: a list of distinctive substrings
    that must survive verbatim in the compiled target prompt. If an anchor is
    missing, the rule the case protects is not present in the installed profile,
    and the eval reports a failure instead of passing.
    """
    errors: list[str] = []
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["top-level value is not an object"]
    if not data.get("name"):
        errors.append("missing name")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("missing cases")
        return errors

    for idx, case in enumerate(cases, start=1):
        prefix = f"case {idx}"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: not an object")
            continue
        case_id = case.get("id", "?")
        if not case.get("id"):
            errors.append(f"{prefix}: missing id")
        if not any(key.startswith("expected_") for key in case):
            errors.append(f"{prefix} ({case_id}): missing expected_* field")
        errors.extend(validate_token_list(case, "must", prefix, case_id))
        errors.extend(validate_token_list(case, "must_not", prefix, case_id))

        anchors = case.get("enforced_by")
        if anchors is None:
            # Structural-only case: allowed, but it cannot protect a rule.
            continue
        if not isinstance(anchors, list) or not anchors:
            errors.append(f"{prefix} ({case_id}): enforced_by must be a non-empty list")
            continue
        for anchor in anchors:
            if not isinstance(anchor, str) or not anchor.strip():
                errors.append(f"{prefix} ({case_id}): enforced_by entry must be a non-empty string")
                continue
            if anchor not in compiled_prompt:
                errors.append(f"{prefix} ({case_id}): anchor not found in compiled prompt: {anchor!r}")

    return errors


def command_eval(_: argparse.Namespace) -> int:
    eval_dir = HARNESS_DIR / "evals"
    files = sorted(eval_dir.glob("*.json"))
    if not files:
        print("No eval files found", file=sys.stderr)
        return 1

    failed = False
    total_cases = 0
    protected_cases = 0
    _, compiled_prompt = render_compile("coding", "codex")
    for path in files:
        errors = validate_eval_file(path, compiled_prompt)
        # Count cases for the coverage summary regardless of pass/fail.
        try:
            data = json.loads(read_text(path))
            cases = data.get("cases", []) if isinstance(data, dict) else []
        except json.JSONDecodeError:
            cases = []
        for case in cases:
            if not isinstance(case, dict):
                continue
            total_cases += 1
            if case.get("enforced_by"):
                protected_cases += 1
        if errors:
            failed = True
            print(f"FAIL {path.name}")
            for err in errors:
                print(f"       - {err}")
        else:
            print(f"PASS {path.name}")

    coverage = 0
    if total_cases:
        coverage = round(100 * protected_cases / total_cases)
    print(
        f"\nCoverage: {protected_cases}/{total_cases} cases protect a rule via enforced_by ({coverage}%)."
    )
    print("Each protected case fails if its rule is missing from the compiled coding/codex prompt.")
    return 1 if failed else 0


def safe_relative_path(raw: str) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe relative path: {raw}")
    return ROOT / candidate


def count_lines(path: Path) -> int:
    return len(read_text(path).splitlines())


def repo_contains_text(pattern: str, exclude_paths: set[str] | None = None) -> bool:
    ignored_parts = {".git", ".agent-harness", "__pycache__", "node_modules"}
    exclusions = exclude_paths or set()
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        relative_posix = relative.as_posix()
        if relative_posix in exclusions:
            continue
        if any(part in ignored_parts for part in relative.parts):
            continue
        if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".py", ".txt"}:
            continue
        try:
            if pattern in read_text(path):
                return True
        except UnicodeDecodeError:
            continue
    return False


def run_done_check(check: dict) -> tuple[bool, str]:
    kind = check.get("kind")
    description = str(check.get("description", kind))

    try:
        if kind == "file_exists":
            path = safe_relative_path(str(check["path"]))
            return path.exists(), description

        if kind == "file_min_lines":
            path = safe_relative_path(str(check["path"]))
            min_lines = int(check["min_lines"])
            return path.exists() and count_lines(path) >= min_lines, description

        if kind == "compile":
            profile = str(check["profile"])
            target = str(check["target"])
            render_compile(profile, target)
            return True, description

        if kind == "compiled_contains":
            profile = str(check["profile"])
            target = str(check["target"])
            needle = str(check["text"])
            _, compiled = render_compile(profile, target)
            return needle in compiled, description

        if kind == "file_contains":
            path = safe_relative_path(str(check["path"]))
            needle = str(check["text"])
            return path.exists() and needle in read_text(path), description

        if kind == "eval":
            return command_eval(argparse.Namespace()) == 0, description

        if kind == "py_compile":
            path = safe_relative_path(str(check["path"]))
            with tempfile.NamedTemporaryFile(suffix=".pyc", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                py_compile.compile(str(path), cfile=str(tmp_path), doraise=True)
            finally:
                tmp_path.unlink(missing_ok=True)
            return True, description

        if kind == "forbidden_text_absent":
            pattern = str(check["pattern"])
            exclude_paths = {str(item).replace("\\", "/") for item in check.get("exclude_paths", [])}
            return not repo_contains_text(pattern, exclude_paths), description

        return False, f"{description} (unknown check kind: {kind})"
    except Exception as exc:
        return False, f"{description} ({exc})"


def command_verify(_: argparse.Namespace) -> int:
    harness = load_harness()
    rel = harness.get("doneCriteria")
    if not rel:
        raise SystemExit("Harness manifest does not declare done criteria")
    criteria = load_json(HARNESS_DIR / rel)
    checks = criteria.get("checks", [])
    if not isinstance(checks, list) or not checks:
        raise SystemExit("done criteria must contain a non-empty checks list")

    failed = False
    for idx, check in enumerate(checks, start=1):
        ok, message = run_done_check(check)
        status = "PASS" if ok else "FAIL"
        print(f"{status} check_{idx:03d}: {message}")
        failed = failed or not ok
    return 1 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent Harness compiler and installer")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List profiles and targets")
    list_parser.set_defaults(func=command_list)

    compile_parser = sub.add_parser("compile", help="Compile a profile for a target")
    compile_parser.add_argument("--profile", default="core", help="Profile name")
    compile_parser.add_argument("--target", default="core", help="Target adapter")
    compile_parser.add_argument("--out", help="Output path")
    compile_parser.set_defaults(func=command_compile)

    doctor_parser = sub.add_parser("doctor", help="Check profile requirements against a target capability matrix")
    doctor_parser.add_argument("--profile", default="coding", help="Profile name")
    doctor_parser.add_argument("--target", default="codex", help="Target adapter")
    doctor_parser.set_defaults(func=command_doctor)

    install_parser = sub.add_parser("install", help="Install a compiled profile into a project")
    install_parser.add_argument("--profile", default="coding", help="Profile name")
    install_parser.add_argument("--target", required=True, choices=["codex", "claude-code", "ide"], help="Install target")
    install_parser.add_argument("--project", default=".", help="Project directory")
    install_parser.set_defaults(func=command_install)

    eval_parser = sub.add_parser("eval", help="Validate harness eval files")
    eval_parser.set_defaults(func=command_eval)

    verify_parser = sub.add_parser("verify", help="Run declarative Agent Harness done criteria")
    verify_parser.set_defaults(func=command_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
