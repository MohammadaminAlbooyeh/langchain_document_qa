import { generateId, debounce, classNames } from '../../utils/helpers';

describe('generateId', () => {
  it('generates a non-empty string', () => {
    const id = generateId();
    expect(id).toBeTruthy();
    expect(typeof id).toBe('string');
  });

  it('generates unique IDs', () => {
    const ids = new Set(Array.from({ length: 100 }, () => generateId()));
    expect(ids.size).toBe(100);
  });
});

describe('debounce', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('debounces function calls', () => {
    const fn = jest.fn();
    const debounced = debounce(fn, 300);

    debounced();
    debounced();
    debounced();

    expect(fn).not.toHaveBeenCalled();
    jest.advanceTimersByTime(300);
    expect(fn).toHaveBeenCalledTimes(1);
  });

  it('uses default delay of 300ms', () => {
    const fn = jest.fn();
    const debounced = debounce(fn);
    debounced();
    jest.advanceTimersByTime(300);
    expect(fn).toHaveBeenCalledTimes(1);
  });

  it('passes arguments to original function', () => {
    const fn = jest.fn();
    const debounced = debounce(fn, 100);
    debounced('arg1', 'arg2');
    jest.advanceTimersByTime(100);
    expect(fn).toHaveBeenCalledWith('arg1', 'arg2');
  });
});

describe('classNames', () => {
  it('joins class names', () => {
    expect(classNames('foo', 'bar')).toBe('foo bar');
  });

  it('filters falsy values', () => {
    expect(classNames('foo', false, null, undefined, 0, 'bar')).toBe('foo bar');
  });

  it('returns empty string for no classes', () => {
    expect(classNames()).toBe('');
  });
});
