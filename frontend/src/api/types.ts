export type FestivalStatus = 'preparation' | 'published' | 'cancelled';
export type ConcertStatus = 'scheduled' | 'cancelled';

export interface Festival {
  id: number;
  name: string;
  location: string;
  start_date: string;
  end_date: string;
  status: FestivalStatus;
}

export interface FestivalCreatePayload {
  name: string;
  location: string;
  start_date: string;
  end_date: string;
}

export interface Artist {
  id: number;
  name: string;
  genre: string;
  required_equipment: string[];
}

export interface ArtistCreatePayload {
  name: string;
  genre: string;
  required_equipment: string[];
}

export interface Stage {
  id: number;
  festival_id: number;
  name: string;
  capacity: number;
  available_equipment: string[];
}

export interface StageCreatePayload {
  festival_id: number;
  name: string;
  capacity: number;
  available_equipment: string[];
}

export interface Concert {
  id: number;
  festival_id: number;
  artist_id: number;
  stage_id: number;
  start_time: string;
  end_time: string;
  status: ConcertStatus;
}

export interface ConcertCreatePayload {
  festival_id: number;
  artist_id: number;
  stage_id: number;
  start_time: string;
  end_time: string;
}

export interface ConcertReschedulePayload {
  stage_id?: number | null;
  start_time: string;
  end_time: string;
}

export interface Incident {
  id: number;
  concert_id: number;
  description: string;
  occurred_at: string;
  resolved: boolean;
}

export interface IncidentCreatePayload {
  concert_id: number;
  description: string;
  occurred_at?: string | null;
}

export interface ApiErrorResponse {
  type: string;
  detail: string;
  errors?: Array<{
    loc: (string | number)[];
    msg: string;
    type: string;
  }>;
}

