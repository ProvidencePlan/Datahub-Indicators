from indicators.models import Indicator, IndicatorData
from haystack.indexes import *
from haystack import site


class IndicatorIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    datalevels = MultiValueField()
    datasources = MultiValueField()

    def prepare_datasources(self, obj):
        return [ds.short for ds in obj.sorted_datasources()]

    def prepare_datalevels(self, obj):
        return [dl['key_unit_type'] for dl in IndicatorData.objects.filter(indicator=obj).values('key_unit_type').distinct('key_unit_type')]

    def index_queryset(self, using=None):
        return Indicator.objects.filter(published=True)

site.register(Indicator, IndicatorIndex)
