

obj_ect = "test_repo\\test"


with open(obj_ect, "rb") as f:
    lines = f.read().decode().strip()

print(lines)

new_object = b"123131A421"

with open(obj_ect, "wb") as f:
    f.truncate(0)
    f.write(new_object)
    
with open(obj_ect, "rb") as f:
    lines = f.read().decode().strip()

print(lines)