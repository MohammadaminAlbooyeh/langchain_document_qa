import { formatFileSize, formatDate, truncate } from '../../utils/formatters';

describe('formatFileSize', () => {
  it('formats bytes', () => {
    expect(formatFileSize(500)).toBe('500 B');
  });

  it('formats kilobytes', () => {
    expect(formatFileSize(2048)).toBe('2.0 KB');
  });

  it('formats megabytes', () => {
    expect(formatFileSize(5 * 1024 * 1024)).toBe('5.0 MB');
  });
});

describe('formatDate', () => {
  it('formats a date string', () => {
    const result = formatDate('2024-01-15T10:30:00Z');
    expect(result).toContain('2024');
    expect(result).toContain('Jan');
  });

  it('handles different date formats', () => {
    const result = formatDate('2024-06-01');
    expect(result).toContain('Jun');
  });
});

describe('truncate', () => {
  it('returns full string when under limit', () => {
    expect(truncate('Hello', 100)).toBe('Hello');
  });

  it('truncates strings over the limit', () => {
    const long = 'a'.repeat(200);
    const result = truncate(long, 100);
    expect(result).toHaveLength(103);
    expect(result.endsWith('...')).toBe(true);
  });

  it('returns empty string for null/undefined', () => {
    expect(truncate(null)).toBe('');
    expect(truncate(undefined)).toBe('');
  });

  it('uses default length of 100', () => {
    const long = 'a'.repeat(150);
    expect(truncate(long)).toHaveLength(103);
  });
});
