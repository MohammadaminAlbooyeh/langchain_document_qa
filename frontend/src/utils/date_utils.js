export const daysAgo = (dateString) => {
  const now = new Date();
  const date = new Date(dateString);
  const diff = now - date;
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  if (days === 0) return 'today';
  if (days === 1) return 'yesterday';
  return `${days} days ago`;
};

export const isExpired = (dateString, days = 30) => {
  const now = new Date();
  const date = new Date(dateString);
  return (now - date) > (days * 24 * 60 * 60 * 1000);
};
