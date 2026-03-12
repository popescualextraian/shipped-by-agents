#!/usr/bin/env python3
"""REST API test manager — inventory CRUD and test runner for Hurl files."""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = SKILL_DIR / "templates"

DEFAULT_TEST_DIR = "integration-tests"


def find_test_dir():
    """Find integration-tests directory by walking up from cwd."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / DEFAULT_TEST_DIR
        if (candidate / "inventory.json").exists():
            return candidate
    return cwd / DEFAULT_TEST_DIR


def load_inventory(test_dir):
    """Load inventory.json from test directory."""
    inv_path = test_dir / "inventory.json"
    if not inv_path.exists():
        print(f"Error: No inventory.json found at {inv_path}")
        print("Run 'init <base_url>' first.")
        sys.exit(1)
    with open(inv_path, "r") as f:
        return json.load(f)


def save_inventory(test_dir, inventory):
    """Save inventory.json to test directory."""
    inv_path = test_dir / "inventory.json"
    with open(inv_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Inventory saved: {inv_path}")


def cmd_init(args):
    """Initialize integration-tests directory with inventory."""
    test_dir = Path.cwd() / DEFAULT_TEST_DIR
    if (test_dir / "inventory.json").exists():
        print(f"Already initialized: {test_dir}")
        return

    test_dir.mkdir(parents=True, exist_ok=True)

    template = TEMPLATES_DIR / "inventory.template.json"
    with open(template, "r") as f:
        inventory = json.load(f)
    inventory["base_url"] = args.base_url
    save_inventory(test_dir, inventory)

    for suite in ["smoke", "crud", "validation"]:
        (test_dir / suite).mkdir(exist_ok=True)

    print(f"Initialized: {test_dir}")
    print(f"Base URL: {args.base_url}")
    print("Created suites: smoke, crud, validation")


def cmd_add(args):
    """Add a test to the inventory."""
    test_dir = find_test_dir()
    inventory = load_inventory(test_dir)

    for t in inventory["tests"]:
        if t["name"] == args.name:
            print(f"Error: Test '{args.name}' already exists.")
            sys.exit(1)

    suite_dir = test_dir / args.suite
    suite_dir.mkdir(parents=True, exist_ok=True)

    entry = {
        "name": args.name,
        "suite": args.suite,
        "file": f"{args.suite}/{args.name}.hurl",
        "method": args.method.upper(),
        "endpoint": args.endpoint,
        "description": args.description,
    }
    inventory["tests"].append(entry)
    save_inventory(test_dir, inventory)
    print(f"Added test: {args.name} ({args.method.upper()} {args.endpoint}) -> {entry['file']}")


def cmd_remove(args):
    """Remove a test from the inventory."""
    test_dir = find_test_dir()
    inventory = load_inventory(test_dir)

    found = None
    for i, t in enumerate(inventory["tests"]):
        if t["name"] == args.name:
            found = i
            break

    if found is None:
        print(f"Error: Test '{args.name}' not found in inventory.")
        sys.exit(1)

    entry = inventory["tests"].pop(found)
    save_inventory(test_dir, inventory)

    hurl_file = test_dir / entry["file"]
    if hurl_file.exists():
        if args.keep_file:
            print(f"Removed from inventory (file kept): {entry['file']}")
        else:
            hurl_file.unlink()
            print(f"Removed from inventory and deleted: {entry['file']}")
    else:
        print(f"Removed from inventory: {args.name}")


def cmd_list(args):
    """List tests from inventory."""
    test_dir = find_test_dir()
    inventory = load_inventory(test_dir)

    tests = inventory["tests"]

    if args.suite:
        tests = [t for t in tests if t["suite"] == args.suite]
    if args.method:
        tests = [t for t in tests if t["method"] == args.method.upper()]

    if not tests:
        print("No tests found matching criteria.")
        return

    print(f"Base URL: {inventory['base_url']}")
    print(f"{'Name':<25} {'Suite':<15} {'Method':<8} {'Endpoint':<25} {'Description'}")
    print("-" * 100)
    for t in tests:
        print(f"{t['name']:<25} {t['suite']:<15} {t['method']:<8} {t['endpoint']:<25} {t['description']}")
    print(f"\nTotal: {len(tests)} test(s)")


def _read_hurl_lines(filepath):
    """Read a .hurl file and return lines as a list (1-indexed via index+1)."""
    with open(filepath, "r") as f:
        return f.readlines()


def _build_assertion_labels(hurl_lines, assert_results):
    """Match assertion results (with line numbers) to .hurl file lines."""
    labels = []
    for a in assert_results:
        line_num = a.get("line", 0)
        success = a.get("success", False)
        # Get the source line text (1-indexed)
        if 0 < line_num <= len(hurl_lines):
            text = hurl_lines[line_num - 1].strip()
        else:
            text = f"(line {line_num})"
        icon = "PASS" if success else "FAIL"
        labels.append((icon, text, success))
    return labels


def run_hurl(test_dir, files, base_url):
    """Run hurl files and return exit code."""
    import tempfile

    if not files:
        print("No test files to run.")
        return 0

    if not shutil.which("hurl"):
        print("Error: Hurl CLI not found. Install from https://hurl.dev")
        sys.exit(1)

    if len(files) > 1:
        return _run_multi_tests(test_dir, files, base_url)

    # Single test: use --test with --report-json for structured assertion results
    with tempfile.TemporaryDirectory() as report_dir:
        cmd = [
            "hurl", "--test",
            "--variable", f"base_url={base_url}",
            "--error-format", "long",
            "--report-json", report_dir,
        ] + [str(f) for f in files]

        print(f"Running 1 test...\n")

        result = subprocess.run(cmd, cwd=str(test_dir), capture_output=True, text=True)
        _print_single_details(result, test_dir, files[0], report_dir)
    return result.returncode


def _print_single_details(result, test_dir, hurl_file, report_dir):
    """Print detailed output for a single test run."""
    passed = result.returncode == 0
    label = "PASSED" if passed else "FAILED"
    print(f"Result: {label}")

    # Parse the report JSON for structured assertion results
    report_data = None
    report_path = Path(report_dir)
    for json_file in report_path.glob("*.json"):
        with open(json_file, "r") as f:
            report_data = json.load(f)
        break

    if report_data and isinstance(report_data, list) and len(report_data) > 0:
        entry = report_data[0]

        # Show HTTP status and timing from the report
        entries = entry.get("entries", [])
        for e in entries:
            calls = e.get("calls", [])
            for call in calls:
                resp = call.get("response", {})
                http_ver = resp.get("http_version", "")
                status_code = resp.get("status", "")
                print(f"Status: {http_ver} {status_code}")

                timings = call.get("timings", {})
                total_us = timings.get("total", 0)
                if total_us:
                    print(f"Time: {total_us / 1000:.0f} ms")

                # Show response body (resolve store path if needed)
                body_ref = resp.get("body", "")
                if body_ref:
                    body_path = Path(report_dir) / body_ref
                    if body_path.exists():
                        body_content = body_path.read_text(encoding="utf-8", errors="replace")
                        # Try to pretty-print JSON
                        try:
                            parsed = json.loads(body_content)
                            formatted = json.dumps(parsed, indent=2)
                            # Truncate large responses
                            lines = formatted.splitlines()
                            if len(lines) > 30:
                                preview = "\n".join(lines[:30])
                                print(f"\nResponse body (first 30 lines of {len(lines)}):\n{preview}\n  ...")
                            else:
                                print(f"\nResponse body:\n{formatted}")
                        except (json.JSONDecodeError, ValueError):
                            if len(body_content) > 2000:
                                print(f"\nResponse body (first 2000 chars):\n{body_content[:2000]}\n  ...")
                            else:
                                print(f"\nResponse body:\n{body_content}")
                    else:
                        print(f"\nResponse body:\n{body_ref}")

            # Show assertion results matched to .hurl source lines
            asserts = e.get("asserts", [])
            if asserts:
                hurl_path = test_dir / hurl_file if not Path(hurl_file).is_absolute() else Path(hurl_file)
                hurl_lines = _read_hurl_lines(hurl_path)
                labels = _build_assertion_labels(hurl_lines, asserts)
                # Deduplicate assertions on the same line
                seen = set()
                unique_labels = []
                for icon, text, success in labels:
                    key = (text, success)
                    if key not in seen:
                        seen.add(key)
                        unique_labels.append((icon, text, success))

                print(f"\nAssertions ({len(unique_labels)}):")
                for icon, text, success in unique_labels:
                    print(f"  [{icon}] {text}")

    # Show failure details from stderr
    if not passed:
        stderr = result.stderr or ""
        stdout = result.stdout or ""
        details = stderr + stdout
        if details.strip():
            print(f"\nFailure output:")
            print(details.strip())


def _run_multi_tests(test_dir, files, base_url):
    """Run multiple tests individually, collecting per-test status and timing."""
    import time as _time

    results = []
    total_fail = 0

    print(f"Running {len(files)} test(s)...\n")
    print(f"{'Test':<35} {'Status':<10} {'HTTP':<10} {'Time'}")
    print("-" * 75)

    for f in files:
        name = Path(f).stem
        cmd = [
            "hurl", "--verbose",
            "--variable", f"base_url={base_url}",
            "--error-format", "long",
            str(f),
        ]

        start = _time.perf_counter()
        result = subprocess.run(cmd, cwd=str(test_dir), capture_output=True, text=True)
        elapsed_ms = (_time.perf_counter() - start) * 1000

        # Extract HTTP status from verbose stderr
        http_status = ""
        for line in (result.stderr or "").splitlines():
            if line.startswith("< HTTP/"):
                http_status = line.lstrip("< ").strip()
                break

        passed = result.returncode == 0
        label = "PASS" if passed else "FAIL"
        if not passed:
            total_fail += 1

        print(f"{name:<35} {label:<10} {http_status:<10} {elapsed_ms:.0f}ms")

        if not passed:
            # Collect failure details to show after the table
            results.append((name, result))

    print("-" * 75)
    total = len(files)
    print(f"Passed: {total - total_fail}/{total}  Failed: {total_fail}/{total}")

    # Show failure details
    for name, result in results:
        print(f"\n--- FAILURE: {name} ---")
        output = result.stderr or ""
        for line in output.splitlines():
            if "assert" in line.lower() or "error" in line.lower() or "actual" in line.lower() or "expected" in line.lower():
                print(f"  {line.strip()}")

    return 1 if total_fail > 0 else 0


def cmd_run_all(args):
    """Run all tests."""
    test_dir = find_test_dir()
    inventory = load_inventory(test_dir)

    files = [test_dir / t["file"] for t in inventory["tests"]]
    missing = [f for f in files if not f.exists()]
    if missing:
        print("Warning: Missing test files:")
        for f in missing:
            print(f"  - {f}")
        files = [f for f in files if f.exists()]

    rc = run_hurl(test_dir, files, inventory["base_url"])
    sys.exit(rc)


def cmd_run_suite(args):
    """Run all tests in a suite."""
    test_dir = find_test_dir()
    inventory = load_inventory(test_dir)

    tests = [t for t in inventory["tests"] if t["suite"] == args.suite]
    if not tests:
        print(f"No tests found in suite: {args.suite}")
        sys.exit(1)

    files = [test_dir / t["file"] for t in tests]
    files = [f for f in files if f.exists()]

    rc = run_hurl(test_dir, files, inventory["base_url"])
    sys.exit(rc)


def cmd_run(args):
    """Run specific test files."""
    test_dir = find_test_dir()
    inventory = load_inventory(test_dir)

    files = []
    for name in args.tests:
        found = [t for t in inventory["tests"] if t["name"] == name]
        if found:
            files.append(test_dir / found[0]["file"])
        else:
            p = test_dir / name
            if p.exists():
                files.append(p)
            else:
                print(f"Warning: Test '{name}' not found in inventory or as file.")

    if not files:
        print("No valid test files to run.")
        sys.exit(1)

    rc = run_hurl(test_dir, files, inventory["base_url"])
    sys.exit(rc)


def main():
    parser = argparse.ArgumentParser(
        description="REST API Test Manager — manage and run Hurl integration tests"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    p_init = subparsers.add_parser("init", help="Initialize test directory")
    p_init.add_argument("base_url", help="Base URL for the API")

    # add
    p_add = subparsers.add_parser("add", help="Add test to inventory")
    p_add.add_argument("name", help="Test name (used as filename)")
    p_add.add_argument("suite", help="Suite/folder name")
    p_add.add_argument("method", help="HTTP method")
    p_add.add_argument("endpoint", help="API endpoint")
    p_add.add_argument("description", help="Short description")

    # remove
    p_remove = subparsers.add_parser("remove", help="Remove test from inventory")
    p_remove.add_argument("name", help="Test name to remove")
    p_remove.add_argument("--keep-file", action="store_true", help="Keep .hurl file on disk")

    # list
    p_list = subparsers.add_parser("list", help="List tests in inventory")
    p_list.add_argument("--suite", help="Filter by suite")
    p_list.add_argument("--method", help="Filter by HTTP method")

    # run-all
    subparsers.add_parser("run-all", help="Run all tests")

    # run-suite
    p_rsuite = subparsers.add_parser("run-suite", help="Run all tests in a suite")
    p_rsuite.add_argument("suite", help="Suite name to run")

    # run
    p_run = subparsers.add_parser("run", help="Run specific tests")
    p_run.add_argument("tests", nargs="+", help="Test names or file paths")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "remove": cmd_remove,
        "list": cmd_list,
        "run-all": cmd_run_all,
        "run-suite": cmd_run_suite,
        "run": cmd_run,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
