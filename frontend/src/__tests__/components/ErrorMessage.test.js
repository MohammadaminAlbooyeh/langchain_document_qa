import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ErrorMessage from '../../components/ErrorMessage';

describe('ErrorMessage', () => {
  it('renders the error message', () => {
    render(<ErrorMessage message="Something went wrong" />);
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
  });

  it('calls onRetry when retry button is clicked', () => {
    const retryMock = jest.fn();
    render(<ErrorMessage message="Error" onRetry={retryMock} />);
    const retryButton = screen.getByText('Retry');
    fireEvent.click(retryButton);
    expect(retryMock).toHaveBeenCalledTimes(1);
  });

  it('does not show retry button when onRetry is not provided', () => {
    render(<ErrorMessage message="Error" />);
    expect(screen.queryByText('Retry')).not.toBeInTheDocument();
  });
});
