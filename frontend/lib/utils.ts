/**
 * A utility function to trigger a file download in the browser.
 * @param blob The file content as a Blob.
 * @param filename The desired name for the downloaded file.
 */
export function downloadFile(blob: Blob, filename: string) {
  // Create a URL for the blob
  const url = window.URL.createObjectURL(blob);

  // Create a temporary anchor element
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  
  // Append to the DOM, click, and then remove
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  
  // Revoke the object URL to free up memory
  window.URL.revokeObjectURL(url);
}

