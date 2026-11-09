import React, { useState, useEffect } from 'react';
import { useFestival } from '../context/FestivalContext';
import { Concert } from '../api/types';
import { api, ApiError } from '../api/client';
import {
  X,
  Calendar,
  Sparkles,
  AlertTriangle,
  CheckCircle2,
  Lock,
} from 'lucide-react';
import {
  checkEquipmentMatch,
  formatEquipment,
  toLocalDatetimeInput,
} from '../utils/formatters';

interface RescheduleModalProps {
  concert: Concert | null;
  isOpen: boolean;
  onClose: () => void;
}

export const RescheduleModal: React.FC<RescheduleModalProps> = ({
  concert,
  isOpen,
  onClose,
}) => {
  const { currentFestival, artists, stages, refreshData, addToast } = useFestival();

  const [stageId, setStageId] = useState<number>(0);
  const [startTime, setStartTime] = useState<string>('');
  const [endTime, setEndTime] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (concert && isOpen) {
      setErrorMessage(null);
      setStageId(concert.stage_id);
      setStartTime(toLocalDatetimeInput(concert.start_time));
      setEndTime(toLocalDatetimeInput(concert.end_time));
    }
  }, [concert, isOpen]);

  if (!isOpen || !concert || !currentFestival) return null;

  const isPublished = currentFestival.status === 'published';
  const artist = artists.find((a) => a.id === concert.artist_id);
  const targetStage = stages.find((s) => s.id === stageId);

  // Live equipment check
  const equipmentCheck = checkEquipmentMatch(
    artist?.required_equipment || [],
    targetStage?.available_equipment || []
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (isPublished) {
      setErrorMessage('Le festival est déjà publié (Règle R7) : la modification directe est interdite.');
      return;
    }

    const start = new Date(startTime);
    const end = new Date(endTime);

    if (end <= start) {
      setErrorMessage('La date de fin doit être postérieure à la date de début.');
      return;
    }

    setIsSubmitting(true);
    try {
      await api.rescheduleConcert(concert.id, {
        stage_id: stageId !== concert.stage_id ? stageId : null,
        start_time: start.toISOString(),
        end_time: end.toISOString(),
      });

      addToast(
        `Concert de ${artist?.name || 'Artiste'} déplacé avec succès !`,
        'success'
      );
      await refreshData();
      onClose();
    } catch (err: any) {
      const msg = err instanceof ApiError ? err.message : 'Erreur lors du déplacement du concert.';
      setErrorMessage(msg);
      addToast('Déplacement impossible', 'error', msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-hell-card border border-hell-border max-w-lg w-full rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="p-4 bg-hell-surface border-b border-hell-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-amber-500/20 text-amber-500 border border-amber-500/40">
              <Calendar className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-gothic font-bold text-lg text-white">Déplacer le Concert</h3>
              <p className="text-xs text-hell-steel">
                {artist?.name} — Nouveau créneau ou changement de scène
              </p>
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
        <form onSubmit={handleSubmit} className="p-6 space-y-4 overflow-y-auto">
          {/* Publication lock warning */}
          {isPublished && (
            <div className="p-3.5 rounded-lg bg-red-950/90 border border-red-700 text-xs text-red-200 flex items-start gap-2.5">
              <Lock className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-red-300">Action Interdite — Festival Publié (Règle R7)</p>
                <p className="text-[11px] text-red-200/90 mt-0.5">
                  Une fois le festival publié, le planning officiel est verrouillé pour garantir la stabilité envers le public.
                </p>
              </div>
            </div>
          )}

          {errorMessage && (
            <div className="p-3 rounded-lg bg-red-950/80 border border-red-800 text-xs text-red-200 flex items-start gap-2">
              <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-red-300">Erreur :</p>
                <p className="mt-0.5">{errorMessage}</p>
              </div>
            </div>
          )}

          {/* Target Stage */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5">
              Scène de destination
            </label>
            <select
              value={stageId}
              onChange={(e) => setStageId(Number(e.target.value))}
              disabled={isPublished}
              className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-hell-red disabled:opacity-50 cursor-pointer"
            >
              {stages.map((stage) => (
                <option key={stage.id} value={stage.id} className="bg-hell-card text-white">
                  {stage.name} (Capacité : {stage.capacity.toLocaleString('fr-FR')}p)
                </option>
              ))}
            </select>
          </div>

          {/* Live equipment check */}
          <div
            className={`p-3 rounded-lg border text-xs flex items-start gap-2.5 ${
              equipmentCheck.ok
                ? 'bg-emerald-950/40 border-emerald-800/60 text-emerald-300'
                : 'bg-amber-950/40 border-amber-800/60 text-amber-200'
            }`}
          >
            {equipmentCheck.ok ? (
              <>
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold text-emerald-400">Matériel Validé</p>
                  <p className="text-[11px] text-emerald-200/80 mt-0.5">
                    Tous les équipements requis par {artist?.name} sont disponibles sur cette scène.
                  </p>
                </div>
              </>
            ) : (
              <>
                <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold text-amber-400">Attention Incompatibilité</p>
                  <p className="text-[11px] text-amber-200/80 mt-0.5">
                    Équipements manquants : {equipmentCheck.missing.map(formatEquipment).join(', ')}.
                  </p>
                </div>
              </>
            )}
          </div>

          {/* Start and End Times */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5 flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" /> Nouveau Début *
              </label>
              <input
                type="datetime-local"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                disabled={isPublished}
                required
                className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-hell-red disabled:opacity-50"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5 flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" /> Nouvelle Fin *
              </label>
              <input
                type="datetime-local"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                disabled={isPublished}
                required
                className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-hell-red disabled:opacity-50"
              />
            </div>
          </div>

          {/* Footer actions */}
          <div className="pt-4 border-t border-hell-border flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 rounded-lg bg-hell-surface border border-hell-border text-xs font-semibold text-hell-steel hover:text-white transition-all"
            >
              Fermer
            </button>

            <button
              type="submit"
              disabled={isSubmitting || isPublished}
              className="flex items-center gap-2 px-5 py-2 rounded-lg bg-gradient-to-r from-amber-600 to-orange-600 text-white text-xs font-bold uppercase tracking-wider hover:brightness-110 disabled:opacity-50 transition-all cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Sparkles className="w-4 h-4 animate-spin" /> Déplacement...
                </>
              ) : (
                'Valider le Déplacement'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

