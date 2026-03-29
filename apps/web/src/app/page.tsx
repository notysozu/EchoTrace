'use client';

import { useTimeline } from '@/hooks/useApi';
import { usePlayerStore } from '@/store/playerStore';
import { Play } from 'lucide-react';
import { useEffect } from 'react';
import { useInView } from 'react-intersection-observer';

export default function Home() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, status } = useTimeline();
  const { ref, inView } = useInView();
  const play = usePlayerStore((s) => s.play);

  useEffect(() => {
    if (inView && hasNextPage) {
      fetchNextPage();
    }
  }, [inView, fetchNextPage, hasNextPage]);

  if (status === 'pending') return <div className="text-center py-20 animate-pulse text-slate-500">Loading timeline...</div>;
  if (status === 'error') return <div className="text-red-500 text-center py-20">Error loading timeline</div>;

  return (
    <div className="space-y-12">
      <header className="mb-16">
        <h1 className="text-4xl font-bold tracking-tight text-white mb-2">EchoTrace</h1>
        <p className="text-slate-400">History you can hear.</p>
      </header>
      
      <div className="relative border-l-2 border-slate-800 ml-4 pl-8 space-y-16">
        {data.pages.map((page, i) => (
          <div key={i} className="space-y-16">
            {page.data.map((event: any) => (
              <div key={event.id} className="relative group">
                {/* Timeline dot */}
                <div className="absolute -left-[41px] top-2 w-5 h-5 rounded-full bg-slate-900 border-2 border-amber-500 group-hover:scale-125 group-hover:bg-amber-500 transition-all cursor-pointer" />
                
                <h3 className="text-sm font-bold text-amber-500 mb-1">{event.year > 0 ? event.year : `${Math.abs(event.year)} BC`}</h3>
                <h2 className="text-2xl font-semibold mb-2">{event.title}</h2>
                {event.era && <span className="text-xs bg-slate-800 px-2 py-1 rounded text-slate-300 mb-4 inline-block">{event.era.label}</span>}
                
                <div className="flex items-center mt-4">
                  <button 
                    onClick={() => play({
                      eventId: event.id,
                      title: event.title,
                      year: event.year,
                      perspective: 'narrator',
                      url: event.audio_preview_url || '',
                      durationSeconds: event.duration_seconds || 0
                    })}
                    className="flex items-center gap-2 bg-white text-slate-900 px-4 py-2 rounded-full text-sm font-semibold hover:bg-amber-500 hover:text-white transition-colors"
                  >
                    <Play size={16} className="fill-current" /> Play Preview
                  </button>
                </div>
              </div>
            ))}
          </div>
        ))}
        
        {/* Infinite scroll trigger */}
        <div ref={ref} className="h-10 text-center text-slate-500">
          {isFetchingNextPage ? 'Loading more...' : hasNextPage ? 'Scroll down for more' : 'End of timeline'}
        </div>
      </div>
    </div>
  );
}
