from django.contrib import admin
from .models import *


class RaceYearListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "Race Year"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "year"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("before_2000", "Before 2000"),
            ("after_2000", "After 2000"),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == "before_2000":
            return queryset.filter(
                year__lte = 2000,
            )
        if self.value() == "after_2000":
            return queryset.filter(
                year__gte=2000,
            )


class RaceResultAdmin(admin.ModelAdmin):
    list_filter = [RaceYearListFilter]


admin.site.register(RaceResult, RaceResultAdmin)
