#!/usr/bin/env python3
"""Tool metadata extraction and storage system.

This module provides functionality to analyze Python tool scripts,
extract their metadata (commands, parameters, documentation), and
store it locally for easy access and search.
"""

import ast
import importlib.util
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Metadata storage location
METADATA_DIR = Path.home() / ".axle" / "metadata"
METADATA_FILE = METADATA_DIR / "tools_metadata.json"


def ensure_metadata_dir() -> None:
    """Ensure the metadata directory exists."""
    METADATA_DIR.mkdir(parents=True, exist_ok=True)


def extract_function_metadata(func_node: ast.FunctionDef) -> Dict[str, Any]:
    """Extract metadata from a function AST node.

    Args:
        func_node: AST function node

    Returns:
        Dictionary with function metadata
    """
    metadata = {
        "name": func_node.name,
        "args": [],
        "returns": None,
        "docstring": ast.get_docstring(func_node),
        "lineno": func_node.lineno,
    }

    # Extract arguments
    for arg in func_node.args.args:
        arg_info = {"name": arg.arg, "annotation": None}

        # Get type annotation if present
        if arg.annotation:
            if isinstance(arg.annotation, ast.Name):
                arg_info["annotation"] = arg.annotation.id
            elif isinstance(arg.annotation, ast.Subscript):
                arg_info["annotation"] = ast.unparse(arg.annotation)
            elif isinstance(arg.annotation, ast.Constant):
                arg_info["annotation"] = str(arg.annotation.value)

        metadata["args"].append(arg_info)

    # Extract return type
    if func_node.returns:
        if isinstance(func_node.returns, ast.Name):
            metadata["returns"] = func_node.returns.id
        elif isinstance(func_node.returns, ast.Subscript):
            metadata["returns"] = ast.unparse(func_node.returns)
        elif isinstance(func_node.returns, ast.Constant):
            metadata["returns"] = str(func_node.returns.value)

    return metadata


def extract_class_metadata(class_node: ast.ClassDef) -> Dict[str, Any]:
    """Extract metadata from a class AST node.

    Args:
        class_node: AST class node

    Returns:
        Dictionary with class metadata
    """
    metadata = {
        "name": class_node.name,
        "docstring": ast.get_docstring(class_node),
        "methods": [],
        "lineno": class_node.lineno,
    }

    # Extract methods
    for item in class_node.body:
        if isinstance(item, ast.FunctionDef):
            method_metadata = extract_function_metadata(item)
            metadata["methods"].append(method_metadata)

    return metadata


