import React from 'react';
import { useFestival } from '../context/FestivalContext';
import {
  Flame,
  ShieldCheck,
  Calendar,
  MapPin,
  PlusCircle,
  Radio,
  RefreshCw,
  Lock,
  Unlock,
  AlertOctagon,
  Sparkles,
} from 'lucide-react';
import { formatDateFull } from '../utils/formatters';

interface HeaderProps {
  onOpenCreateConcert: () => void;
  onOpenCreateFestival: () => void;
  onOpenPublish: () => void;
  activeTab: 'timetable' | 'artists' | 'stages' | 'incidents' | 'architecture';
  setActiveTab: (tab: 'timetable' | 'artists' | 'stages' | 'incidents' | 'architecture') => void;
}

export const Header: React.FC<HeaderProps> = ({
  onOpenCreateConcert,
  onOpenCreateFestival,
  onOpenPublish,
  activeTab,
  setActiveTab,
}) => {
  const {
    festivals,
    currentFestival,
    setCurrentFestivalId,
    refreshData,
    isLoading,
    incidents,
  } = useFestival();

  const isPublished = currentFestival?.status === 'published';

  return (
    <header className="border-b border-hell-border bg-hell-darkest/90 backdrop-blur-md sticky top-0 z-40">
      {/* Top Hellfest Brand Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          {/* Logo & Festival Info */}
          <div className="flex items-center gap-4">
            <div className="relative group">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-hell-red via-hell-red-dark to-black p-0.5 shadow-flame flex items-center justify-center transition-transform group-hover:scale-105">
                <div className="w-full h-full bg-hell-card rounded-[10px] flex items-center justify-center">
                  <Flame className="w-8 h-8 text-hell-red animate-flame" />
                </div>
              </div>
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-hell-green-acid rounded-full border-2 border-hell-darkest shadow-acid animate-pulse" />
            </div>

            <div>
              <div className="flex items-center gap-3">
                <h1 className="font-gothic font-black text-2xl sm:text-3xl tracking-wider text-hell-steel-bright">
                  FESTI<span className="text-hell-red">PLAN</span>
                </h1>
              </div>
            </div>
          </div>

          {/* Festival Switcher & Controls */}
          <div className="flex flex-wrap items-center gap-3">
            {/* Festival Selector Dropdown */}
            <div className="flex items-center bg-hell-card border border-hell-border rounded-lg px-3 py-1.5 focus-within:border-hell-red">
              <Calendar className="w-4 h-4 text-hell-steel mr-2" />
              <select
                aria-label="Sélectionner un festival"
                value={currentFestival?.id || ''}
                onChange={(e) => setCurrentFestivalId(Number(e.target.value))}
                className="bg-transparent text-sm font-semibold text-hell-steel-bright focus:outline-none cursor-pointer"
              >
                {festivals.map((fest) => (
                  <option key={fest.id} value={fest.id} className="bg-hell-card text-white">
                    {fest.name} ({fest.status.toUpperCase()})
                  </option>
                ))}
              </select>
            </div>

            {/* Sync Refresh Button */}
            <button
              onClick={() => refreshData()}
              disabled={isLoading}
              className="p-2 rounded-lg bg-hell-card border border-hell-border text-hell-steel hover:text-white hover:border-hell-steel transition-all disabled:opacity-50"
              title="Rafraîchir les données"
              aria-label="Rafraîchir les données"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-hell-red' : ''}`} />
            </button>

            {/* Create Festival button */}
            <button
              onClick={onOpenCreateFestival}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-hell-surface border border-hell-border hover:border-hell-steel text-xs font-semibold text-hell-steel-bright transition-all"
            >
              <PlusCircle className="w-3.5 h-3.5 text-hell-steel" />
              Nouveau Festival
            </button>

            {/* Publish Festival or Locked Badge */}
            {currentFestival && !isPublished ? (
              <button
                onClick={onOpenPublish}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-hell-green-dark via-hell-green to-emerald-500 text-white font-bold text-xs uppercase tracking-wider shadow-acid hover:shadow-acid-lg hover:brightness-110 transition-all cursor-pointer"
              >
                <Unlock className="w-4 h-4 text-hell-green-glow" />
                Publier le Festival
              </button>
            ) : currentFestival && isPublished ? (
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-hell-green-dark/40 border border-hell-green/50 text-hell-green-acid text-xs font-bold tracking-wide">
                <Lock className="w-3.5 h-3.5" />
                Publié
              </div>
            ) : null}

            {/* Program Concert CTA */}
            <button
              onClick={onOpenCreateConcert}
              disabled={isPublished}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-bold text-xs uppercase tracking-wider transition-all ${
                isPublished
                  ? 'bg-hell-card text-hell-steel border border-hell-border cursor-not-allowed opacity-60'
                  : 'bg-gradient-to-r from-hell-red-dark via-hell-red to-orange-600 text-white shadow-flame hover:shadow-flame-lg hover:scale-[1.02] cursor-pointer'
              }`}
              title={isPublished ? 'Le festival est publié : modifications bloquées (Règle R7)' : 'Ajouter un concert'}
            >
              <PlusCircle className="w-4 h-4" />
              Programmer un Concert
            </button>
          </div>
        </div>

        {/* Festival Sub-banner (Status & Location) */}
        {currentFestival && (
          <div className="mt-4 pt-3 border-t border-hell-border/60 flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex flex-wrap items-center gap-4 text-hell-steel">
              <span className="flex items-center gap-1.5 text-hell-steel-light font-medium">
                <MapPin className="w-3.5 h-3.5 text-hell-red" />
                {currentFestival.location}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5 text-hell-steel" />
                Du {formatDateFull(currentFestival.start_date)} au {formatDateFull(currentFestival.end_date)}
              </span>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-hell-steel text-[11px] uppercase tracking-wider">Statut :</span>
              {isPublished ? (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-950/80 border border-emerald-500/50 text-emerald-400 font-bold tracking-wide">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  PUBLIÉ (Règle R7 Verrouillée)
                </span>
              ) : (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-red-950/80 border border-red-500/50 text-red-400 font-bold tracking-wide">
                  <Flame className="w-3.5 h-3.5 text-red-500 animate-pulse" />
                  EN PRÉPARATION (Modifiable)
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex overflow-x-auto gap-2 no-scrollbar border-t border-hell-border/40">
        <button
          onClick={() => setActiveTab('timetable')}
          className={`flex items-center gap-2 py-3 px-4 text-xs font-bold uppercase tracking-wider border-b-2 transition-all shrink-0 ${
            activeTab === 'timetable'
              ? 'border-hell-red text-white bg-hell-card/50'
              : 'border-transparent text-hell-steel hover:text-white hover:border-hell-border'
          }`}
        >
          <Calendar className="w-4 h-4 text-hell-red" />
          Running Order (Programmation)
        </button>

        <button
          onClick={() => setActiveTab('artists')}
          className={`flex items-center gap-2 py-3 px-4 text-xs font-bold uppercase tracking-wider border-b-2 transition-all shrink-0 ${
            activeTab === 'artists'
              ? 'border-hell-red text-white bg-hell-card/50'
              : 'border-transparent text-hell-steel hover:text-white hover:border-hell-border'
          }`}
        >
          <Radio className="w-4 h-4 text-hell-steel-light" />
          Lineup & Artistes
        </button>

        <button
          onClick={() => setActiveTab('stages')}
          className={`flex items-center gap-2 py-3 px-4 text-xs font-bold uppercase tracking-wider border-b-2 transition-all shrink-0 ${
            activeTab === 'stages'
              ? 'border-hell-red text-white bg-hell-card/50'
              : 'border-transparent text-hell-steel hover:text-white hover:border-hell-border'
          }`}
        >
          <Sparkles className="w-4 h-4 text-amber-500" />
          Scènes & Matériel
        </button>

        <button
          onClick={() => setActiveTab('incidents')}
          className={`flex items-center gap-2 py-3 px-4 text-xs font-bold uppercase tracking-wider border-b-2 transition-all shrink-0 relative ${
            activeTab === 'incidents'
              ? 'border-hell-red text-white bg-hell-card/50'
              : 'border-transparent text-hell-steel hover:text-white hover:border-hell-border'
          }`}
        >
          <AlertOctagon className="w-4 h-4 text-red-500" />
          Tour d'Incidents
          {incidents.length > 0 && (
            <span className="ml-1 px-1.5 py-0.2 rounded-full bg-red-600 text-white text-[10px] font-bold">
              {incidents.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('architecture')}
          className={`flex items-center gap-2 py-3 px-4 text-xs font-bold uppercase tracking-wider border-b-2 transition-all shrink-0 ${
            activeTab === 'architecture'
              ? 'border-hell-green text-white bg-hell-card/50'
              : 'border-transparent text-hell-steel hover:text-white hover:border-hell-border'
          }`}
        >
          <ShieldCheck className="w-4 h-4 text-hell-green-acid" />
          Hexa & DDD Invariants
        </button>
      </div>
    </header>
  );
};

