import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

jest.mock('../components/Header', () => () => <div data-testid="header">Header</div>);
jest.mock('../components/Sidebar', () => () => <div data-testid="sidebar">Sidebar</div>);
jest.mock('../pages/HomePage', () => () => <div data-testid="home-page">Home</div>);
jest.mock('../pages/UploadPage', () => () => <div data-testid="upload-page">Upload</div>);
jest.mock('../pages/NotFoundPage', () => () => <div data-testid="not-found">Not Found</div>);

describe('App', () => {
  it('renders header and sidebar', () => {
    const App = require('../App').default;
    render(
      <MemoryRouter>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('header')).toBeInTheDocument();
    expect(screen.getByTestId('sidebar')).toBeInTheDocument();
  });

  it('renders home page on default route', () => {
    const App = require('../App').default;
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('home-page')).toBeInTheDocument();
  });

  it('renders upload page at /upload', () => {
    const App = require('../App').default;
    render(
      <MemoryRouter initialEntries={['/upload']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('upload-page')).toBeInTheDocument();
  });

  it('renders 404 page for unknown routes', () => {
    const App = require('../App').default;
    render(
      <MemoryRouter initialEntries={['/unknown']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('not-found')).toBeInTheDocument();
  });
});
