import { useQuery, useInfiniteQuery, useMutation } from '@tanstack/react-query';
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1',
});

// Add auth interceptor here if using Auth0

export const useTimeline = (era?: string, topic?: string) => {
  return useInfiniteQuery({
    queryKey: ['timeline', era, topic],
    queryFn: async ({ pageParam = null }) => {
      const { data } = await api.get('/timeline', {
        params: { era, topic, cursor_year: pageParam, limit: 10 }
      });
      return data; // { data: Event[], next_cursor: string, total: number }
    },
    getNextPageParam: (lastPage: any) => lastPage.next_cursor || undefined,
    initialPageParam: null,
  });
};

export const useEventDetail = (eventId: string) => {
  return useQuery({
    queryKey: ['event', eventId],
    queryFn: async () => {
      const { data } = await api.get(`/events/${eventId}`);
      return data;
    },
    enabled: !!eventId,
  });
};

export const useEventAudio = (eventId: string) => {
  return useQuery({
    queryKey: ['audio', eventId],
    queryFn: async () => {
      const { data } = await api.get(`/events/${eventId}/audio`);
      return data; // Array of audio objects with presigned_urls
    },
    enabled: !!eventId,
  });
};

export const useEventPerspectives = (eventId: string) => {
  return useQuery({
    queryKey: ['perspectives', eventId],
    queryFn: async () => {
      const { data } = await api.get(`/events/${eventId}/perspectives`);
      return data;
    },
    enabled: !!eventId,
  });
};
