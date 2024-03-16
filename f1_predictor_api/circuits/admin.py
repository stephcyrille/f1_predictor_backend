from django.contrib import admin
from .models import *


class CircuitIsActiveListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "Active Circuit"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "active"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("Is Active", "Is active"),
            ("Not active", "Not active"),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == "Is Active":
            return queryset.filter(
                circuits_is_active=1,
            )
        if self.value() == "Not active":
            return queryset.filter(
                circuits_is_active=0,
            )


class CircuitAdmin(admin.ModelAdmin):
    list_filter = [CircuitIsActiveListFilter]


admin.site.register(Circuit, CircuitAdmin)