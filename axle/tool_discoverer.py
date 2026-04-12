#!/usr/bin/env python3
"""Intelligent tool discovery and execution system.

This module provides automatic discovery of Python scripts,
extracting commands, functions, and usage information without
requiring any specific contract implementation.
"""

import ast
import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ToolFunction:
    """Represents a discovered function from a tool."""

    def __init__(
        self,
        name: str,
        tool_path: Path,
        module,
        func_obj: Any,
        argspec: inspect.FullArgSpec,
    ):
        self.name = name
        self.tool_path = tool_path
        self.module = module
        self.func_obj = func_obj
        self.argspec = argspec

    @property
    def docstring(self) -> Optional[str]:
        """Get function docstring."""
        return inspect.getdoc(self.func_obj)

    @property
    def signature(self) -> str:
        """Get function signature as string."""
        return str(inspect.signature(self.func_obj))

    @property
    def is_main(self) -> bool:
        """Check if this is a main entry point."""
        return self.name in ['main', 'run', 'cli', 'start', 'execute']

    @property
    def arg_count(self) -> int:
        """Get number of required arguments."""
        # argspec.args is a list in Python 3.11+
        required_count = 0
        args_list = self.argspec.args if isinstance(self.argspec.args, list) else list(self.argspec.args.keys())

        # Check if each arg has a default value
        defaults_offset = len(args_list) - len(self.argspec.defaults) if self.argspec.defaults else len(args_list)

        for i, name in enumerate(args_list):
            if name not in ['self', 'cls']:
                # If there are defaults and this arg is before the defaults, it's required
                if i < defaults_offset:
                    required_count += 1
        return required_count

    def get_arg_names(self) -> List[str]:
        """Get argument names excluding self/cls."""
        # argspec.args is a list in Python 3.11+
        if isinstance(self.argspec.args, list):
            return [name for name in self.argspec.args if name not in ['self', 'cls']]
        else:
            return [name for name in self.argspec.args.keys() if name not in ['self', 'cls']]


