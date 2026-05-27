import React from 'react';
import { useParams } from 'react-router-dom';
import ChatBox from '../components/ChatBox';

export default function ChatPage() {
  const { id } = useParams();

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Chat with Document</h1>
      <ChatBox documentId={id} />
    </div>
  );
}
