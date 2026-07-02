import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Header from '../../components/Header';

describe('Header', () => {
  it('renders the app title', () => {
    render(<Header onToggleSidebar={() => {}} />);
    expect(screen.getByText('LangChain Document QA')).toBeInTheDocument();
  });

  it('calls onToggleSidebar when menu button is clicked', () => {
    const toggleMock = jest.fn();
    render(<Header onToggleSidebar={toggleMock} />);
    const menuButton = screen.getByRole('button');
    fireEvent.click(menuButton);
    expect(toggleMock).toHaveBeenCalledTimes(1);
  });
});
