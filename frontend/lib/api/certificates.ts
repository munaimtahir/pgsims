/**
 * Certificates API client
 */
import apiClient from './client';
import { downloadFile } from '@/lib/utils';

export interface CertificateSummary {
  id: number;
  title: string;
  certificate_type_name: string;
  issue_date: string;
  status: string;
  has_file: boolean;
  file_name: string;
}

export const certificatesApi = {
  /**
   * Get certificates for the authenticated PG
   */
  getMyCertificates: async () => {
    const response = await apiClient.get<{ count: number; results: CertificateSummary[] }>('/api/certificates/my/');
    return response.data.results;
  },

  /**
   * Get a direct download URL for a certificate.
   * This simply constructs the URL, as the download is handled by a separate endpoint.
   */
  getCertificateDownloadUrl: (id: number) => {
    // We get the base URL from the apiClient's defaults
    const baseUrl = apiClient.defaults.baseURL || window.location.origin;
    return `${baseUrl}/api/certificates/my/${id}/download/`;
  },
  
  /**
   * Triggers a download for a certificate file.
   * @param id The ID of the certificate to download.
   * @param filename The name to use for the downloaded file.
   */
  downloadCertificate: async (id: number, filename: string) => {
    const url = certificatesApi.getCertificateDownloadUrl(id);
    // Use a helper to fetch the blob and trigger download
    try {
        const response = await apiClient.get(url, {
            responseType: 'blob', // Important for file downloads
        });
        downloadFile(response.data, filename);
        return true;
    } catch (error) {
        console.error('Download failed:', error);
        return false;
    }
  },
};

export default certificatesApi;
