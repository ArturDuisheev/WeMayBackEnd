# from src.core.settings import

def user_image_path(instance, filename):
    return f"user_images/{instance.username}/{filename}"


def default_user_image_path():
    return 'default/avatar/DefaultUserAvatar.png'
