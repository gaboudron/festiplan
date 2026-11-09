import React from 'react';
import { Concert, Artist, Stage } from '../api/types';
import { useFestival } from '../context/FestivalContext';
import {
  Clock,
  Sparkles,
  AlertTriangle,
  CheckCircle2,
  CalendarDays,
  Flame,
  XCircle,
  FileWarning,
} from 'lucide-react';
import { formatTimeSlot, checkEquipmentMatch, formatEquipment } from '../utils/formatters';

interface ConcertCardProps {
  concert: Concert;
  artist?: Artist;
  stage?: Stage;
  onReschedule: (concert: Concert) => void;
  onDeclareIncident: (concert: Concert) => void;
}

export const ConcertCard: React.FC<ConcertCardProps> = ({
  concert,
  artist,
  stage,
  onReschedule,
  onDeclareIncident,
}) => {
  const { currentFestival, cancelConcert, incidents } = useFestival();
  const isPublished = currentFestival?.status === 'published';
  const isCancelled = concert.status === 'cancelled';

  // Find incidents for this concert
  const concertIncidents = incidents.filter((i) => i.concert_id === concert.id);

  // Equipment check
  const equipmentCheck = checkEquipmentMatch(
    artist?.required_equipment || [],
    stage?.available_equipment || []
  );

  const handleCancel = async () => {
    if (window.confirm(`Confirmer l'annulation du concert de "${artist?.name || 'Artiste'}" ?`)) {
      await cancelConcert(concert.id);
    }
  };

  return (
    <div
      className={`rounded-xl border transition-all duration-200 relative overflow-hidden flex flex-col justify-between ${
        isCancelled
          ? 'bg-hell-darkest/70 border-red-950/60 opacity-60'
          : 'bg-hell-card border-hell-border hover:border-hell-red/60 hover:shadow-flame/30'
      }`}
    >
      {/* Top Banner: Time & Status */}
      <div className="p-3.5 pb-2 border-b border-hell-border/60 flex items-center justify-between gap-2">
        <div className="flex items-center gap-1.5 text-xs font-bold text-hell-steel-bright">
          <Clock className="w-3.5 h-3.5 text-hell-red" />
          <span>{formatTimeSlot(concert.start_time, concert.end_time)}</span>
        </div>

        <div>
          {isCancelled ? (
            <span className="inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800">
              <XCircle className="w-3 h-3" /> Annulé
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800/60">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" /> Programmé
            </span>
          )}
        </div>
      </div>

      {/* Main Body: Artist & Stage Info */}
      <div className="p-4 flex-1">
        <div className="flex items-start justify-between gap-2">
          <div>
            <h4
              className={`font-gothic font-bold text-lg tracking-wide ${
                isCancelled ? 'line-through text-hell-steel' : 'text-white'
              }`}
            >
              {artist?.name || `Artiste #${concert.artist_id}`}
            </h4>
            <div className="flex flex-wrap items-center gap-2 mt-1">
              <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-hell-surface text-hell-steel-light border border-hell-border">
                {artist?.genre || 'Metal'}
              </span>
              <span className="text-xs text-hell-steel flex items-center gap-1">
                <Sparkles className="w-3 h-3 text-amber-500" />
                {stage?.name || `Scène #${concert.stage_id}`}
              </span>
            </div>
          </div>
        </div>

        {/* Equipment Compatibility Status */}
        <div className="mt-3 pt-3 border-t border-hell-border/40">
          {equipmentCheck.ok ? (
            <div className="flex items-center gap-1.5 text-[11px] text-emerald-400">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              <span>Matériel conforme ({artist?.required_equipment.length || 0} requis)</span>
            </div>
          ) : (
            <div className="p-2 rounded bg-red-950/50 border border-red-800/60 text-[11px] text-red-300">
              <div className="flex items-center gap-1 font-bold text-red-400 mb-1">
                <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                <span>Incompatibilité Scène / Matériel !</span>
              </div>
              <p className="text-[10px] text-hell-steel">
                Manquant : {equipmentCheck.missing.map(formatEquipment).join(', ')}
              </p>
            </div>
          )}
        </div>

        {/* Incidents on this concert */}
        {concertIncidents.length > 0 && (
          <div className="mt-2 flex items-center gap-1.5 text-[11px] font-bold text-amber-400 bg-amber-950/40 border border-amber-800/50 px-2 py-1 rounded">
            <FileWarning className="w-3.5 h-3.5 text-amber-400 shrink-0" />
            <span>{concertIncidents.length} incident(s) signalé(s)</span>
          </div>
        )}
      </div>

      {/* Action Footer */}
      <div className="p-2.5 pt-0 flex items-center justify-between gap-1.5 border-t border-hell-border/40 bg-hell-surface/30">
        <button
          onClick={() => onReschedule(concert)}
          disabled={isPublished || isCancelled}
          className={`flex items-center gap-1 px-2.5 py-1.5 rounded text-[11px] font-semibold transition-all ${
            isPublished || isCancelled
              ? 'text-hell-steel/40 cursor-not-allowed'
              : 'text-hell-steel-light hover:text-white hover:bg-hell-surface border border-transparent hover:border-hell-border'
          }`}
          title={isPublished ? 'Modification interdite car festival publié' : 'Déplacer créneau / scène'}
        >
          <CalendarDays className="w-3.5 h-3.5 text-hell-steel" />
          Déplacer
        </button>

        <button
          onClick={() => onDeclareIncident(concert)}
          className="flex items-center gap-1 px-2.5 py-1.5 rounded text-[11px] font-semibold text-amber-400 hover:text-amber-300 hover:bg-amber-950/30 border border-transparent hover:border-amber-900/50 transition-all"
          title="Signaler un incident sur ce concert"
        >
          <Flame className="w-3.5 h-3.5 text-amber-500" />
          Incident
        </button>

        {!isCancelled && (
          <button
            onClick={handleCancel}
            className="flex items-center gap-1 px-2.5 py-1.5 rounded text-[11px] font-semibold text-red-400 hover:text-red-300 hover:bg-red-950/30 border border-transparent hover:border-red-900/50 transition-all"
            title="Annuler ce concert"
          >
            <XCircle className="w-3.5 h-3.5 text-red-500" />
            Annuler
          </button>
        )}
      </div>
    </div>
  );
};

