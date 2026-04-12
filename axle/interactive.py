#!/usr/bin/env python3
"""Interactive arrow-key terminal UI for Axle CLI."""

import os
import sys
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple

# ANSI codes
_C   = '\033[1;96m'   # cyan bold  (selected / heading)
_G   = '\033[1;92m'   # green bold (run echo)
_DIM = '\033[2m'
_R   = '\033[0m'      # reset
_HC  = '\033[?25l'    # hide cursor
_SC  = '\033[?25m'    # show cursor
_CL  = '\r\033[K'     # clear to EOL


def _is_tty() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def _getch() -> str:
    """Read one keypress (Unix/macOS). Returns character or escape sequence."""
    try:
        import tty
        import termios
        import select as _sel

        fd  = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = os.read(fd, 1).decode('utf-8', errors='replace')
            if ch == '\x1b':
                r, _, _ = _sel.select([sys.stdin], [], [], 0.15)
                if r:
                    rest = os.read(fd, 3).decode('utf-8', errors='replace')
                    ch += rest
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except Exception:
        try:
            return input()
        except Exception:
            return 'q'


def _w(s: str) -> None:
    sys.stdout.write(s)
    sys.stdout.flush()


# ── Arrow-key list selector ─────────────────────────────────────────────────

def arrow_select(
    items: List[Any],
    title: str = "Select",
    format_item: Optional[Callable] = None,
    max_visible: int = 12,
) -> Optional[Any]:
    """
    Show an arrow-key navigable list and return the selected item.

    Keys:
      ↑ / k     move up
      ↓ / j     move down
      Enter     confirm selection
      q / Esc / Ctrl+C   cancel → returns None
    """
    if not _is_tty() or not items:
        return None

    fmt = format_item or str
    idx = 0          # mutable int — captured by reference in build()

    def build() -> List[str]:
        rows = [
            "",
            f"  {_C}{title}{_R}",
            f"  {'─' * 58}",
            f"  {_DIM}↑ ↓  navigate    Enter  select    q  quit{_R}",
            "",
        ]
        half  = max_visible // 2
        start = max(0, min(idx - half, len(items) - max_visible))
        end   = min(len(items), start + max_visible)
        start = max(0, end - max_visible)   # re-clamp near end

        if start > 0:
            rows.append(f"  {_DIM}  ↑  {start} more above…{_R}")

        for i in range(start, end):
            label = fmt(items[i])
            if i == idx:
                rows.append(f"  {_C}▶ {label}{_R}")
            else:
                rows.append(f"    {label}")

        if end < len(items):
            rows.append(f"  {_DIM}  ↓  {len(items) - end} more below…{_R}")

        rows.append("")
        return rows

    _w(_HC)
    rendered = build()
    _w('\n'.join(rendered))
    n = len(rendered)

    try:
        while True:
            ch = _getch()

            # erase previous render
            _w(f'\033[{n}A\r')
            for _ in range(n):
                _w(_CL + '\n')
            _w(f'\033[{n}A\r')

            if   ch in ('\x1b[A', 'k'):         idx = (idx - 1) % len(items)
            elif ch in ('\x1b[B', 'j'):         idx = (idx + 1) % len(items)
            elif ch in ('\r', '\n'):
                _w(_SC)
                return items[idx]
            elif ch in ('q', '\x03', '\x1b'):   # q, Ctrl-C, bare Esc
                _w(_SC)
                return None

            rendered = build()
            _w('\n'.join(rendered))
            n = len(rendered)

    except (KeyboardInterrupt, EOFError):
        return None
    finally:
        _w(_SC)


# ── Single-line input prompt ─────────────────────────────────────────────────

def _prompt(label: str, example: str = "") -> str:
    """Print a styled input prompt and return the user's response."""
    if example:
        print(f"  {_DIM}e.g.  {example}{_R}")
    _w(f"  {_C}▸{_R} ")
    try:
        return input().strip()
    except (EOFError, KeyboardInterrupt):
        return ""


# ── Public entry point ───────────────────────────────────────────────────────

def run_interactive(tools_dir: Path) -> Optional[Tuple[Any, List[str]]]:
    """
    Show the interactive tool picker and argument prompt.

    Returns:
        (DiscoveredTool, args_list) — ready to execute, or
        None                        — user cancelled
    """
    from axle.tool_discoverer import ToolDiscoverer

    discoverer = ToolDiscoverer(tools_dir)
    tools      = discoverer.list_tools()

    if not tools:
        return None

    # ── Format each tool row ─────────────────────────────────────────────────
    def fmt(tool) -> str:
        num   = tools.index(tool) + 1
        badge = "✅" if tool.metadata.get('has_contract') else "📜"
        name  = tool.name
        desc  = tool.description
        if len(desc) > 42:
            desc = desc[:42] + "…"
        return f"{num:2}.  {badge}  {name:<30}{_DIM}{desc}{_R}"

    # ── Show picker ──────────────────────────────────────────────────────────
    selected = arrow_select(
        tools,
        title="Axle CLI  —  Choose a tool to run",
        format_item=fmt,
        max_visible=14,
    )

    if selected is None:
        print()
        return None

    # ── Mini summary ─────────────────────────────────────────────────────────
    main_func   = selected.get_main_function()
    is_argparse = main_func and main_func.arg_count == 0
    is_contract = selected.metadata.get('has_contract')

    print(f"\n  {_C}▶ {selected.name}{_R}  —  {selected.description}\n")

    # ── Prompt for arguments based on tool type ──────────────────────────────
    if is_argparse:
        print(f"  {_DIM}Argparse-based tool — pass flags directly.{_R}")
        print(f"  {_DIM}Press Enter with no input to show --help.{_R}\n")
        raw  = _prompt(
            label="flags",
            example=f"axle {selected.name} --flag value",
        )
        args = raw.split() if raw else ["--help"]

    elif is_contract:
        print(f"  {_DIM}This tool takes a free-text prompt.{_R}\n")
        raw  = _prompt(
            label="prompt",
            example=f'axle {selected.name} "your prompt here"',
        )
        args = [raw] if raw else []

    else:
        funcs = [f.name for f in selected.functions]
        if funcs:
            print(f"  {_DIM}Available functions: {', '.join(funcs)}{_R}\n")
        raw  = _prompt(
            label="[function] [args…]",
            example=f"axle {selected.name}" + (f" {funcs[0]}" if funcs else ""),
        )
        args = raw.split() if raw else []

    # ── Echo the resolved command ────────────────────────────────────────────
    display = raw if (raw and raw != "--help") else ""
    cmd_str = f"axle {selected.name}" + (f" {display}" if display else "")
    print(f"\n  {_DIM}Running:{_R}  {_G}{cmd_str}{_R}\n")
    print("  " + "─" * 58 + "\n")

    return (selected, args)
