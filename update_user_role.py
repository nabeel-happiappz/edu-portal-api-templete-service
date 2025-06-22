import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_api.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def update_user_role(email, new_role):
    """
    Update a user's role by email

    Args:
        email (str): User's email address
        new_role (str): New role value (user, admin, or super)
    """
    try:
        user = User.objects.get(email=email)
        user.role = new_role
        user.save()
        print(f"Successfully updated user {email} to role '{new_role}'")

        # Show updated user info
        print(f"User ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Username: {user.username}")
        print(f"Role: {user.role}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Is Staff: {user.is_staff}")
    except User.DoesNotExist:
        print(f"User with email {email} not found")
    except Exception as e:
        print(f"Error updating user: {e}")

if __name__ == "__main__":
    # Example usage - uncomment and modify as needed
    # update_user_role("iamnabeelhashim@gmail.com", "admin")

    email = input("Enter user email: ")
    role = input("Enter new role (user, admin, student): ")

    if role not in ["user", "admin", "student"]:
        print("Invalid role! Choose from 'user', 'admin', or 'super'.")
    else:
        update_user_role(email, role)
