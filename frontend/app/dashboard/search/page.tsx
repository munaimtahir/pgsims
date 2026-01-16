'use client';

import { useEffect, useState, useCallback } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { searchApi } from '@/lib/api';
import ErrorBanner from '@/components/ui/ErrorBanner';
import LoadingSkeleton from '@/components/ui/LoadingSkeleton';
import SectionCard from '@/components/ui/SectionCard';
import DataTable, { Column } from '@/components/ui/DataTable';
import Link from 'next/link';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    loadHistory();
  }, []);

  const debouncedSearch = useCallback(
    (() => {
      let timeout: NodeJS.Timeout;
      return (searchQuery: string) => {
        clearTimeout(timeout);
        timeout = setTimeout(async () => {
          if (searchQuery.trim().length > 0) {
            try {
              setLoading(true);
              setError(null);
              const [results, suggs] = await Promise.all([
                searchApi.search(searchQuery).catch(() => ({ results: [], count: 0 })),
                searchApi.getSuggestions(searchQuery).catch(() => ({ results: [] })),
              ]);
              setSearchResults(results.results || []);
              setSuggestions((suggs.results || []).map((s: any) => s.text || s));
            } catch (err: any) {
              setError(err?.message || 'Search failed');
            } finally {
              setLoading(false);
            }
          } else {
            setSearchResults([]);
            setSuggestions([]);
          }
        }, 300);
      };
    })(),
    []
  );

  useEffect(() => {
    debouncedSearch(query);
  }, [query, debouncedSearch]);

  async function loadHistory() {
    try {
      const data = await searchApi.getHistory().catch(() => ({ results: [], count: 0 }));
      setHistory(data.results || []);
    } catch {
      // Ignore history errors
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    setShowSuggestions(false);
  };

  const columns: Column<any>[] = [
    {
      key: 'type',
      label: 'Type',
      render: (item) => (
        <span className="px-2 py-1 text-xs rounded-full bg-indigo-100 text-indigo-800 capitalize">
          {item.type || '-'}
        </span>
      ),
    },
    {
      key: 'title',
      label: 'Title',
    },
    {
      key: 'description',
      label: 'Description',
      render: (item) => (
        <div className="max-w-md truncate">{item.description || '-'}</div>
      ),
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (item) => (
        item.url ? (
          <Link
            href={item.url}
            className="text-sm text-indigo-600 hover:text-indigo-900"
          >
            View
          </Link>
        ) : (
          '-'
        )
      ),
    },
  ];

  const groupedResults = searchResults.reduce((acc, result) => {
    const type = result.type || 'other';
    if (!acc[type]) {
      acc[type] = [];
    }
    acc[type].push(result);
    return acc;
  }, {} as Record<string, any[]>);

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Search</h1>
            <p className="mt-2 text-gray-600">Search across the system</p>
          </div>

          {error && <ErrorBanner message={error} />}

          {/* Search Bar */}
          <SectionCard title="Search">
            <div className="relative">
              <input
                type="text"
                value={query}
                onChange={(e) => {
                  setQuery(e.target.value);
                  setShowSuggestions(true);
                }}
                onFocus={() => setShowSuggestions(true)}
                placeholder="Search for users, exams, logbooks, etc..."
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-4 py-2"
              />
              {showSuggestions && suggestions.length > 0 && (
                <div className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto">
                  {suggestions.map((suggestion, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </SectionCard>

          {/* Search Results */}
          {query && (
            <SectionCard title={`Search Results (${searchResults.length})`}>
              {loading ? (
                <LoadingSkeleton lines={5} />
              ) : searchResults.length > 0 ? (
                <div className="space-y-6">
                  {Object.entries(groupedResults).map(([type, results]) => (
                    <div key={type}>
                      <h3 className="text-lg font-medium text-gray-900 mb-2 capitalize">{type}</h3>
                      <DataTable
                        columns={columns}
                        data={results}
                        emptyMessage="No results"
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  No results found for &quot;{query}&quot;
                </div>
              )}
            </SectionCard>
          )}

          {/* Search History */}
          {history.length > 0 && (
            <SectionCard title="Recent Searches">
              <div className="space-y-2">
                {history.slice(0, 10).map((item, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setQuery(item.query);
                      setShowSuggestions(false);
                    }}
                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded"
                  >
                    <div className="font-medium">{item.query}</div>
                    <div className="text-xs text-gray-500">
                      {item.results_count} results • {new Date(item.searched_at).toLocaleDateString()}
                    </div>
                  </button>
                ))}
              </div>
            </SectionCard>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
