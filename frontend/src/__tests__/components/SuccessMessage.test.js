import React from 'react';
import { render, screen } from '@testing-library/react';
import SuccessMessage from '../../components/SuccessMessage';

describe('SuccessMessage', () => {
  it('renders the success message', () => {
    render(<SuccessMessage message="Operation completed" />);
    expect(screen.getByText('Operation completed')).toBeInTheDocument();
  });
});
