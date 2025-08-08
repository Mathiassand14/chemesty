from chemesty.elements import H, O, C, Fe

# Test accessing properties directly
print("=== Testing element properties ===")
print(f"H.name: {H.name}")
print(f"H.symbol: {H.symbol}")
print(f"H.atomic_number: {H.atomic_number}")
print(f"H.atomic_mass: {H.atomic_mass}")
print(f"O.name: {O.name}")
print(f"C.name: {C.name}")
print(f"Fe.name: {Fe.name}")

# Test computed properties
print("\n=== Testing computed properties ===")
print(f"H.volume_value: {H.volume_value}")

# Test methods
print("\n=== Testing methods ===")
print(f"H.is_metal(): {H.is_metal()}")

# Test element operations
print("\n=== Testing element operations ===")
water = H * 2 + O
print(f"H * 2 + O: {water}")