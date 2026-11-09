import {
  Festival,
  FestivalCreatePayload,
  Artist,
  ArtistCreatePayload,
  Stage,
  StageCreatePayload,
  Concert,
  ConcertCreatePayload,
  ConcertReschedulePayload,
  Incident,
  IncidentCreatePayload,
  ApiErrorResponse,
} from './types';

const API_BASE = import.meta.env.VITE_API_URL || '';

export class ApiError extends Error {
  public type: string;
  public status: number;
  public details?: any;

  constructor(status: number, data: ApiErrorResponse | any) {
    const message = data?.detail || data?.message || 'Une erreur inattendue est survenue';
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.type = data?.type || 'UNKNOWN_ERROR';
    this.details = data?.errors || data;
  }
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    ...options?.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorData: any;
    try {
      errorData = await response.json();
    } catch {
      errorData = { detail: await response.text() };
    }
    throw new ApiError(response.status, errorData);
  }

  // Handle empty 204 or 201 without content
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return (await response.json()) as T;
  }
  return null as unknown as T;
}

export const api = {
  // Festivals
  async getFestivals(): Promise<Festival[]> {
    return request<Festival[]>('/festivals');
  },
  async createFestival(payload: FestivalCreatePayload): Promise<Festival> {
    return request<Festival>('/festivals', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
  async publishFestival(festivalId: number): Promise<Festival> {
    return request<Festival>(`/festivals/${festivalId}/publish`, {
      method: 'POST',
    });
  },

  // Artists
  async getArtists(): Promise<Artist[]> {
    return request<Artist[]>('/artists');
  },
  async createArtist(payload: ArtistCreatePayload): Promise<Artist> {
    return request<Artist>('/artists', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // Stages
  async getStages(festivalId: number): Promise<Stage[]> {
    return request<Stage[]>(`/stages?festival_id=${festivalId}`);
  },
  async createStage(payload: StageCreatePayload): Promise<Stage> {
    return request<Stage>('/stages', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // Concerts
  async getConcerts(festivalId: number): Promise<Concert[]> {
    return request<Concert[]>(`/concerts?festival_id=${festivalId}`);
  },
  async getConcert(concertId: number): Promise<Concert> {
    return request<Concert>(`/concerts/${concertId}`);
  },
  async getSchedule(festivalId: number): Promise<Concert[]> {
    return request<Concert[]>(`/concerts/schedule/${festivalId}`);
  },
  async createConcert(payload: ConcertCreatePayload): Promise<Concert> {
    return request<Concert>('/concerts', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
  async rescheduleConcert(
    concertId: number,
    payload: ConcertReschedulePayload
  ): Promise<Concert> {
    return request<Concert>(`/concerts/${concertId}/reschedule`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    });
  },
  async cancelConcert(concertId: number): Promise<Concert> {
    return request<Concert>(`/concerts/${concertId}/cancel`, {
      method: 'POST',
    });
  },

  // Incidents
  async getIncidents(concertId?: number): Promise<Incident[]> {
    const q = concertId !== undefined ? `?concert_id=${concertId}` : '';
    return request<Incident[]>(`/incidents${q}`);
  },
  async createIncident(payload: IncidentCreatePayload): Promise<Incident> {
    return request<Incident>('/incidents', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
  async resolveIncident(incidentId: number): Promise<Incident> {
    return request<Incident>(`/incidents/${incidentId}/resolve`, {
      method: 'PATCH',
    });
  },
};

