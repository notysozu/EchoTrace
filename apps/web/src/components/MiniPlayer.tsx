import { usePlayerStore } from '@/store/playerStore';
import { useAudioPlayer } from '@/hooks/useAudioPlayer';
import { Play, Pause, SkipForward, Volume2 } from 'lucide-react';

export default function MiniPlayer() {
  const { currentTrack, isPlaying, pause, resume, playNext } = usePlayerStore();
  const { seek, getPosition } = useAudioPlayer(); // Initializes Howler silently

  if (!currentTrack) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 h-20 bg-slate-900 border-t border-slate-800 text-white flex items-center justify-between px-6 z-50 shadow-[0_-10px_40px_rgba(0,0,0,0.3)] backdrop-blur-md bg-opacity-90">
      
      {/* Track Info */}
      <div className="flex items-center gap-4 w-1/3">
        <div className="w-12 h-12 bg-slate-800 rounded flex items-center justify-center text-xs font-bold text-amber-500">
          {currentTrack.year > 0 ? currentTrack.year : `${Math.abs(currentTrack.year)} BC`}
        </div>
        <div>
          <h4 className="font-semibold text-sm truncate">{currentTrack.title}</h4>
          <p className="text-xs text-slate-400 capitalize">{currentTrack.perspective}</p>
        </div>
      </div>

      {/* Controls */}
      <div className="flex flex-col items-center w-1/3">
        <div className="flex items-center gap-6">
          <button 
            onClick={isPlaying ? pause : resume}
            className="w-10 h-10 rounded-full bg-white text-slate-900 flex items-center justify-center hover:scale-105 transition-transform"
          >
            {isPlaying ? <Pause size={20} className="fill-slate-900" /> : <Play size={20} className="fill-slate-900 ml-1" />}
          </button>
          <button onClick={playNext} className="text-slate-400 hover:text-white transition-colors">
            <SkipForward size={20} />
          </button>
        </div>
      </div>

      {/* Extras */}
      <div className="flex items-center justify-end w-1/3 gap-4 text-slate-400">
         <Volume2 size={18} />
      </div>
    </div>
  );
}
