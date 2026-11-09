import React, { useState, useEffect } from 'react';
import { useFestival } from '../context/FestivalContext';
import { api, ApiError } from '../api/client';
import {
  X,
  PlusCircle,
  AlertTriangle,
  CheckCircle2,
  Calendar,
  Sparkles,
  Flame,
} from 'lucide-react';
import {
  checkEquipmentMatch,
  formatEquipment,
  toLocalDatetimeInput,
} from '../utils/formatters';

interface CreateConcertModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CreateConcertModal: React.FC<CreateConcertModalProps> = ({ isOpen, onClose }) => {
  const { currentFestival, artists, stages, refreshData, addToast } = useFestival();

  const [artistId, setArtistId] = useState<number | ''>('');
  const [stageId, setStageId] = useState<number | ''>('');
  const [startTime, setStartTime] = useState<string>('');
  const [endTime, setEndTime] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Initialize defaults when opening
  useEffect(() => {
    if (isOpen) {
      setErrorMessage(null);
      if (artists.length > 0) setArtistId(artists[0].id);
      if (stages.length > 0) setStageId(stages[0].id);

      // Default to festival start date
      if (currentFestival) {
        const start = new Date(currentFestival.start_date);
        start.setHours(18, 0, 0, 0);
        const end = new Date(start);
        end.setHours(19, 0, 0, 0);

        setStartTime(toLocalDatetimeInput(start.toISOString()));
        setEndTime(toLocalDatetimeInput(end.toISOString()));
      }
    }
  }, [isOpen, artists, stages, currentFestival]);

  if (!isOpen || !currentFestival) return null;

  const selectedArtist = artists.find((a) => a.id === Number(artistId));
  const selectedStage = stages.find((s) => s.id === Number(stageId));

  // Live equipment check
  const equipmentCheck = checkEquipmentMatch(
    selectedArtist?.required_equipment || [],
    selectedStage?.available_equipment || []
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!artistId || !stageId || !startTime || !endTime) {
      setErrorMessage('Veuillez remplir tous les champs obligatoires.');
      return;
    }

    const start = new Date(startTime);
    const end = new Date(endTime);

    if (end <= start) {
      setErrorMessage('La date et heure de fin doivent être supérieures à la date de début.');
      return;
    }

    setIsSubmitting(true);
    try {
      await api.createConcert({
        festival_id: currentFestival.id,
        artist_id: Number(artistId),
        stage_id: Number(stageId),
        start_time: start.toISOString(),
        end_time: end.toISOString(),
      });

      addToast(
        `Concert programmé : ${selectedArtist?.name || 'Artiste'} sur ${selectedStage?.name || 'Scène'} !`,
        'success'
      );
      await refreshData();
      onClose();
    } catch (err: any) {
      const msg = err instanceof ApiError ? err.message : 'Erreur lors de la programmation du concert.';
      setErrorMessage(msg);
      addToast('Échec de la programmation', 'error', msg);
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
            <div className="p-1.5 rounded-lg bg-hell-red/20 text-hell-red border border-hell-red/40">
              <PlusCircle className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-gothic font-bold text-lg text-white">Programmer un Concert</h3>
              <p className="text-xs text-hell-steel">Ajout d'un set musical au running order</p>
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
          {errorMessage && (
            <div className="p-3 rounded-lg bg-red-950/80 border border-red-800 text-xs text-red-200 flex items-start gap-2 animate-in fade-in">
              <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-red-300">Règle de programmation non respectée :</p>
                <p className="mt-0.5">{errorMessage}</p>
              </div>
            </div>
          )}

          {/* Artist select */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5">
              Groupe / Artiste *
            </label>
            <select
              value={artistId}
              onChange={(e) => setArtistId(Number(e.target.value))}
              required
              className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-hell-red"
            >
              {artists.map((artist) => (
                <option key={artist.id} value={artist.id} className="bg-hell-card text-white">
                  {artist.name} ({artist.genre})
                </option>
              ))}
            </select>
            {selectedArtist && selectedArtist.required_equipment.length > 0 && (
              <p className="text-[11px] text-hell-steel mt-1">
                Matériel requis : {selectedArtist.required_equipment.map(formatEquipment).join(', ')}
              </p>
            )}
          </div>

          {/* Stage select */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5">
              Scène *
            </label>
            <select
              value={stageId}
              onChange={(e) => setStageId(Number(e.target.value))}
              required
              className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-hell-red"
            >
              {stages.map((stage) => (
                <option key={stage.id} value={stage.id} className="bg-hell-card text-white">
                  {stage.name} (Capacité : {stage.capacity.toLocaleString('fr-FR')}p)
                </option>
              ))}
            </select>
          </div>

          {/* Live Equipment Preflight Verification Box */}
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
                  <p className="font-bold text-emerald-400">Compatibilité Matériel Validée</p>
                  <p className="text-[11px] text-emerald-200/80 mt-0.5">
                    La scène "{selectedStage?.name}" dispose de tous les équipements requis par {selectedArtist?.name}.
                  </p>
                </div>
              </>
            ) : (
              <>
                <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold text-amber-400">Attention : Équipements Manquants (Invariable DDD)</p>
                  <p className="text-[11px] text-amber-200/80 mt-0.5">
                    Cette scène ne possède pas : {equipmentCheck.missing.map(formatEquipment).join(', ')}.
                  </p>
                </div>
              </>
            )}
          </div>

          {/* Time range */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5 flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" /> Début du Set *
              </label>
              <input
                type="datetime-local"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                required
                className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-hell-red"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5 flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" /> Fin du Set *
              </label>
              <input
                type="datetime-local"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                required
                className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-hell-red"
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
              Annuler
            </button>

            <button
              type="submit"
              disabled={isSubmitting}
              className="flex items-center gap-2 px-5 py-2 rounded-lg bg-gradient-to-r from-hell-red to-orange-600 text-white text-xs font-bold uppercase tracking-wider shadow-flame hover:brightness-110 disabled:opacity-50 transition-all cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Sparkles className="w-4 h-4 animate-spin" /> Enregistrement...
                </>
              ) : (
                <>
                  <Flame className="w-4 h-4" /> Programmer le Concert
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