class DiscoveredTool:
    """Represents a discovered Python tool."""

    def __init__(self, tool_path: Path):
        self.tool_path = tool_path
        self.name = tool_path.stem
        self.module = None
        self.functions = []
        self.classes = []
        self.metadata = {}
        self._load_tool()

    def _load_tool(self):
        """Load the tool module and extract metadata."""
        try:
            spec = importlib.util.spec_from_file_location(self.name, self.tool_path)
            if spec and spec.loader:
                self.module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(self.module)

                # Extract all functions
                for name, obj in inspect.getmembers(self.module, inspect.isfunction):
                    # Only include functions defined in this module (not imported)
                    # Use __module__ attribute instead of inspect.getmodule() which returns None for dynamic modules
                    if hasattr(obj, '__module__') and obj.__module__ == self.name:
                        try:
                            argspec = inspect.getfullargspec(obj)
                            func = ToolFunction(name, self.tool_path, self.module, obj, argspec)
                            self.functions.append(func)
                        except Exception:
                            pass

                # Extract all classes
                for name, obj in inspect.getmembers(self.module, inspect.isclass):
                    # Only include classes defined in this module
                    # Use __module__ attribute instead of inspect.getmodule() which returns None for dynamic modules
                    if hasattr(obj, '__module__') and obj.__module__ == self.name:
                        self.classes.append((name, obj))

                # Store metadata
                self.metadata = {
                    'docstring': inspect.getdoc(self.module),
                    'has_main': any(f.is_main for f in self.functions),
                    'main_functions': [f.name for f in self.functions if f.is_main],
                    'all_functions': [f.name for f in self.functions],
                    'has_contract': hasattr(self.module, 'get_description') and hasattr(self.module, 'main'),
                }

        except Exception as e:
            self.metadata = {'error': str(e)}

    @property
    def description(self) -> str:
        """Get tool description."""
        # Try contract method first
        if self.module and hasattr(self.module, 'get_description'):
            try:
                return self.module.get_description()()
            except Exception:
                pass

        # Fall back to module docstring
        if self.metadata.get('docstring'):
            lines = self.metadata['docstring'].strip().split('\n')
            return lines[0] if lines else f"{self.name} - Python tool"

        return f"{self.name} - Python tool"

    def get_main_function(self) -> Optional[ToolFunction]:
        """Get the main entry point function."""
        # Look for main functions in order of preference
        main_candidates = ['main', 'run', 'cli', 'start', 'execute']
        for candidate in main_candidates:
            for func in self.functions:
                if func.name == candidate:
                    return func
        return None

    def get_function_by_name(self, name: str) -> Optional[ToolFunction]:
        """Get a function by name."""
        for func in self.functions:
            if func.name == name:
                return func
        return None

    def get_help_text(self) -> str:
        """Generate help text for this tool."""
        output = []
        output.append(f"\n{'=' * 60}")
        output.append(f"Tool: {self.name}")
        output.append(f"File: {self.tool_path.name}")
        output.append(f"{'=' * 60}")

        # Description
        output.append(f"\n{self.description}")

        # Module docstring
        if self.metadata.get('docstring'):
            output.append(f"\n{self.metadata['docstring']}")

        # Available functions/commands
        if self.functions:
            output.append(f"\n📋 Available Functions:")
            for func in self.functions:
                args = func.get_arg_names()
                args_display = " ".join([f"<{arg}>" for arg in args])
                signature = f"{func.name}({args_display})" if args else func.name + "()"

                is_main = " 🔴 MAIN" if func.is_main else ""
                output.append(f"  • {signature}{is_main}")

                if func.docstring:
                    first_line = func.docstring.split('\n')[0] if func.docstring else ""
                    output.append(f"    {first_line}")

        # Classes
        if self.classes:
            output.append(f"\n🏗️  Available Classes:")
            for name, cls in self.classes:
                output.append(f"  • {name}")

        # Usage examples
        main_func = self.get_main_function()
        if main_func:
            args = main_func.get_arg_names()
            if args:
                args_display = " ".join([f"<{arg}>" for arg in args])
                output.append(f"\n💡 Usage (main): axle run {self.name}")
            else:
                output.append(f"\n💡 Usage (main): axle run {self.name}")

        # Show examples for other functions
        if len(self.functions) > 1:
            output.append(f"\n💡 Other functions:")
            for func in self.functions[:5]:  # Show up to 5 functions
                if func.name != main_func.name if main_func else True:
                    args = func.get_arg_names()
                    if args:
                        args_display = " ".join([f"<{arg}>" for arg in args])
                        output.append(f"   • axle run {self.name} {func.name} {args_display}")
                    else:
                        output.append(f"   • axle run {self.name} {func.name}")

        return "\n".join(output)

    def run_function(self, func: ToolFunction, args: List[str]) -> Any:
        """Run a function with arguments."""
        try:
            # Get function signature to convert argument types
            sig = inspect.signature(func.func_obj)
            params = list(sig.parameters.values())

            # Convert string arguments to appropriate types
            converted_args = []
            for i, arg_str in enumerate(args):
                if i < len(params):
                    param = params[i]
                    annotation = param.annotation

                    # Try to use type annotation for conversion
                    if annotation != inspect.Parameter.empty:
                        try:
                            if annotation == bool:
                                # Handle boolean conversion
                                converted_args.append(arg_str.lower() in ('true', '1', 'yes', 'on'))
                            elif annotation == int:
                                converted_args.append(int(arg_str))
                            elif annotation == float:
                                converted_args.append(float(arg_str))
                            else:
                                # Try to call the annotation as a converter
                                converted_args.append(annotation(arg_str))
                        except (ValueError, TypeError):
                            # If conversion fails, use string
                            converted_args.append(arg_str)
                    else:
                        # No annotation, try intelligent conversion
                        # Try int, then float, then string
                        try:
                            converted_args.append(int(arg_str))
                        except ValueError:
                            try:
                                converted_args.append(float(arg_str))
                            except ValueError:
                                converted_args.append(arg_str)
                else:
                    # More args than parameters, pass as string
                    converted_args.append(arg_str)

            # Call the function with converted arguments
            result = func.func_obj(*converted_args)

            # Always show the result if there is one
            if result is not None:
                sys.stdout.write(f"\n✅ Result: {result}\n")
                sys.stdout.flush()
            return result
        except Exception as e:
            sys.stderr.write(f"❌ Error running {func.name}: {e}\n")
            sys.stderr.flush()
            import traceback
            traceback.print_exc()
            return None


