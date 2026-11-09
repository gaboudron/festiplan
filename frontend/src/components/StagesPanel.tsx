import React from 'react';
import { useFestival } from '../context/FestivalContext';
import { Sparkles, PlusCircle, Users, CheckCircle2, Volume2, Shield } from 'lucide-react';
import { formatEquipment } from '../utils/formatters';

interface StagesPanelProps {
  onOpenCreateStage: () => void;
  onOpenCreateConcert: () => void;
}

export const StagesPanel: React.FC<StagesPanelProps> = ({
  onOpenCreateStage,
  onOpenCreateConcert,
}) => {
  const { stages, concerts, artists, currentFestival } = useFestival();
  const isPublished = currentFestival?.status === 'published';

  const maxCapacity = Math.max(...stages.map((s) => s.capacity), 1);

  return (
    <div className="space-y-6">
      {/* Top Controls */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-hell-surface text-amber-400 border border-hell-border">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-gothic font-bold text-lg text-white">Scènes & Installations Techniques</h2>
            <p className="text-xs text-hell-steel">
              {stages.length} scènes déployées sur le site de {currentFestival?.location || 'FestiPlan'}
            </p>
          </div>
        </div>

        <button
          onClick={onOpenCreateStage}
          className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold uppercase tracking-wider shadow hover:brightness-110 transition-all cursor-pointer"
        >
          <PlusCircle className="w-4 h-4" /> Ajouter une Scène
        </button>
      </div>

      {/* Stages Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {stages.map((stage) => {
          const stageConcerts = concerts.filter((c) => c.stage_id === stage.id && c.status === 'scheduled');
          const stageArtists = stageConcerts.map((c) => artists.find((a) => a.id === c.artist_id)).filter(Boolean);
          const percent = Math.round((stage.capacity / maxCapacity) * 100);

          return (
            <div
              key={stage.id}
              className="bg-hell-card border border-hell-border rounded-xl p-5 flex flex-col justify-between hover:border-amber-500/60 transition-all"
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="font-gothic font-bold text-xl text-white flex items-center gap-2">
                      <span className="w-3 h-3 rounded-full bg-amber-500 shadow-sm" />
                      {stage.name}
                    </h3>
                    <div className="flex items-center gap-1.5 text-xs text-hell-steel mt-1">
                      <Users className="w-3.5 h-3.5 text-amber-500" />
                      <span>Capacité maximale : <strong className="text-white">{stage.capacity.toLocaleString('fr-FR')}</strong> festivaliers</span>
                    </div>
                  </div>

                  <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-hell-surface border border-hell-border text-hell-steel-bright">
                    {stageConcerts.length} sets prévus
                  </span>
                </div>

                {/* Capacity Visual Gauge */}
                <div className="mt-4">
                  <div className="w-full bg-hell-surface h-2 rounded-full overflow-hidden border border-hell-border/60">
                    <div
                      className="bg-gradient-to-r from-amber-600 to-amber-400 h-full rounded-full transition-all duration-500"
                      style={{ width: `${percent}%` }}
                    />
                  </div>
                  <div className="flex justify-between items-center text-[10px] text-hell-steel mt-1">
                    <span>Jauge arène</span>
                    <span>{percent}% de la plus grande scène</span>
                  </div>
                </div>

                {/* Available Equipments */}
                <div className="mt-4 pt-3 border-t border-hell-border/60">
                  <span className="text-[10px] uppercase font-bold tracking-wider text-hell-steel block mb-2 flex items-center gap-1">
                    <Shield className="w-3 h-3 text-amber-500" /> Régie & Équipements Installés :
                  </span>
                  {stage.available_equipment.length === 0 ? (
                    <span className="text-xs text-hell-steel/60 italic">
                      Équipements standards uniquement
                    </span>
                  ) : (
                    <div className="flex flex-wrap gap-1.5">
                      {stage.available_equipment.map((eq) => (
                        <span
                          key={eq}
                          className="text-[11px] font-semibold px-2.5 py-1 rounded bg-amber-950/30 text-amber-300 border border-amber-800/40 flex items-center gap-1"
                        >
                          <CheckCircle2 className="w-3 h-3 text-amber-400 shrink-0" />
                          {formatEquipment(eq)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Programmed Artists on this Stage */}
                {stageArtists.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-hell-border/40">
                    <span className="text-[10px] uppercase font-bold tracking-wider text-hell-steel block mb-1.5">
                      Groupes programmés sur cette scène :
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {stageArtists.slice(0, 5).map((a, idx) => (
                        <span
                          key={idx}
                          className="text-[10px] font-medium px-2 py-0.5 rounded bg-hell-surface text-hell-steel-light border border-hell-border"
                        >
                          {a?.name}
                        </span>
                      ))}
                      {stageArtists.length > 5 && (
                        <span className="text-[10px] text-hell-steel px-1">
                          +{stageArtists.length - 5} autres
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Action */}
              {!isPublished && (
                <div className="mt-5 pt-3 border-t border-hell-border/40 flex justify-end">
                  <button
                    onClick={onOpenCreateConcert}
                    className="text-xs font-semibold text-amber-400 hover:text-amber-300 flex items-center gap-1"
                  >
                    <Volume2 className="w-3.5 h-3.5" /> Programmer un concert sur {stage.name}
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

