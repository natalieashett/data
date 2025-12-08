python
print("World Database Explorer")
print("=" * 30)

# Let's look at the first part of our SQL file
try:
    with open('world db (1).sql', 'r', encoding='utf-8') as file:
        content = file.read()
    
    print(f"File size: {len(content)} characters")
    print(f"Number of lines: {len(content.split(chr(10)))}")
    
    # Show first 500 characters
    print("\nFirst 500 characters:")
    print("-" * 40)
    print(content[:500])
    
    # Look for key patterns
    print("\n\nLooking for database structure...")
    if "CREATE TABLE" in content:
        print("✓ Found CREATE TABLE statements")
    if "INSERT INTO" in content:
        print("✓ Found INSERT INTO statements")
    if "world" in content.lower():
        print("✓ Contains 'world' references")
    
except Exception as e:
    print(f"Error reading file: {e}")
