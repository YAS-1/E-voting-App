from repositories.data_repository import DataRepository
from services.audit_service import AuditService
from services.admin_service import AdminService

repo = DataRepository()
repo.load()

audit_service = AuditService(repo)
admin_service = AdminService(repo, audit_service)

current_user = None
for admin in repo.admins.values():
    if admin["role"] == "super_admin" and admin["is_active"]:
        current_user = admin
        break

print("=== All Admins ===")
print(admin_service.get_all_admins())

if current_user:
    print("\n=== Create Admin ===")
    ok, message, admin = admin_service.create_admin(
        current_user=current_user,
        username="test_admin",
        full_name="Test Admin",
        email="testadmin@example.com",
        password="admin123",
        role_choice="2"
    )
    print(ok, message)
    print(admin)

    print("\n=== Deactivate Admin ===")
    if admin:
        ok, message = admin_service.deactivate_admin(current_user, admin["id"])
        print(ok, message)