import sys
try:
    from auth import get_password_hash
    print(get_password_hash("123"))
except Exception as e:
    import traceback
    traceback.print_exc()
