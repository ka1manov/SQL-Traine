import { useState, useEffect, useRef } from 'react';
import { Clock } from 'lucide-react';

interface Props {
  seconds: number;
  onExpire?: () => void;
  running?: boolean;
}

export default function Timer({ seconds, onExpire, running = true }: Props) {
  const [remaining, setRemaining] = useState(seconds);
  const onExpireRef = useRef(onExpire);

  useEffect(() => {
    onExpireRef.current = onExpire;
  }, [onExpire]);

  useEffect(() => {
    setRemaining(seconds);
  }, [seconds]);

  useEffect(() => {
    if (!running || remaining <= 0) return;
    const interval = setInterval(() => {
      setRemaining(prev => {
        if (prev <= 1) {
          onExpireRef.current?.();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [running]);

  const mins = Math.floor(remaining / 60);
  const secs = remaining % 60;
  const isLow = remaining < 300;

  return (
    <div className={`flex items-center gap-2 font-mono text-lg ${isLow ? 'text-accent-red' : 'text-gray-300 dark:text-gray-300 text-gray-600'}`}>
      <Clock className="w-5 h-5" />
      {String(mins).padStart(2, '0')}:{String(secs).padStart(2, '0')}
    </div>
  );
}
