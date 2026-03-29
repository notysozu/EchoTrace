import { useEffect, useRef } from 'react';
import { Howl } from 'howler';
import { usePlayerStore } from '@/store/playerStore';

export function useAudioPlayer() {
  const { 
    currentTrack, 
    isPlaying, 
    volume, 
    playbackRate, 
    playNext,
    pause,
    resume 
  } = usePlayerStore();
  
  const soundRef = useRef<Howl | null>(null);

  useEffect(() => {
    // Cleanup previous track
    if (soundRef.current) {
      soundRef.current.unload();
      soundRef.current = null;
    }

    if (currentTrack) {
      soundRef.current = new Howl({
        src: [currentTrack.url],
        html5: true, // Streaming mode
        volume: volume,
        rate: playbackRate,
        onend: () => {
          playNext();
        },
        onloaderror: (id, err) => {
          console.error("Howler Load Error", err);
          pause();
        },
        onplayerror: (id, err) => {
          console.error("Howler Play Error", err);
          pause();
        }
      });

      if (isPlaying) {
        soundRef.current.play();
      }
    }

    return () => {
      if (soundRef.current) {
        soundRef.current.unload();
      }
    };
  }, [currentTrack?.url]); // Only re-init when track URL changes

  // Handle play/pause sync
  useEffect(() => {
    if (!soundRef.current) return;
    
    if (isPlaying && !soundRef.current.playing()) {
      soundRef.current.play();
    } else if (!isPlaying && soundRef.current.playing()) {
      soundRef.current.pause();
    }
  }, [isPlaying]);

  // Handle volume & rate sync
  useEffect(() => {
    if (soundRef.current) {
      soundRef.current.volume(volume);
    }
  }, [volume]);

  useEffect(() => {
    if (soundRef.current) {
      soundRef.current.rate(playbackRate);
    }
  }, [playbackRate]);

  const seek = (seconds: number) => {
    if (soundRef.current) {
      soundRef.current.seek(seconds);
    }
  };

  const getPosition = () => {
    if (soundRef.current && soundRef.current.playing()) {
        return soundRef.current.seek() as number;
    }
    return 0;
  }

  return { seek, getPosition };
}
