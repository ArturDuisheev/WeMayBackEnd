def category_image_path(instance, filename):
    return f"category_images/{instance.title}/{filename}"


def category_icon_path(instance, filename):
    return f"category_icons/{instance.title}/{filename}"
