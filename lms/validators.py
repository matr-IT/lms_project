from rest_framework.serializers import ValidationError


def validate_url(url):
    if not url.startswith("https://www.youtube.com"):
        raise ValidationError(
            "Запрещены ссылки на сторонние ресурсы, кроме youtube.com."
        )
