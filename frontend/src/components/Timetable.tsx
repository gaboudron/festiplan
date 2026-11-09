import React, { useState, useMemo } from 'react';
import { useFestival } from '../context/FestivalContext';
import { Concert } from '../api/types';
import { ConcertCard } from './ConcertCard';
import {
  Calendar,
  Filter,
  Search,
  Sparkles,
  LayoutGrid,
  List,
  AlertCircle,
  PlusCircle,
} from 'lucide-react';
import { formatDateFull, getDayKey } from '../utils/formatters';

interface TimetableProps {
  onOpenCreateConcert: () => void;
  onReschedule: (concert: Concert) => void;
  onDeclareIncident: (concert: Concert) => void;
}

export const Timetable: React.FC<TimetableProps> = ({
  onOpenCreateConcert,
  onReschedule,
  onDeclareIncident,
}) => {
  const { currentFestival, concerts, stages, artists } = useFestival();

  const [selectedDay, setSelectedDay] = useState<string>('all');
  const [selectedStageId, setSelectedStageId] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [viewMode, setViewMode] = useState<'columns' | 'grid'>('columns');

  // Compute unique days from concerts and festival start/end
  const days = useMemo(() => {
    const daySet = new Set<string>();
    concerts.forEach((c) => {
      daySet.add(getDayKey(c.start_time));
    });
    return Array.from(daySet).sort();
  }, [concerts]);

  // Set default day to first day if available and selectedDay is 'all'
  // (We keep 'all' as an option too)

  // Filtered concerts
  const filteredConcerts = useMemo(() => {
    return concerts.filter((concert) => {
      // Day filter
      if (selectedDay !== 'all') {
        const concertDay = getDayKey(concert.start_time);
        if (concertDay !== selectedDay) return false;
      }

      // Stage filter
      if (selectedStageId !== 'all') {
        if (concert.stage_id !== Number(selectedStageId)) return false;
      }

      // Search filter (artist name or genre)
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        const artist = artists.find((a) => a.id === concert.artist_id);
        const stage = stages.find((s) => s.id === concert.stage_id);
        const artistName = artist?.name.toLowerCase() || '';
        const genre = artist?.genre.toLowerCase() || '';
        const stageName = stage?.name.toLowerCase() || '';
        return (
          artistName.includes(query) ||
          genre.includes(query) ||
          stageName.includes(query)
        );
      }

      return true;
    });
  }, [concerts, selectedDay, selectedStageId, searchQuery, artists, stages]);

  // Sort concerts chronologically
  const sortedConcerts = useMemo(() => {
    return [...filteredConcerts].sort(
      (a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime()
    );
  }, [filteredConcerts]);

  if (!currentFestival) {
    return (
      <div className="text-center py-20 bg-hell-card border border-hell-border rounded-xl">
        <AlertCircle className="w-12 h-12 text-hell-red mx-auto mb-3" />
        <h3 className="text-xl font-bold font-gothic text-white">Aucun festival sélectionné</h3>
        <p className="text-sm text-hell-steel mt-1">Créez ou sélectionnez un festival pour afficher le running order.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filters & Control Bar */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-4 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Day selection tabs */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => setSelectedDay('all')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider transition-all ${
              selectedDay === 'all'
                ? 'bg-hell-red text-white shadow-flame'
                : 'bg-hell-surface text-hell-steel hover:text-white border border-hell-border'
            }`}
          >
            Tous les jours ({concerts.length})
          </button>
          {days.map((day) => {
            const dayShows = concerts.filter((c) => getDayKey(c.start_time) === day).length;
            return (
              <button
                key={day}
                onClick={() => setSelectedDay(day)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider transition-all flex items-center gap-1.5 ${
                  selectedDay === day
                    ? 'bg-hell-red text-white shadow-flame'
                    : 'bg-hell-surface text-hell-steel hover:text-white border border-hell-border'
                }`}
              >
                <Calendar className="w-3.5 h-3.5" />
                <span>{formatDateFull(day)}</span>
                <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-black/40">
                  {dayShows}
                </span>
              </button>
            );
          })}
        </div>

        {/* Search, Stage Filter & View Toggle */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Search box */}
          <div className="relative flex-1 sm:w-60">
            <Search className="w-4 h-4 text-hell-steel absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Rechercher groupe, genre..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-hell-surface border border-hell-border rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-hell-steel focus:outline-none focus:border-hell-red"
            />
          </div>

          {/* Stage Filter */}
          <div className="flex items-center bg-hell-surface border border-hell-border rounded-lg px-2.5 py-1.5">
            <Filter className="w-3.5 h-3.5 text-hell-steel mr-1.5" />
            <select
              aria-label="Filtrer par scène"
              value={selectedStageId}
              onChange={(e) => setSelectedStageId(e.target.value)}
              className="bg-transparent text-xs font-semibold text-hell-steel-bright focus:outline-none cursor-pointer"
            >
              <option value="all" className="bg-hell-card text-white">Toutes les scènes</option>
              {stages.map((stage) => (
                <option key={stage.id} value={stage.id} className="bg-hell-card text-white">
                  {stage.name} ({stage.capacity.toLocaleString('fr-FR')}p)
                </option>
              ))}
            </select>
          </div>

          {/* View Mode Toggle */}
          <div className="flex items-center bg-hell-surface border border-hell-border rounded-lg p-1">
            <button
              onClick={() => setViewMode('columns')}
              className={`p-1.5 rounded text-xs transition-all ${
                viewMode === 'columns' ? 'bg-hell-card text-white shadow' : 'text-hell-steel hover:text-white'
              }`}
              title="Vue par Scènes (Colonnes Hellfest)"
              aria-label="Vue par Scènes (Colonnes Hellfest)"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded text-xs transition-all ${
                viewMode === 'grid' ? 'bg-hell-card text-white shadow' : 'text-hell-steel hover:text-white'
              }`}
              title="Vue Chronologique"
              aria-label="Vue Chronologique"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Empty State */}
      {sortedConcerts.length === 0 ? (
        <div className="text-center py-16 bg-hell-card border border-hell-border rounded-xl">
          <Sparkles className="w-12 h-12 text-hell-steel/50 mx-auto mb-3" />
          <h4 className="text-lg font-bold font-gothic text-white">Aucun concert correspondant</h4>
          <p className="text-xs text-hell-steel mt-1 max-w-md mx-auto">
            {searchQuery
              ? `Aucun résultat pour "${searchQuery}". Essayez une autre recherche.`
              : 'Aucun concert n’a encore été programmé sur cette sélection.'}
          </p>
          {currentFestival.status !== 'published' && (
            <button
              onClick={onOpenCreateConcert}
              className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-hell-red text-white text-xs font-bold uppercase tracking-wider shadow-flame hover:brightness-110 transition-all"
            >
              <PlusCircle className="w-4 h-4" /> Programmer un concert
            </button>
          )}
        </div>
      ) : viewMode === 'columns' && selectedStageId === 'all' ? (
        /* Hellfest-style Stage Columns */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 items-start">
          {stages.map((stage) => {
            const stageConcerts = sortedConcerts.filter((c) => c.stage_id === stage.id);
            return (
              <div
                key={stage.id}
                className="bg-hell-darkest/80 border border-hell-border rounded-xl overflow-hidden flex flex-col"
              >
                {/* Stage Header */}
                <div className="p-3 bg-hell-surface border-b border-hell-border flex items-center justify-between">
                  <div>
                    <h3 className="font-gothic font-bold text-sm text-white tracking-wider flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full bg-hell-red" />
                      {stage.name}
                    </h3>
                    <span className="text-[10px] text-hell-steel">
                      Capacité : {stage.capacity.toLocaleString('fr-FR')} festivaliers
                    </span>
                  </div>
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-hell-card text-hell-steel-light border border-hell-border">
                    {stageConcerts.length}
                  </span>
                </div>

                {/* Stage Concerts List */}
                <div className="p-3 space-y-3 min-h-[160px]">
                  {stageConcerts.length === 0 ? (
                    <div className="text-center py-8 text-xs text-hell-steel/60 italic">
                      Scène libre sur ce créneau
                    </div>
                  ) : (
                    stageConcerts.map((concert) => {
                      const artist = artists.find((a) => a.id === concert.artist_id);
                      return (
                        <ConcertCard
                          key={concert.id}
                          concert={concert}
                          artist={artist}
                          stage={stage}
                          onReschedule={onReschedule}
                          onDeclareIncident={onDeclareIncident}
                        />
                      );
                    })
                  )}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* Unified Grid / Timeline */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sortedConcerts.map((concert) => {
            const artist = artists.find((a) => a.id === concert.artist_id);
            const stage = stages.find((s) => s.id === concert.stage_id);
            return (
              <ConcertCard
                key={concert.id}
                concert={concert}
                artist={artist}
                stage={stage}
                onReschedule={onReschedule}
                onDeclareIncident={onDeclareIncident}
              />
            );
          })}
        </div>
      )}
    </div>
  );
};

