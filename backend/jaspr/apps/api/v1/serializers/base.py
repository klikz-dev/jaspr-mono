from rest_framework import serializers


class JasprBaseModelSerializer(serializers.ModelSerializer):
    """
    All Jaspr related model serializers should inherit from
    this in case we ever want to add shared functionality, etc.
    """

    pass


class JasprBaseSerializer(serializers.Serializer):
    """
    All Jaspr related regular serializers should inherit from
    this in case we ever want to add shared functionality, etc.
    """

    pass