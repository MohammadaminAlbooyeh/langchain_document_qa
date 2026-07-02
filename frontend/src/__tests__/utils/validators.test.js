import { validateFileType, validateFileSize, validateQuestion } from '../../utils/validators';

describe('validateFileType', () => {
  it('accepts pdf files', () => {
    expect(validateFileType('document.pdf')).toBe(true);
  });

  it('accepts docx files', () => {
    expect(validateFileType('document.docx')).toBe(true);
  });

  it('accepts txt files', () => {
    expect(validateFileType('document.txt')).toBe(true);
  });

  it('rejects unsupported file types', () => {
    expect(validateFileType('image.png')).toBe(false);
    expect(validateFileType('script.js')).toBe(false);
  });

  it('is case insensitive', () => {
    expect(validateFileType('document.PDF')).toBe(true);
    expect(validateFileType('document.DOCX')).toBe(true);
  });
});

describe('validateFileSize', () => {
  it('accepts files under the limit', () => {
    const file = { size: 50 * 1024 * 1024 };
    expect(validateFileSize(file, 100)).toBe(true);
  });

  it('rejects files over the limit', () => {
    const file = { size: 200 * 1024 * 1024 };
    expect(validateFileSize(file, 100)).toBe(false);
  });

  it('uses default 100MB limit', () => {
    const small = { size: 50 * 1024 * 1024 };
    const large = { size: 150 * 1024 * 1024 };
    expect(validateFileSize(small)).toBe(true);
    expect(validateFileSize(large)).toBe(false);
  });
});

describe('validateQuestion', () => {
  it('accepts valid questions', () => {
    expect(validateQuestion('What is this document about?')).toBe(true);
  });

  it('rejects empty questions', () => {
    expect(validateQuestion('')).toBe(false);
    expect(validateQuestion('   ')).toBe(false);
  });

  it('rejects overly long questions', () => {
    const long = 'a'.repeat(5000);
    expect(validateQuestion(long)).toBe(false);
  });
});