class ToolDiscoverer:
    """Discovers and manages Python tools in the tools directory."""

    def __init__(self, tools_dir: Path):
        self.tools_dir = tools_dir
        self.tools: Dict[str, DiscoveredTool] = {}
        self._scan_tools()

    def _scan_tools(self):
        """Scan tools directory for Python files."""
        if not self.tools_dir.exists():
            return

        for py_file in self.tools_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            tool = DiscoveredTool(py_file)
            self.tools[tool.name] = tool

    def get_tool(self, identifier: str) -> Optional[DiscoveredTool]:
        """Get a tool by name or number."""
        # Try by name first
        if identifier in self.tools:
            return self.tools[identifier]

        # Try to match by name part
        for name, tool in self.tools.items():
            if identifier in name or name.replace('_', '') == identifier.replace('_', ''):
                return tool

        # Try as number
        try:
            num = int(identifier)
            tools_list = sorted(self.tools.keys())
            if 1 <= num <= len(tools_list):
                return self.tools[tools_list[num - 1]]
        except ValueError:
            pass

        return None

    def list_tools(self) -> List[DiscoveredTool]:
        """List all tools sorted by name."""
        return [self.tools[name] for name in sorted(self.tools.keys())]

    def run_tool(
        self,
        identifier: str,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
    ) -> int:
        """
        Run a tool or specific command.

        Args:
            identifier: Tool name or number
            command: Optional specific function/command to run
            args: Arguments to pass to the function

        Returns:
            Exit code (0 for success, 1 for error)
        """
        tool = self.get_tool(identifier)
        if not tool:
            print(f"❌ Tool '{identifier}' not found")
            return 1

        # If no command specified, try to find and run main function
        if not command:
            # Check for contract-based main first
            if tool.metadata.get('has_contract'):
                try:
                    prompt = " ".join(args) if args else ""
                    tool.module.main(prompt)
                    return 0
                except Exception as e:
                    print(f"❌ Error running tool: {e}")
                    return 1

            # Try to find main function
            main_func = tool.get_main_function()
            if main_func:
                func_args = args if args else []
                result = tool.run_function(main_func, func_args)
                return 0 if result is not None else 1

            # No main function found, show help
            print(tool.get_help_text())
            print(f"\n💡 This tool doesn't have a clear main function.")
            print(f"   Available functions: {', '.join(tool.metadata['all_functions'])}")
            return 0

        # Check if command is a valid function name
        func = tool.get_function_by_name(command)
        if func:
            func_args = args if args else []
            result = tool.run_function(func, func_args)
            return 0 if result is not None else 1

        # If command is not a valid function, check if this is a contract-based tool
        # If so, treat the command as a prompt
        if tool.metadata.get('has_contract'):
            try:
                # Combine command and args into the prompt
                prompt_parts = [command] + args if args else [command]
                prompt = " ".join(prompt_parts)
                tool.module.main(prompt)
                return 0
            except Exception as e:
                print(f"❌ Error running tool: {e}")
                return 1

        # Not a contract tool and function not found
        print(f"❌ Function '{command}' not found in tool")
        print(f"   Available functions: {', '.join(tool.metadata['all_functions'])}")
        return 1

    def show_tool_help(self, identifier: str) -> int:
        """Show help for a specific tool."""
        tool = self.get_tool(identifier)
        if not tool:
            print(f"❌ Tool '{identifier}' not found")
            return 1

        print(tool.get_help_text())
        return 0
