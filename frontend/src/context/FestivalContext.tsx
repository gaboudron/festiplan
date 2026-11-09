import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { Festival, Stage, Artist, Concert, Incident } from '../api/types';
import { api, ApiError } from '../api/client';

export interface ToastItem {
  id: string;
  message: string;
  detail?: string;
  type: 'error' | 'success' | 'warning' | 'info';
}

interface FestivalContextType {
  festivals: Festival[];
  currentFestival: Festival | null;
  stages: Stage[];
  artists: Artist[];
  concerts: Concert[];
  incidents: Incident[];
  isLoading: boolean;
  toasts: ToastItem[];
  addToast: (message: string, type?: ToastItem['type'], detail?: string) => void;
  removeToast: (id: string) => void;
  setCurrentFestivalId: (id: number) => void;
  refreshData: () => Promise<void>;
  publishFestival: () => Promise<boolean>;
  cancelConcert: (concertId: number) => Promise<boolean>;
  resolveIncident: (incidentId: number) => Promise<boolean>;
}

const FestivalContext = createContext<FestivalContextType | undefined>(undefined);

export const FestivalProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [festivals, setFestivals] = useState<Festival[]>([]);
  const [currentFestivalId, setCurrentFestivalId] = useState<number | null>(null);
  const [stages, setStages] = useState<Stage[]>([]);
  const [artists, setArtists] = useState<Artist[]>([]);
  const [concerts, setConcerts] = useState<Concert[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const addToast = useCallback(
    (message: string, type: ToastItem['type'] = 'info', detail?: string) => {
      const id = `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
      setToasts((prev) => [...prev, { id, message, type, detail }]);

      // Auto dismiss after 5 seconds
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, 5000);
    },
    []
  );

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  // Fetch initial festivals list
  const loadFestivals = useCallback(async () => {
    try {
      const data = await api.getFestivals();
      setFestivals(data);
      if (data.length > 0 && currentFestivalId === null) {
        // Select the first festival by default (Hellforge Open Air)
        setCurrentFestivalId(data[0].id);
      }
    } catch (err) {
      const msg = err instanceof ApiError ? err.message : 'Erreur de connexion au serveur API';
      addToast('Erreur chargement festivals', 'error', msg);
    }
  }, [addToast, currentFestivalId]);

  // Fetch all details for current festival
  const refreshData = useCallback(async () => {
    setIsLoading(true);
    try {
      // Always fetch global artists and incidents
      const [artistsData, incidentsData, allFestivals] = await Promise.all([
        api.getArtists(),
        api.getIncidents(),
        api.getFestivals(),
      ]);

      setArtists(artistsData);
      setIncidents(incidentsData);
      setFestivals(allFestivals);

      if (currentFestivalId) {
        const [stagesData, concertsData] = await Promise.all([
          api.getStages(currentFestivalId),
          api.getSchedule(currentFestivalId),
        ]);
        setStages(stagesData);
        setConcerts(concertsData);
      }
    } catch (err) {
      const msg = err instanceof ApiError ? err.message : 'Erreur lors de la synchronisation des données';
      addToast('Erreur de synchronisation', 'error', msg);
    } finally {
      setIsLoading(false);
    }
  }, [currentFestivalId, addToast]);

  useEffect(() => {
    loadFestivals();
  }, [loadFestivals]);

  useEffect(() => {
    if (currentFestivalId !== null) {
      refreshData();
    }
  }, [currentFestivalId, refreshData]);

  const currentFestival = festivals.find((f) => f.id === currentFestivalId) || null;

  const publishFestival = async (): Promise<boolean> => {
    if (!currentFestival) return false;
    try {
      const updated = await api.publishFestival(currentFestival.id);
      addToast(`Le festival "${updated.name}" est maintenant PUBLIÉ !`, 'success', 'Le running order est figé.');
      await refreshData();
      return true;
    } catch (err: any) {
      const msg = err instanceof ApiError ? err.message : 'Échec de publication du festival';
      addToast('Impossible de publier le festival', 'error', msg);
      return false;
    }
  };

  const cancelConcert = async (concertId: number): Promise<boolean> => {
    try {
      await api.cancelConcert(concertId);
      addToast('Concert annulé avec succès', 'warning', 'Les notifications ont été transmises.');
      await refreshData();
      return true;
    } catch (err: any) {
      const msg = err instanceof ApiError ? err.message : "Erreur lors de l'annulation";
      addToast("Erreur d'annulation", 'error', msg);
      return false;
    }
  };

  const resolveIncident = async (incidentId: number): Promise<boolean> => {
    try {
      await api.resolveIncident(incidentId);
      addToast(`Incident #${incidentId} clôturé et résolu !`, 'success', 'Régie technique informée.');
      await refreshData();
      return true;
    } catch (err: any) {
      const msg = err instanceof ApiError ? err.message : "Erreur lors de la résolution de l'incident";
      addToast("Erreur de résolution", 'error', msg);
      return false;
    }
  };

  return (
    <FestivalContext.Provider
      value={{
        festivals,
        currentFestival,
        stages,
        artists,
        concerts,
        incidents,
        isLoading,
        toasts,
        addToast,
        removeToast,
        setCurrentFestivalId,
        refreshData,
        publishFestival,
        cancelConcert,
        resolveIncident,
      }}
    >
      {children}
    </FestivalContext.Provider>
  );
};

export const useFestival = () => {
  const context = useContext(FestivalContext);
  if (!context) {
    throw new Error('useFestival must be used within a FestivalProvider');
  }
  return context;
};

