from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Sequence

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db import connection
from django.db.models import Q
from django.urls import reverse

from sims.cases.models import ClinicalCase
from sims.certificates.models import Certificate
from sims.logbook.models import LogbookEntry
from sims.rotations.models import Rotation

from .models import SavedSearchSuggestion, SearchQueryLog

User = get_user_model()


@dataclass
class SearchResult:
    module: str
    object_id: int
    title: str
    summary: str
    url: str
    score: float


class SearchService:
    def __init__(self, user: User):
        self.user = user
        self.use_full_text = connection.vendor == "postgresql"
        self.limit = settings.GLOBAL_SEARCH_CONFIG["MAX_RESULTS"]

    def search(self, query: str, filters: Dict[str, str] | None = None) -> List[SearchResult]:
        filters = filters or {}
        query = query.strip()
        if not query:
            return []

        results: List[SearchResult] = []
        results.extend(self._search_users(query, filters))
        results.extend(self._search_rotations(query, filters))
        results.extend(self._search_logbook(query, filters))
        results.extend(self._search_certificates(query, filters))
        results.extend(self._search_cases(query, filters))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[: self.limit]

    # region Individual searchers
    def _search_users(self, query: str, filters: Dict[str, str]) -> Sequence[SearchResult]:
        qs = User.objects.filter(is_active=True)
        if not self.user.is_superuser and getattr(self.user, "role", "") != "admin":
            if hasattr(self.user, "is_supervisor") and self.user.is_supervisor():
                qs = qs.filter(Q(supervisor=self.user) | Q(pk=self.user.pk))
            else:
                qs = qs.filter(pk=self.user.pk)

        if role := filters.get("role"):
            qs = qs.filter(role=role)

        if self.use_full_text:
            vector = (
                SearchVector("first_name", weight="A")
                + SearchVector("last_name", weight="A")
                + SearchVector("username", weight="B")
                + SearchVector("email", weight="B")
                + SearchVector("specialty", weight="C")
            )
            search_query = SearchQuery(query)
            qs = (
                qs.annotate(rank=SearchRank(vector, search_query))
                .filter(rank__gte=0.1)
                .order_by("-rank")
            )
            scored = [(obj, obj.rank) for obj in qs[: self.limit]]
        else:
            condition = (
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(username__icontains=query)
                | Q(email__icontains=query)
                | Q(specialty__icontains=query)
            )
            qs = qs.filter(condition)
            scored = [(obj, 0.5) for obj in qs[: self.limit]]

        return [
            SearchResult(
                module="users",
                object_id=obj.pk,
                title=obj.get_full_name() or obj.username,
                summary=f"Role: {obj.get_role_display()} | Email: {obj.email}",
                url=(
                    reverse("users:profile_detail", args=[obj.pk])
                    if self._has_url("users:profile_detail")
                    else ""
                ),
                score=float(score or 0.1),
            )
            for obj, score in scored
        ]

    def _search_rotations(self, query: str, filters: Dict[str, str]) -> Sequence[SearchResult]:
        qs = Rotation.objects.select_related("pg", "department", "hospital")
        if not self.user.is_superuser and getattr(self.user, "role", "") != "admin":
            if hasattr(self.user, "is_supervisor") and self.user.is_supervisor():
                qs = qs.filter(Q(supervisor=self.user) | Q(pg__supervisor=self.user))
            else:
                qs = qs.filter(pg=self.user)

        if status := filters.get("status"):
            qs = qs.filter(status=status)

        return self._apply_generic_search(
            qs,
            query,
            module="rotations",
            title=lambda obj: f"{obj.pg.get_full_name()} - {obj.department.name}",
            summary=lambda obj: f"{obj.hospital.name} ({obj.start_date} - {obj.end_date})",
            url_name="rotations:detail",
            fields=[
                "department__name",
                "hospital__name",
                "pg__first_name",
                "pg__last_name",
                "notes",
            ],
        )

    def _search_logbook(self, query: str, filters: Dict[str, str]) -> Sequence[SearchResult]:
        qs = LogbookEntry.objects.select_related("pg", "rotation").prefetch_related("procedures")
        if not self.user.is_superuser and getattr(self.user, "role", "") != "admin":
            if hasattr(self.user, "is_supervisor") and self.user.is_supervisor():
                qs = qs.filter(Q(supervisor=self.user) | Q(rotation__supervisor=self.user))
            else:
                qs = qs.filter(pg=self.user)

        if status := filters.get("status"):
            qs = qs.filter(status=status)

        return self._apply_generic_search(
            qs,
            query,
            module="logbook",
            title=lambda obj: obj.case_title,
            summary=lambda obj: obj.patient_history_summary[:160],
            url_name="logbook:detail",
            fields=[
                "case_title",
                "patient_history_summary",
                "management_action",
                "learning_points",
            ],
        )

    def _search_certificates(self, query: str, filters: Dict[str, str]) -> Sequence[SearchResult]:
        qs = Certificate.objects.select_related("pg", "certificate_type")
        if not self.user.is_superuser and getattr(self.user, "role", "") != "admin":
            if hasattr(self.user, "is_supervisor") and self.user.is_supervisor():
                qs = qs.filter(pg__supervisor=self.user)
            else:
                qs = qs.filter(pg=self.user)

        if status := filters.get("status"):
            qs = qs.filter(status=status)

        return self._apply_generic_search(
            qs,
            query,
            module="certificates",
            title=lambda obj: obj.title,
            summary=lambda obj: f"{obj.certificate_type.name} - {obj.pg.get_full_name()}",
            url_name="certificates:detail",
            fields=[
                "title",
                "issuing_organization",
                "certificate_number",
                "description",
            ],
        )

    def _search_cases(self, query: str, filters: Dict[str, str]) -> Sequence[SearchResult]:
        qs = ClinicalCase.objects.select_related("pg", "category")
        if not self.user.is_superuser and getattr(self.user, "role", "") != "admin":
            if hasattr(self.user, "is_supervisor") and self.user.is_supervisor():
                qs = qs.filter(pg__supervisor=self.user)
            else:
                qs = qs.filter(pg=self.user)

        if category := filters.get("category"):
            qs = qs.filter(category__id=category)

        return self._apply_generic_search(
            qs,
            query,
            module="cases",
            title=lambda obj: obj.case_title,
            summary=lambda obj: obj.clinical_reasoning[:160],
            url_name="cases:case_detail",
            fields=[
                "case_title",
                "chief_complaint",
                "clinical_reasoning",
                "learning_points",
            ],
        )

    # endregion

    def _apply_generic_search(
        self,
        queryset,
        query: str,
        *,
        module: str,
        title,
        summary,
        url_name: str,
        fields: Sequence[str],
    ) -> List[SearchResult]:
        if self.use_full_text:
            vector = None
            for idx, field in enumerate(fields):
                weight = "A" if idx == 0 else "B"
                component = SearchVector(field, weight=weight)
                vector = component if vector is None else vector + component
            search_query = SearchQuery(query)
            queryset = (
                queryset.annotate(rank=SearchRank(vector, search_query))
                .filter(rank__gte=0.1)
                .order_by("-rank")
            )
            scored = [(obj, obj.rank) for obj in queryset[: self.limit]]
        else:
            condition = Q()
            for field in fields:
                condition |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(condition)
            scored = [(obj, 0.4) for obj in queryset[: self.limit]]

        results = []
        for obj, score in scored:
            results.append(
                SearchResult(
                    module=module,
                    object_id=obj.pk,
                    title=title(obj),
                    summary=_build_snippet(summary(obj), query),
                    url=(reverse(url_name, args=[obj.pk]) if self._has_url(url_name) else ""),
                    score=float(score or 0.1),
                )
            )
        return results

    def log_query(
        self, query: str, filters: Dict[str, str], result_count: int, duration_ms: int
    ) -> None:
        SearchQueryLog.objects.create(
            user=self.user,
            query=query,
            filters=filters,
            result_count=result_count,
            duration_ms=duration_ms,
        )

    def get_recent_history(self) -> List[str]:
        limit = settings.GLOBAL_SEARCH_CONFIG["RECENT_HISTORY_LIMIT"]
        return list(
            SearchQueryLog.objects.filter(user=self.user)
            .order_by("-created_at")
            .values_list("query", flat=True)[:limit]
        )

    def get_suggestions(self, prefix: str) -> List[str]:
        limit = settings.GLOBAL_SEARCH_CONFIG["SUGGESTION_LIMIT"]
        qs = SavedSearchSuggestion.objects.all()
        if prefix:
            qs = qs.filter(label__istartswith=prefix)
        return list(qs.order_by("label").values_list("label", flat=True)[:limit])

    @staticmethod
    def _has_url(name: str) -> bool:
        from django.urls import NoReverseMatch

        try:
            reverse(name, args=[1])
        except NoReverseMatch:
            return False
        return True


def _build_snippet(text: str, query: str, radius: int = 120) -> str:
    if not text:
        return ""
    if not query:
        return text[:radius]

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    match = pattern.search(text)
    if not match:
        return text[:radius]

    index = match.start()
    matched_length = match.end() - match.start()
    start = max(index - radius // 2, 0)
    end = min(index + matched_length + radius // 2, len(text))
    snippet = text[start:end]
    return pattern.sub(lambda m: f"**{m.group(0)}**", snippet)
