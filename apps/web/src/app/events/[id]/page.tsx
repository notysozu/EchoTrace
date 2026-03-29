'use client';

import { useEventDetail, useEventAudio, useEventPerspectives } from '@/hooks/useApi';
import { usePlayerStore } from '@/store/playerStore';
import { Play } from 'lucide-react';
import { useState } from 'react';

export default function EventDetailPage({ params }: { params: { id: string } }) {
  const { data: event, status: eventStatus } = useEventDetail(params.id);
  const { data: audioFiles } = useEventAudio(params.id);
  const { data: perspectives } = useEventPerspectives(params.id);
  
  const [activeTab, setActiveTab] = useState<string>('narrator');
  const play = usePlayerStore((s) => s.play);

  if (eventStatus === 'pending') return <div className="text-center py-20 animate-pulse text-slate-500">Loading event...</div>;
  if (eventStatus === 'error' || !event) return <div className="text-red-500 text-center py-20">Event not found</div>;

  const currentAudio = audioFiles?.find((a: any) => a.perspective_type === activeTab);
  const currentPerspective = perspectives?.find((p: any) => p.perspective_type === activeTab);

  const handlePlay = () => {
    if (currentAudio) {
      play({
        eventId: event.id,
        title: event.title,
        year: event.year,
        perspective: activeTab as any,
        url: currentAudio.presigned_url,
        durationSeconds: currentAudio.duration_seconds
      });
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h3 className="text-amber-500 font-bold tracking-widest uppercase text-sm mb-2">
            {event.year > 0 ? event.year : `${Math.abs(event.year)} BC`} • {event.era?.label.toUpperCase()}
        </h3>
        <h1 className="text-5xl font-bold tracking-tight text-white mb-4">{event.title}</h1>
        <p className="text-xl text-slate-400 leading-relaxed">{event.description}</p>
      </div>

      {/* Hero Audio Player area */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 flex flex-col items-center justify-center min-h-64 relative overflow-hidden group">
        
        {/* Abstract waveform viz placeholder */}
        <div className="absolute inset-0 flex items-center justify-center opacity-20">
            <div className="w-[120%] h-32 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] mix-blend-overlay animate-pulse"></div>
        </div>

        <button 
            onClick={handlePlay}
            disabled={!currentAudio}
            className="w-20 h-20 bg-amber-500 text-slate-900 rounded-full flex items-center justify-center z-10 hover:scale-105 transition-transform disabled:opacity-50 disabled:hover:scale-100 shadow-[0_0_40px_rgba(245,158,11,0.3)]"
        >
            <Play size={36} className="fill-slate-900 ml-2" />
        </button>
        <p className="mt-6 text-slate-400 font-medium z-10 uppercase tracking-widest text-sm">Play {activeTab} capsule</p>
      </div>

      {/* Perspective Tabs */}
      <div className="mt-12">
        <div className="flex space-x-2 border-b border-slate-800 pb-px">
          {['narrator', 'eyewitness', 'historian', 'opposition'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 font-semibold text-sm capitalize transition-colors border-b-2 ${
                activeTab === tab 
                  ? 'border-amber-500 text-amber-500' 
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
        
        <div className="py-8 space-y-6">
           <h2 className="text-2xl font-semibold capitalize text-white">{activeTab} Perspective</h2>
           <p className="text-slate-300 leading-relaxed text-lg">
               {currentPerspective?.summary || "No specific summary available for this perspective yet."}
           </p>

           {currentPerspective?.fact_tags?.length > 0 && (
              <div className="mt-8">
                  <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">Historical Fact Tags</h4>
                  <div className="flex flex-wrap gap-2">
                      {currentPerspective.fact_tags.map((tag: any, i: number) => (
                          <span key={i} className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700">
                              {tag.tag}
                          </span>
                      ))}
                  </div>
              </div>
           )}
        </div>
      </div>
    </div>
  );
}
