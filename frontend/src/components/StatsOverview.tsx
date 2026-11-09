import React from 'react';
import { useFestival } from '../context/FestivalContext';
import { Users, Sparkles, Volume2, AlertTriangle, ShieldCheck, Flame } from 'lucide-react';
import { checkEquipmentMatch } from '../utils/formatters';

export const StatsOverview: React.FC = () => {
  const { currentFestival, stages, artists, concerts, incidents } = useFestival();

  if (!currentFestival) return null;

  const totalCapacity = stages.reduce((acc, s) => acc + s.capacity, 0);
  const scheduledCount = concerts.filter((c) => c.status === 'scheduled').length;
  const cancelledCount = concerts.filter((c) => c.status === 'cancelled').length;
  const activeIncidents = incidents.filter((i) => !i.resolved).length;

  // Count equipment warnings among scheduled concerts
  const equipmentWarnings = concerts.filter((c) => {
    if (c.status !== 'scheduled') return false;
    const artist = artists.find((a) => a.id === c.artist_id);
    const stage = stages.find((s) => s.id === c.stage_id);
    if (!artist || !stage) return false;
    const { ok } = checkEquipmentMatch(artist.required_equipment, stage.available_equipment);
    return !ok;
  }).length;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3 mb-6">
      {/* Stages & Capacity */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-4 relative overflow-hidden group hover:border-hell-steel transition-all">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-hell-steel">Scènes Déployées</span>
          <div className="p-2 rounded-lg bg-hell-surface text-amber-500">
            <Sparkles className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-black text-white font-gothic">{stages.length}</span>
          <span className="text-xs text-hell-steel">scènes</span>
        </div>
        <p className="text-[11px] text-hell-steel/80 mt-1 truncate">
          Jauge totale : {totalCapacity.toLocaleString('fr-FR')} festivaliers
        </p>
        <div className="absolute -bottom-6 -right-6 w-16 h-16 bg-amber-500/5 rounded-full blur-xl group-hover:bg-amber-500/10 transition-all" />
      </div>

      {/* Bands / Lineup */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-4 relative overflow-hidden group hover:border-hell-steel transition-all">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-hell-steel">Artistes Au Lineup</span>
          <div className="p-2 rounded-lg bg-hell-surface text-hell-steel-bright">
            <Users className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-black text-white font-gothic">{artists.length}</span>
          <span className="text-xs text-hell-steel">groupes</span>
        </div>
        <p className="text-[11px] text-hell-steel/80 mt-1">
          Heavy, Thrash, Stoner, Doom...
        </p>
        <div className="absolute -bottom-6 -right-6 w-16 h-16 bg-white/5 rounded-full blur-xl group-hover:bg-white/10 transition-all" />
      </div>

      {/* Shows planned */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-4 relative overflow-hidden group hover:border-hell-red transition-all">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-hell-steel">Concerts Prévus</span>
          <div className="p-2 rounded-lg bg-hell-surface text-hell-red">
            <Volume2 className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-black text-hell-red font-gothic">{scheduledCount}</span>
          {cancelledCount > 0 && (
            <span className="text-xs text-hell-steel">({cancelledCount} annulés)</span>
          )}
        </div>
        <p className="text-[11px] text-hell-steel/80 mt-1 flex items-center gap-1">
          <Flame className="w-3 h-3 text-hell-red" /> Planning sous contrôle
        </p>
        <div className="absolute -bottom-6 -right-6 w-16 h-16 bg-hell-red/10 rounded-full blur-xl group-hover:bg-hell-red/20 transition-all" />
      </div>

      {/* Incidents */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-4 relative overflow-hidden group hover:border-red-500 transition-all">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-hell-steel">Tour d'Incidents</span>
          <div className="p-2 rounded-lg bg-hell-surface text-red-500">
            <AlertTriangle className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className={`text-2xl font-black font-gothic ${incidents.length > 0 ? 'text-red-400' : 'text-emerald-400'}`}>
            {incidents.length}
          </span>
          <span className="text-xs text-hell-steel">déclarés</span>
        </div>
        <p className="text-[11px] text-hell-steel/80 mt-1">
          {activeIncidents > 0 ? `${activeIncidents} en cours d'intervention` : 'Régie & Sécurité nominale'}
        </p>
        <div className="absolute -bottom-6 -right-6 w-16 h-16 bg-red-600/10 rounded-full blur-xl group-hover:bg-red-600/20 transition-all" />
      </div>

      {/* Equipment & Rules Status */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-4 relative overflow-hidden group hover:border-hell-green transition-all col-span-2 md:col-span-4 lg:col-span-1">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-hell-steel">Conformité Matériel</span>
          <div className="p-2 rounded-lg bg-hell-surface text-hell-green-acid">
            <ShieldCheck className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          {equipmentWarnings === 0 ? (
            <span className="text-2xl font-black text-hell-green-acid font-gothic">100%</span>
          ) : (
            <span className="text-2xl font-black text-amber-400 font-gothic">{equipmentWarnings} alerte</span>
          )}
        </div>
        <p className="text-[11px] text-hell-steel/80 mt-1">
          {equipmentWarnings === 0 ? 'Toutes scènes compatibles' : 'Matériel requis manquant sur scène'}
        </p>
        <div className="absolute -bottom-6 -right-6 w-16 h-16 bg-hell-green/10 rounded-full blur-xl group-hover:bg-hell-green/20 transition-all" />
      </div>
    </div>
  );
};

