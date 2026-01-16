/**
 * Search API client
 * Handles global search functionality
 */

import apiClient from './client';

export interface SearchResult {
  type: string;
  id: number;
  title: string;
  description?: string;
  url: string;
  metadata?: Record<string, any>;
}

export interface SearchHistory {
  id: number;
  query: string;
  results_count: number;
  searched_at: string;
}

export interface SearchSuggestion {
  text: string;
  type?: string;
}

export const searchApi = {
  /**
   * Global search
   */
  search: async (query: string, params?: { types?: string[]; limit?: number }) => {
    const response = await apiClient.get<{ results: SearchResult[]; count: number }>('/api/search/', {
      params: { q: query, ...params },
    });
    return response.data;
  },

  /**
   * Get search history
   */
  getHistory: async () => {
    const response = await apiClient.get<{ results: SearchHistory[]; count: number }>('/api/search/history/');
    return response.data;
  },

  /**
   * Get search suggestions
   */
  getSuggestions: async (query: string) => {
    const response = await apiClient.get<{ results: SearchSuggestion[] }>('/api/search/suggestions/', {
      params: { q: query },
    });
    return response.data;
  },
};

export default searchApi;
