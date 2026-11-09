import React, { useState } from 'react';
import { useFestival } from '../context/FestivalContext';
import {
  AlertTriangle,
  Flame,
  CheckCircle2,
  Clock,
  ShieldCheck,
  PlusCircle,
} from 'lucide-react';
import { formatDateFull, formatTime, formatTimeSlot } from '../utils/formatters';

interface IncidentsPanelProps {
  onOpenDeclareIncident: () => void;
}

export const IncidentsPanel: React.FC<IncidentsPanelProps> = ({
  onOpenDeclareIncident,
}) => {
  const { incidents, concerts, artists, stages, resolveIncident } = useFestival();
  const [filterResolved, setFilterResolved] = useState<string>('all');
  const [resolvingId, setResolvingId] = useState<number | null>(null);

  const handleResolve = async (incidentId: number) => {
    setResolvingId(incidentId);
    await resolveIncident(incidentId);
    setResolvingId(null);
  };

  const filteredIncidents = incidents.filter((inc) => {
    if (filterResolved === 'active') return !inc.resolved;
    if (filterResolved === 'resolved') return inc.resolved;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-red-950/80 text-red-500 border border-red-800">
            <AlertTriangle className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h2 className="font-gothic font-bold text-lg text-white">Tour de Contrôle des Incidents</h2>
            <p className="text-xs text-hell-steel">
              Journal en direct de la régie technique, pannes et interventions de sécurité
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Filter */}
          <div className="flex items-center bg-hell-surface border border-hell-border rounded-lg p-1 text-xs">
            <button
              onClick={() => setFilterResolved('all')}
              className={`px-3 py-1 rounded font-semibold transition-all ${
                filterResolved === 'all' ? 'bg-hell-card text-white shadow' : 'text-hell-steel hover:text-white'
              }`}
            >
              Tous ({incidents.length})
            </button>
            <button
              onClick={() => setFilterResolved('active')}
              className={`px-3 py-1 rounded font-semibold transition-all ${
                filterResolved === 'active' ? 'bg-red-900/60 text-red-300 shadow' : 'text-hell-steel hover:text-white'
              }`}
            >
              En cours ({incidents.filter((i) => !i.resolved).length})
            </button>
            <button
              onClick={() => setFilterResolved('resolved')}
              className={`px-3 py-1 rounded font-semibold transition-all ${
                filterResolved === 'resolved' ? 'bg-emerald-900/60 text-emerald-300 shadow' : 'text-hell-steel hover:text-white'
              }`}
            >
              Résolus ({incidents.filter((i) => i.resolved).length})
            </button>
          </div>

          <button
            onClick={onOpenDeclareIncident}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-bold uppercase tracking-wider shadow-flame hover:brightness-110 transition-all cursor-pointer"
          >
            <PlusCircle className="w-4 h-4" /> Signaler un Incident
          </button>
        </div>
      </div>

      {/* Incidents List */}
      {filteredIncidents.length === 0 ? (
        <div className="text-center py-20 bg-hell-card border border-hell-border rounded-xl">
          <ShieldCheck className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
          <h3 className="text-xl font-bold font-gothic text-white">Régie Technique Nominale</h3>
          <p className="text-xs text-hell-steel mt-1 max-w-md mx-auto">
            Aucun incident technique ou de sécurité n'est actuellement à signaler sur le festival.
          </p>
          <button
            onClick={onOpenDeclareIncident}
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-hell-surface border border-hell-border text-hell-steel-bright hover:text-white text-xs font-semibold transition-all"
          >
            <Flame className="w-4 h-4 text-red-500" /> Signaler un incident en direct
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredIncidents.map((incident) => {
            const concert = concerts.find((c) => c.id === incident.concert_id);
            const artist = concert ? artists.find((a) => a.id === concert.artist_id) : null;
            const stage = concert ? stages.find((s) => s.id === concert.stage_id) : null;

            return (
              <div
                key={incident.id}
                className="bg-hell-card border border-hell-border hover:border-red-900/60 rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 transition-all"
              >
                <div className="flex items-start gap-3 flex-1">
                  <div
                    className={`p-2 rounded-lg shrink-0 mt-0.5 ${
                      incident.resolved
                        ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                        : 'bg-red-950 text-red-400 border border-red-800 animate-pulse'
                    }`}
                  >
                    {incident.resolved ? (
                      <CheckCircle2 className="w-5 h-5" />
                    ) : (
                      <AlertTriangle className="w-5 h-5" />
                    )}
                  </div>

                  <div className="space-y-1 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-gothic font-bold text-base text-white">
                        Incident #{incident.id}
                      </span>
                      {incident.resolved ? (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-emerald-950/80 text-emerald-300 border border-emerald-800">
                          Résolu
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-red-950/80 text-red-300 border border-red-800">
                          En cours d'intervention
                        </span>
                      )}
                      <span className="text-xs text-hell-steel flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        Signalé le {formatDateFull(incident.occurred_at)} à {formatTime(incident.occurred_at)}
                      </span>
                    </div>

                    <p className="text-sm text-hell-steel-light leading-relaxed pt-1">
                      {incident.description}
                    </p>

                    {/* Associated Concert & Stage */}
                    {concert && (
                      <div className="pt-2 flex flex-wrap items-center gap-2 text-xs text-hell-steel">
                        <span>Concert :</span>
                        <strong className="text-white">{artist?.name || `Artiste #${concert.artist_id}`}</strong>
                        <span>sur</span>
                        <span className="text-amber-400 font-semibold">{stage?.name || `Scène #${concert.stage_id}`}</span>
                        <span>({formatTimeSlot(concert.start_time, concert.end_time)})</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Action button to mark as resolved */}
                {!incident.resolved && (
                  <div className="shrink-0 pt-2 md:pt-0">
                    <button
                      onClick={() => handleResolve(incident.id)}
                      disabled={resolvingId === incident.id}
                      className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-emerald-950/80 hover:bg-emerald-900 border border-emerald-600/80 text-emerald-300 hover:text-white text-xs font-bold transition-all shadow-acid/40 hover:shadow-acid disabled:opacity-50 cursor-pointer"
                      title="Marquer cet incident comme résolu"
                    >
                      <CheckCircle2 className={`w-4 h-4 text-emerald-400 ${resolvingId === incident.id ? 'animate-spin' : ''}`} />
                      <span>{resolvingId === incident.id ? 'Clôture en cours...' : 'Marquer comme résolu'}</span>
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
