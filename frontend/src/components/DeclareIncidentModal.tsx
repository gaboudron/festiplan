import React, { useState, useEffect } from 'react';
import { useFestival } from '../context/FestivalContext';
import { Concert } from '../api/types';
import { api, ApiError } from '../api/client';
import {
  X,
  AlertTriangle,
  Flame,
  Sparkles,
} from 'lucide-react';
import { formatTimeSlot } from '../utils/formatters';

interface DeclareIncidentModalProps {
  initialConcert?: Concert | null;
  isOpen: boolean;
  onClose: () => void;
}

export const DeclareIncidentModal: React.FC<DeclareIncidentModalProps> = ({
  initialConcert,
  isOpen,
  onClose,
}) => {
  const { concerts, artists, stages, refreshData, addToast } = useFestival();

  const [concertId, setConcertId] = useState<number | ''>('');
  const [description, setDescription] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setErrorMessage(null);
      setDescription('');
      if (initialConcert) {
        setConcertId(initialConcert.id);
      } else if (concerts.length > 0) {
        setConcertId(concerts[0].id);
      }
    }
  }, [isOpen, initialConcert, concerts]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!concertId || !description.trim()) {
      setErrorMessage('Veuillez sélectionner un concert et rédiger une description.');
      return;
    }

    if (description.trim().length < 3) {
      setErrorMessage('La description doit contenir au moins 3 caractères.');
      return;
    }

    setIsSubmitting(true);
    try {
      await api.createIncident({
        concert_id: Number(concertId),
        description: description.trim(),
        occurred_at: new Date().toISOString(),
      });

      addToast('Incident déclaré à la régie', 'warning', 'Les équipes techniques sont notifiées.');
      await refreshData();
      onClose();
    } catch (err: any) {
      const msg = err instanceof ApiError ? err.message : "Erreur lors de l'enregistrement de l'incident.";
      setErrorMessage(msg);
      addToast('Échec déclaration', 'error', msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-hell-card border border-red-900/60 max-w-lg w-full rounded-2xl shadow-flame overflow-hidden flex flex-col">
        {/* Modal Header */}
        <div className="p-4 bg-hell-surface border-b border-hell-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-red-600/20 text-red-500 border border-red-500/40">
              <AlertTriangle className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <h3 className="font-gothic font-bold text-lg text-white">Signaler un Incident</h3>
              <p className="text-xs text-hell-steel">Régie Technique & Sécurité Backstage</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-hell-steel hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {errorMessage && (
            <div className="p-3 rounded-lg bg-red-950/80 border border-red-800 text-xs text-red-200 flex items-start gap-2">
              <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-red-300">Erreur :</p>
                <p className="mt-0.5">{errorMessage}</p>
              </div>
            </div>
          )}

          {/* Concert select */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5">
              Concert concerné *
            </label>
            <select
              value={concertId}
              onChange={(e) => setConcertId(Number(e.target.value))}
              required
              className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-red-600 cursor-pointer"
            >
              {concerts.map((c) => {
                const artist = artists.find((a) => a.id === c.artist_id);
                const stage = stages.find((s) => s.id === c.stage_id);
                return (
                  <option key={c.id} value={c.id} className="bg-hell-card text-white">
                    {artist?.name || `Artiste #${c.artist_id}`} — {stage?.name || `Scène #${c.stage_id}`} (
                    {formatTimeSlot(c.start_time, c.end_time)})
                  </option>
                );
              })}
            </select>
          </div>

          {/* Description */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5">
              Description de l'incident *
            </label>
            <textarea
              rows={4}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Ex: Panne ampli retour guitare scène 2, retard technique de 15 minutes..."
              required
              className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-xs text-white placeholder-hell-steel focus:outline-none focus:border-red-600"
            />
          </div>

          {/* Footer actions */}
          <div className="pt-4 border-t border-hell-border flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 rounded-lg bg-hell-surface border border-hell-border text-xs font-semibold text-hell-steel hover:text-white transition-all"
            >
              Annuler
            </button>

            <button
              type="submit"
              disabled={isSubmitting}
              className="flex items-center gap-2 px-5 py-2 rounded-lg bg-gradient-to-r from-red-700 to-red-500 text-white text-xs font-bold uppercase tracking-wider shadow-flame hover:brightness-110 disabled:opacity-50 transition-all cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Sparkles className="w-4 h-4 animate-spin" /> Transmission...
                </>
              ) : (
                <>
                  <Flame className="w-4 h-4" /> Enregistrer l'Incident
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

