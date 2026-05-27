import React from 'react';
import { NavLink } from 'react-router-dom';

export default function Sidebar({ isOpen }) {
  const links = [
    { to: '/', label: 'Home' },
    { to: '/upload', label: 'Upload' },
    { to: '/history', label: 'History' },
    { to: '/settings', label: 'Settings' },
  ];

  return (
    <aside className={`bg-white border-r w-64 transition-all ${isOpen ? '' : 'w-0 overflow-hidden'}`}>
      <nav className="p-4 space-y-2">
        {links.map(link => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `block px-4 py-2 rounded text-sm ${isActive ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50'}`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
