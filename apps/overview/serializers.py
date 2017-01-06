from .models import Overview

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer


class OverviewSerializer(DocumentSerializer):

    class Meta:
        model = Overview
        fields = ('__all__')