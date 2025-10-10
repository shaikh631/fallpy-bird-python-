# Arithmetic Unit Simulator
# Topic: Computer Organization (Unit 1 & 2)
# Operations: Addition, Subtraction, Multiplication (Shift-and-Add, Booth’s Algorithm)

def binary_addition(a, b):
    """Performs binary addition using ripple carry logic"""
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    result = ''
    carry = 0

    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if a[i] == '1' else 0
        r += 1 if b[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1

    if carry != 0:
        result = '1' + result

    return result.zfill(max_len)

def binary_subtraction(a, b):
    """Performs subtraction using 2's complement"""
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)

    # 2's complement of b
    b_invert = ''.join('1' if bit == '0' else '0' for bit in b)
    b_twos_complement = binary_addition(b_invert, '1'.zfill(max_len))
    return binary_addition(a, b_twos_complement)[-max_len:]

def shift_and_add_multiplication(m, q):
    """Performs multiplication using shift-and-add"""
    m = int(m, 2)
    q = int(q, 2)
    product = 0
    step = 0
    print("\nShift-and-Add Multiplication Steps:")
    while q > 0:
        if q & 1:
            product += m
            print(f"Step {step}: Added multiplicand -> Product = {bin(product)[2:]}")
        m <<= 1
        q >>= 1
        step += 1
    print(f"Final Product: {bin(product)[2:]}")
    return bin(product)[2:]

def booths_algorithm(m, q):
    """Booth’s algorithm for signed multiplication"""
    print("\nBooth’s Algorithm Steps:")
    m = int(m, 2)
    q = int(q, 2)
    A = 0
    Q = q
    Q_1 = 0
    count = 4  # assuming 4-bit numbers

    print(f"Initial -> A: {A:04b}, Q: {Q:04b}, Q-1: {Q_1}, M: {m:04b}")

    for i in range(count):
        if (Q & 1) == 1 and Q_1 == 0:
            A = A - m
            print(f"Step {i+1}: 10 -> A = A - M -> {A:04b}")
        elif (Q & 1) == 0 and Q_1 == 1:
            A = A + m
            print(f"Step {i+1}: 01 -> A = A + M -> {A:04b}")

        # Arithmetic right shift
        combined = (A << (count + 1)) | (Q << 1) | Q_1
        combined >>= 1
        A = (combined >> (count + 1)) & ((1 << count) - 1)
        Q = (combined >> 1) & ((1 << count) - 1)
        Q_1 = combined & 1

        print(f"After shift {i+1}: A={A:04b}, Q={Q:04b}, Q-1={Q_1}")

    result = (A << count) | Q
    print(f"Final Result: {result:08b}")
    return f"{result:08b}"

# -------- Main --------
print("=== Arithmetic Unit Simulator ===")
print("1. Addition")
print("2. Subtraction")
print("3. Shift-and-Add Multiplication")
print("4. Booth’s Multiplication")

choice = int(input("Enter your choice (1-4): "))

if choice in [1, 2]:
    a = input("Enter first binary number: ")
    b = input("Enter second binary number: ")
    if choice == 1:
        print("Result:", binary_addition(a, b))
    else:
        print("Result:", binary_subtraction(a, b))
elif choice == 3:
    a = input("Enter multiplicand (binary): ")
    b = input("Enter multiplier (binary): ")
    shift_and_add_multiplication(a, b)
elif choice == 4:
    a = input("Enter multiplicand (4-bit binary): ")
    b = input("Enter multiplier (4-bit binary): ")
    booths_algorithm(a, b)
else:
    print("Invalid choice!")
