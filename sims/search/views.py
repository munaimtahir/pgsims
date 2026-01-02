from __future__ import annotations

import time

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.audit.utils import log_view

from .serializers import SearchQueryLogSerializer, SearchResultSerializer
from .services import SearchService


class GlobalSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "").strip()
        filters = {
            key.replace("filter_", ""): value
            for key, value in request.query_params.items()
            if key.startswith("filter_") and value
        }
        service = SearchService(request.user)
        start = time.perf_counter()
        results = service.search(query, filters)
        duration_ms = int((time.perf_counter() - start) * 1000)
        if query:
            service.log_query(query, filters, len(results), duration_ms)
        log_view(request, "global-search", metadata={"query": query, "filters": filters})
        serializer = SearchResultSerializer(results, many=True)
        return Response(
            {
                "results": serializer.data,
                "count": len(results),
                "duration_ms": duration_ms,
                "history": service.get_recent_history(),
                "suggestions": service.get_suggestions(query[:32]),
            }
        )


class SearchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        service = SearchService(request.user)
        logs = request.user.search_queries.all()[:50]
        serializer = SearchQueryLogSerializer(logs, many=True)
        return Response(serializer.data)


class SearchSuggestionsView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(30))
    def get(self, request, *args, **kwargs):
        prefix = request.query_params.get("q", "")
        service = SearchService(request.user)
        suggestions = service.get_suggestions(prefix)
        return Response({"suggestions": suggestions})
