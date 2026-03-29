import { create } from 'zustand';
import { persist } from 'zustand/middleware';

type Perspective = 'narrator' | 'eyewitness' | 'historian' | 'opposition' | 'immersive';

interface AudioItem {
  eventId: string;
  title: string;
  year: number;
  url: string; // Presigned S3 URL
  perspective: Perspective;
  durationSeconds: number;
}

interface PlayerState {
  currentTrack: AudioItem | null;
  queue: AudioItem[];
  isPlaying: boolean;
  history: AudioItem[];
  volume: number;
  playbackRate: number;
  
  // Actions
  play: (track: AudioItem) => void;
  pause: () => void;
  resume: () => void;
  addToQueue: (track: AudioItem) => void;
  playNext: () => void;
  setVolume: (val: number) => void;
  setPlaybackRate: (val: number) => void;
}

export const usePlayerStore = create<PlayerState>()(
  persist(
    (set, get) => ({
      currentTrack: null,
      queue: [],
      isPlaying: false,
      history: [],
      volume: 1.0,
      playbackRate: 1.0,

      play: (track) => set((state) => ({ 
        currentTrack: track, 
        isPlaying: true,
        history: [track, ...state.history.slice(0, 19)] 
      })),
      
      pause: () => set({ isPlaying: false }),
      resume: () => set((state) => ({ isPlaying: !!state.currentTrack })),
      
      addToQueue: (track) => set((state) => ({ 
        queue: [...state.queue, track] 
      })),
      
      playNext: () => {
        const { queue } = get();
        if (queue.length > 0) {
          const [nextTrack, ...remaining] = queue;
          set((state) => ({
            currentTrack: nextTrack,
            queue: remaining,
            isPlaying: true,
            history: [nextTrack, ...state.history.slice(0, 19)]
          }));
        } else {
          set({ currentTrack: null, isPlaying: false });
        }
      },

      setVolume: (volume) => set({ volume }),
      setPlaybackRate: (playbackRate) => set({ playbackRate }),
    }),
    {
      name: 'echotrace-player-storage',
      partialize: (state) => ({ 
        history: state.history, 
        volume: state.volume, 
        playbackRate: state.playbackRate 
      }),
    }
  )
);
