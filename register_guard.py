from database import register_guard

# Replace with desired guard credentials
username = "guard1"
password = "1234"

register_guard(username, password)
print(f"✅ Guard '{username}' registered successfully!")
