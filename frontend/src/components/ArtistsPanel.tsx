import React, { useState, useMemo } from 'react';
import { useFestival } from '../context/FestivalContext';
import { Search, PlusCircle, Users, Sparkles, Music, Volume2 } from 'lucide-react';
import { formatEquipment } from '../utils/formatters';

interface ArtistsPanelProps {
  onOpenCreateArtist: () => void;
  onOpenCreateConcert: () => void;
}

export const ArtistsPanel: React.FC<ArtistsPanelProps> = ({
  onOpenCreateArtist,
  onOpenCreateConcert,
}) => {
  const { artists, concerts, currentFestival } = useFestival();
  const [search, setSearch] = useState<string>('');
  const [selectedGenre, setSelectedGenre] = useState<string>('all');

  const isPublished = currentFestival?.status === 'published';

  // Compute unique genres
  const genres = useMemo(() => {
    const set = new Set<string>();
    artists.forEach((a) => {
      if (a.genre) set.add(a.genre);
    });
    return Array.from(set).sort();
  }, [artists]);

  const filteredArtists = useMemo(() => {
    return artists.filter((artist) => {
      if (selectedGenre !== 'all' && artist.genre !== selectedGenre) {
        return false;
      }
      if (search.trim()) {
        const q = search.toLowerCase();
        return (
          artist.name.toLowerCase().includes(q) ||
          artist.genre.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [artists, selectedGenre, search]);

  return (
    <div className="space-y-6">
      {/* Top Controls */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-hell-surface text-hell-steel-bright border border-hell-border">
            <Users className="w-5 h-5 text-hell-red" />
          </div>
          <div>
            <h2 className="font-gothic font-bold text-lg text-white">Lineup & Artistes</h2>
            <p className="text-xs text-hell-steel">
              {artists.length} groupes enregistrés sur l'infrastructure FestiPlan
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Search box */}
          <div className="relative flex-1 sm:w-64">
            <Search className="w-4 h-4 text-hell-steel absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Rechercher un groupe..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-hell-surface border border-hell-border rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-hell-steel focus:outline-none focus:border-hell-red"
            />
          </div>

          <button
            onClick={onOpenCreateArtist}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-hell-red text-white text-xs font-bold uppercase tracking-wider shadow-flame hover:brightness-110 transition-all cursor-pointer"
          >
            <PlusCircle className="w-4 h-4" /> Ajouter un Artiste
          </button>
        </div>
      </div>

      {/* Genre Filter Chips */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => setSelectedGenre('all')}
          className={`px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider transition-all ${
            selectedGenre === 'all'
              ? 'bg-hell-red text-white shadow-flame'
              : 'bg-hell-card text-hell-steel hover:text-white border border-hell-border'
          }`}
        >
          Tous ({artists.length})
        </button>
        {genres.map((g) => {
          const count = artists.filter((a) => a.genre === g).length;
          return (
            <button
              key={g}
              onClick={() => setSelectedGenre(g)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                selectedGenre === g
                  ? 'bg-hell-red text-white shadow-flame'
                  : 'bg-hell-card text-hell-steel hover:text-white border border-hell-border'
              }`}
            >
              {g} ({count})
            </button>
          );
        })}
      </div>

      {/* Artists Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredArtists.map((artist) => {
          const artistShows = concerts.filter((c) => c.artist_id === artist.id);
          const scheduledShows = artistShows.filter((c) => c.status === 'scheduled');

          return (
            <div
              key={artist.id}
              className="bg-hell-card border border-hell-border rounded-xl p-5 flex flex-col justify-between hover:border-hell-red/60 hover:shadow-flame/20 transition-all group"
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="font-gothic font-bold text-lg text-white group-hover:text-red-400 transition-colors">
                      {artist.name}
                    </h3>
                    <span className="inline-block mt-1 text-[11px] font-semibold px-2 py-0.5 rounded bg-hell-surface text-hell-steel-light border border-hell-border">
                      {artist.genre}
                    </span>
                  </div>
                  <div className="p-2 rounded-lg bg-hell-surface text-hell-steel group-hover:text-hell-red transition-colors">
                    <Music className="w-4 h-4" />
                  </div>
                </div>

                {/* Technical Rider / Equipments */}
                <div className="mt-4 pt-3 border-t border-hell-border/60">
                  <span className="text-[10px] uppercase font-bold tracking-wider text-hell-steel block mb-1.5">
                    Rider Technique Requis :
                  </span>
                  {artist.required_equipment.length === 0 ? (
                    <span className="text-xs text-hell-steel/60 italic">
                      Aucun équipement lourd spécifique (Standard)
                    </span>
                  ) : (
                    <div className="flex flex-wrap gap-1.5">
                      {artist.required_equipment.map((eq) => (
                        <span
                          key={eq}
                          className="text-[10px] font-semibold px-2 py-0.5 rounded bg-hell-surface text-red-300 border border-red-900/60"
                        >
                          ⚡ {formatEquipment(eq)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Footer: Shows count & action */}
              <div className="mt-5 pt-3 border-t border-hell-border/40 flex items-center justify-between text-xs">
                <span className="text-hell-steel flex items-center gap-1.5">
                  <Volume2 className="w-3.5 h-3.5 text-hell-red" />
                  {scheduledShows.length} concert(s) prévu(s)
                </span>

                {!isPublished && (
                  <button
                    onClick={onOpenCreateConcert}
                    className="text-xs font-semibold text-hell-red hover:text-red-400 flex items-center gap-1"
                  >
                    <Sparkles className="w-3 h-3" /> Programmer
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

