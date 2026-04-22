export function uniqueToken(prefix: string): string {
  return `${prefix}-${Date.now()}`;
}