def analyze_tool_file(tool_path: Path) -> Dict[str, Any]:
    """Analyze a Python tool file and extract metadata.

    Args:
        tool_path: Path to the Python file

    Returns:
        Dictionary with tool metadata
    """
    try:
        source = tool_path.read_text()
    except Exception as e:
        return {
            "error": f"Could not read file: {e}",
            "path": str(tool_path),
        }

    metadata = {
        "path": str(tool_path),
        "name": tool_path.stem,
        "size_bytes": len(source),
        "last_modified": datetime.fromtimestamp(tool_path.stat().st_mtime).isoformat(),
        "functions": [],
        "classes": [],
        "imports": [],
        "docstring": None,
        "errors": [],
    }

    try:
        tree = ast.parse(source)

        # Get module docstring
        metadata["docstring"] = ast.get_docstring(tree)

        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    metadata["imports"].append({
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    metadata["imports"].append({
                        "type": "from_import",
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname,
                    })

        # Extract top-level functions and classes
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_metadata = extract_function_metadata(node)
                metadata["functions"].append(func_metadata)
            elif isinstance(node, ast.ClassDef):
                class_metadata = extract_class_metadata(node)
                metadata["classes"].append(class_metadata)

        # Check for required functions
        function_names = [f["name"] for f in metadata["functions"]]
        metadata["has_get_description"] = "get_description" in function_names
        metadata["has_main"] = "main" in function_names

        # Extract main function signature
        if metadata["has_main"]:
            for func in metadata["functions"]:
                if func["name"] == "main":
                    metadata["main_signature"] = func
                    break

    except SyntaxError as e:
        metadata["errors"].append(f"Syntax error at line {e.lineno}: {e.msg}")
    except Exception as e:
        metadata["errors"].append(f"Parse error: {e}")

    return metadata


def get_tools_directory() -> Path:
    """Get the tools directory path.

    Returns:
        Path to the tools directory
    """
    # Try to find tools directory relative to this module
    current_dir = Path(__file__).parent.parent
    tools_dir = current_dir / "tools"

    if tools_dir.exists():
        return tools_dir

    # Fallback to current directory / tools
    return Path.cwd() / "tools"


def scan_all_tools() -> Dict[str, Dict[str, Any]]:
    """Scan all tools in the tools directory and extract metadata.

    Returns:
        Dictionary mapping tool names to their metadata
    """
    tools_dir = get_tools_directory()

    if not tools_dir.exists():
        return {"error": f"Tools directory not found: {tools_dir}"}

    metadata = {}
    py_files = sorted(tools_dir.glob("*.py"))

    for py_file in py_files:
        if py_file.name == "__init__.py":
            continue

        tool_metadata = analyze_tool_file(py_file)
        metadata[py_file.stem] = tool_metadata

    return metadata


def load_metadata() -> Dict[str, Any]:
    """Load metadata from storage.

    Returns:
        Metadata dictionary
    """
    if not METADATA_FILE.exists():
        return {}

    try:
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_metadata(metadata: Dict[str, Any]) -> bool:
    """Save metadata to storage.

    Args:
        metadata: Metadata dictionary to save

    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_metadata_dir()
        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata, f, indent=2)
        return True
    except (IOError, TypeError) as e:
        print(f"Error saving metadata: {e}")
        return False


def update_metadata() -> Tuple[bool, str]:
    """Update the stored metadata by scanning all tools.

    Returns:
        Tuple of (success, message)
    """
    try:
        metadata = scan_all_tools()

        # Add metadata metadata
        metadata["_metadata"] = {
            "last_updated": datetime.now().isoformat(),
            "tool_count": len([k for k in metadata.keys() if not k.startswith("_")]),
            "axle_version": "1.2.0",
        }

        if save_metadata(metadata):
            tool_count = metadata.get("_metadata", {}).get("tool_count", 0)
            return True, f"Updated metadata for {tool_count} tool(s)"
        else:
            return False, "Failed to save metadata"

    except Exception as e:
        return False, f"Error updating metadata: {e}"


def get_tool_description_from_file(tool_path: Path) -> Optional[str]:
    """Get tool description by importing and calling get_description().

    Args:
        tool_path: Path to the tool file

    Returns:
        Tool description or None
    """
    try:
        spec = importlib.util.spec_from_file_location(tool_path.stem, tool_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "get_description"):
                return module.get_description()
    except Exception:
        pass

    return None


def format_tool_metadata(tool_name: str, metadata: Dict[str, Any]) -> str:
    """Format tool metadata for display.

    Args:
        tool_name: Name of the tool
        metadata: Tool metadata dictionary

    Returns:
        Formatted string for display
    """
    output = []
    output.append(f"\n{'=' * 60}")
    output.append(f"📋 Tool: {tool_name}")
    output.append(f"{'=' * 60}")

    if "error" in metadata:
        output.append(f"❌ {metadata['error']}")
        return "\n".join(output)

    # Basic info
    output.append(f"\n📁 File: {metadata.get('path', 'Unknown')}")
    output.append(f"📊 Size: {metadata.get('size_bytes', 0)} bytes")
    output.append(f"🕒 Last Modified: {metadata.get('last_modified', 'Unknown')}")

    # Tool contract
    output.append(f"\n📜 Tool Contract:")
    output.append(f"   get_description(): {'✅' if metadata.get('has_get_description') else '❌'}")
    output.append(f"   main(): {'✅' if metadata.get('has_main') else '❌'}")

    # Get actual description
    if metadata.get('has_get_description'):
        tool_path = Path(metadata['path'])
        description = get_tool_description_from_file(tool_path)
        if description:
            output.append(f"\n📝 Description:")
            output.append(f"   {description}")

    # Module docstring
    if metadata.get('docstring'):
        output.append(f"\n📄 Documentation:")
        for line in metadata['docstring'].split('\n'):
            output.append(f"   {line}")

    # Main function signature
    if metadata.get('main_signature'):
        main_sig = metadata['main_signature']
        output.append(f"\n🔧 Main Function:")

        # Format arguments
        args_str = ", ".join([
            f"{arg['name']}: {arg['annotation']}" if arg['annotation'] else arg['name']
            for arg in main_sig.get('args', [])
        ])
        return_type = f" -> {main_sig['returns']}" if main_sig.get('returns') else ""

        output.append(f"   def main({args_str}){return_type}:")

        if main_sig.get('docstring'):
            output.append(f"   \"\"\"")
            for line in main_sig['docstring'].split('\n'):
                output.append(f"   {line}")
            output.append(f"   \"\"\"")

    # Other functions
    other_functions = [
        f for f in metadata.get('functions', [])
        if f['name'] not in ['get_description', 'main']
    ]

    if other_functions:
        output.append(f"\n📦 Additional Functions:")
        for func in other_functions:
            args_str = ", ".join([
                f"{arg['name']}: {arg['annotation']}" if arg['annotation'] else arg['name']
                for arg in func.get('args', [])
            ])
            return_type = f" -> {func['returns']}" if func.get('returns') else ""

            output.append(f"   • {func['name']}({args_str}){return_type}")
            if func.get('docstring'):
                first_line = func['docstring'].split('\n')[0]
                output.append(f"     {first_line}")

    # Classes
    if metadata.get('classes'):
        output.append(f"\n🏗️  Classes:")
        for cls in metadata['classes']:
            output.append(f"   • {cls['name']}")
            if cls.get('docstring'):
                first_line = cls['docstring'].split('\n')[0]
                output.append(f"     {first_line}")

            if cls.get('methods'):
                output.append(f"     Methods: {', '.join([m['name'] for m in cls['methods']])}")

    # Imports
    if metadata.get('imports'):
        output.append(f"\n📦 Imports:")
        for imp in metadata['imports'][:10]:  # Show first 10
            if imp['type'] == 'import':
                display = f"   • import {imp['module']}"
                if imp['alias']:
                    display += f" as {imp['alias']}"
                output.append(display)
            else:
                display = f"   • from {imp['module']} import {imp['name']}"
                if imp['alias']:
                    display += f" as {imp['alias']}"
                output.append(display)

        if len(metadata['imports']) > 10:
            output.append(f"   ... and {len(metadata['imports']) - 10} more")

    # Errors
    if metadata.get('errors'):
        output.append(f"\n⚠️  Errors:")
        for error in metadata['errors']:
            output.append(f"   • {error}")

    return "\n".join(output)


def search_tools(query: str) -> List[Tuple[str, Dict[str, Any]]]:
    """Search tools by name, description, or functions.

    Args:
        query: Search query

    Returns:
        List of (tool_name, metadata) tuples matching the query
    """
    metadata = load_metadata()
    if not metadata:
        return []

    query = query.lower()
    results = []

    for tool_name, tool_metadata in metadata.items():
        if tool_name.startswith("_"):
            continue

        # Search in tool name
        if query in tool_name.lower():
            results.append((tool_name, tool_metadata))
            continue

        # Search in description
        if tool_metadata.get('docstring'):
            if query in tool_metadata['docstring'].lower():
                results.append((tool_name, tool_metadata))
                continue

        # Search in function names
        for func in tool_metadata.get('functions', []):
            if query in func['name'].lower():
                results.append((tool_name, tool_metadata))
                break

        # Search in class names
        for cls in tool_metadata.get('classes', []):
            if query in cls['name'].lower():
                results.append((tool_name, tool_metadata))
                break

    return results


def list_tools_summarized() -> List[Dict[str, Any]]:
    """Get a summarized list of all tools.

    Returns:
        List of tool summary dictionaries
    """
    metadata = load_metadata()
    if not metadata:
        return []

    summaries = []

    for tool_name, tool_metadata in metadata.items():
        if tool_name.startswith("_"):
            continue

        summary = {
            "name": tool_name,
            "path": tool_metadata.get('path', ''),
            "has_contract": tool_metadata.get('has_get_description') and tool_metadata.get('has_main'),
            "function_count": len(tool_metadata.get('functions', [])),
            "class_count": len(tool_metadata.get('classes', [])),
            "description": None,
        }

        # Get description
        if summary['has_contract']:
            tool_path = Path(tool_metadata['path'])
            summary['description'] = get_tool_description_from_file(tool_path)

        summaries.append(summary)

    return sorted(summaries, key=lambda x: x['name'])


def main():
    """Command-line interface for tool metadata."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Axle Tool Metadata System"
    )
    parser.add_argument(
        "action",
        choices=["scan", "show", "search", "list"],
        help="Action to perform"
    )
    parser.add_argument(
        "tool",
        nargs="?",
        help="Tool name (for 'show' action)"
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Search query (for 'search' action)"
    )

    args = parser.parse_args()

    if args.action == "scan":
        success, message = update_metadata()
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

    elif args.action == "show":
        if not args.tool:
            print("❌ Please provide a tool name")
            return 1

        metadata = load_metadata()
        if not metadata or args.tool not in metadata:
            print(f"❌ Tool '{args.tool}' not found in metadata")
            print("   Run 'axle metadata scan' to update metadata")
            return 1

        formatted = format_tool_metadata(args.tool, metadata[args.tool])
        print(formatted)

    elif args.action == "search":
        if not args.query:
            print("❌ Please provide a search query")
            return 1

        results = search_tools(args.query)
        if not results:
            print(f"❌ No results found for '{args.query}'")
            return 0

        print(f"\n🔍 Search Results for '{args.query}':")
        print("=" * 60)

        for tool_name, tool_metadata in results:
            print(f"\n📋 {tool_name}")

            # Get description
            if tool_metadata.get('has_get_description'):
                tool_path = Path(tool_metadata['path'])
                description = get_tool_description_from_file(tool_path)
                if description:
                    print(f"   {description}")

    elif args.action == "list":
        summaries = list_tools_summarized()

        if not summaries:
            print("❌ No tools found")
            print("   Run 'axle metadata scan' to scan tools")
            return 0

        print(f"\n📋 Available Tools ({len(summaries)}):")
        print("=" * 60)

        for summary in summaries:
            status = "✅" if summary['has_contract'] else "⚠️ "
            print(f"\n{status} {summary['name']}")
            if summary['description']:
                print(f"   {summary['description']}")
            print(f"   Functions: {summary['function_count']}, Classes: {summary['class_count']}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
