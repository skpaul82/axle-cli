#!/usr/bin/env python3
"""A simple calculator tool - demonstrates Axle's intelligent discovery.

This is a simple example script that shows how Axle can automatically
discover and run ANY Python script without requiring specific
contract implementation.
"""

def add(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a.

    Args:
        a: First number
        b: Second number

    Returns:
        Difference of a and b
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b
    """
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b.

    Args:
        a: First number
        b: Second number

    Returns:
        Quotient of a and b

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


def main():
    """Main calculator function - runs an interactive calculator."""
    print("🔢 Simple Calculator")
    print("=" * 40)
    print("Available operations:")
    print("  add - Add two numbers")
    print("  subtract - Subtract two numbers")
    print("  multiply - Multiply two numbers")
    print("  divide - Divide two numbers")
    print("=" * 40)

    while True:
        try:
            print("\nEnter operation (or 'quit'):")
            operation = input("Operation: ").strip().lower()

            if operation in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if operation not in ['add', 'subtract', 'multiply', 'divide']:
                print("❌ Unknown operation. Try: add, subtract, multiply, divide")
                continue

            print(f"\nEnter two numbers for {operation}:")
            a = float(input("First number: "))
            b = float(input("Second number: "))

            # Get the function
            func = globals()[operation]
            result = func(a, b)

            print(f"\n✅ Result: {a} {operation} {b} = {result}")

        except ValueError as e:
            print(f"\n❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
