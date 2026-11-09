import React, { useState } from 'react';
import { FestivalProvider } from './context/FestivalContext';
import { Header } from './components/Header';
import { StatsOverview } from './components/StatsOverview';
import { Timetable } from './components/Timetable';
import { ArtistsPanel } from './components/ArtistsPanel';
import { StagesPanel } from './components/StagesPanel';
import { IncidentsPanel } from './components/IncidentsPanel';
import { ArchitectureInfoPanel } from './components/ArchitectureInfoPanel';
import { CreateConcertModal } from './components/CreateConcertModal';
import { RescheduleModal } from './components/RescheduleModal';
import { DeclareIncidentModal } from './components/DeclareIncidentModal';
import { CreateFestivalModal } from './components/CreateFestivalModal';
import { CreateStageModal } from './components/CreateStageModal';
import { CreateArtistModal } from './components/CreateArtistModal';
import { PublishModal } from './components/PublishModal';
import { ToastContainer } from './components/Toast';
import { Concert } from './api/types';
import { Flame, GitFork, Shield } from 'lucide-react';

export const FestiPlanApp: React.FC = () => {
  const [activeTab, setActiveTab] = useState<
    'timetable' | 'artists' | 'stages' | 'incidents' | 'architecture'
  >('timetable');

  // Modal states
  const [isCreateConcertOpen, setIsCreateConcertOpen] = useState(false);
  const [isCreateFestivalOpen, setIsCreateFestivalOpen] = useState(false);
  const [isCreateStageOpen, setIsCreateStageOpen] = useState(false);
  const [isCreateArtistOpen, setIsCreateArtistOpen] = useState(false);
  const [isPublishOpen, setIsPublishOpen] = useState(false);

  // Reschedule & Incident target concert
  const [rescheduleConcert, setRescheduleConcert] = useState<Concert | null>(null);
  const [incidentConcert, setIncidentConcert] = useState<Concert | null>(null);
  const [isDeclareIncidentOpen, setIsDeclareIncidentOpen] = useState(false);

  const handleOpenReschedule = (concert: Concert) => {
    setRescheduleConcert(concert);
  };

  const handleOpenDeclareIncident = (concert?: Concert) => {
    setIncidentConcert(concert || null);
    setIsDeclareIncidentOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-hell-darkest text-hell-steel-bright selection:bg-hell-red selection:text-white bg-noise">
      {/* Background ambient lighting */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[400px] bg-gradient-to-b from-hell-red/10 via-transparent to-transparent pointer-events-none blur-3xl z-0" />
      <div className="fixed bottom-0 right-0 w-[500px] h-[350px] bg-gradient-to-t from-hell-green/5 via-transparent to-transparent pointer-events-none blur-3xl z-0" />

      {/* Main Header & Nav */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenCreateConcert={() => setIsCreateConcertOpen(true)}
        onOpenCreateFestival={() => setIsCreateFestivalOpen(true)}
        onOpenPublish={() => setIsPublishOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 relative z-10">
        {activeTab === 'timetable' && (
          <div className="space-y-6">
            <StatsOverview />
            <Timetable
              onOpenCreateConcert={() => setIsCreateConcertOpen(true)}
              onReschedule={handleOpenReschedule}
              onDeclareIncident={handleOpenDeclareIncident}
            />
          </div>
        )}

        {activeTab === 'artists' && (
          <ArtistsPanel
            onOpenCreateArtist={() => setIsCreateArtistOpen(true)}
            onOpenCreateConcert={() => setIsCreateConcertOpen(true)}
          />
        )}

        {activeTab === 'stages' && (
          <StagesPanel
            onOpenCreateStage={() => setIsCreateStageOpen(true)}
            onOpenCreateConcert={() => setIsCreateConcertOpen(true)}
          />
        )}

        {activeTab === 'incidents' && (
          <IncidentsPanel
            onOpenDeclareIncident={() => handleOpenDeclareIncident()}
          />
        )}

        {activeTab === 'architecture' && <ArchitectureInfoPanel />}
      </main>

      {/* Footer */}
      <footer className="border-t border-hell-border/60 bg-hell-card/80 backdrop-blur-sm py-6 mt-12 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-hell-steel">
          <div className="flex items-center gap-2">
            <Flame className="w-4 h-4 text-hell-red" />
            <span className="font-gothic font-bold text-white tracking-wider">FESTIPLAN</span>
            <span>—</span>
            <span>Régie Hellforge & Festival Management</span>
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <span className="flex items-center gap-1.5 text-hell-steel-light">
              <Shield className="w-3.5 h-3.5 text-hell-green-acid" />
              Hexagonal Architecture (Ports & Adapters)
            </span>
            <span>•</span>
            <span className="flex items-center gap-1.5 text-hell-steel-light">
              <GitFork className="w-3.5 h-3.5 text-amber-500" />
              Tactical DDD Domain Invariants (R1 à R7)
            </span>
          </div>
        </div>
      </footer>

      {/* Modals */}
      <CreateConcertModal
        isOpen={isCreateConcertOpen}
        onClose={() => setIsCreateConcertOpen(false)}
      />

      <RescheduleModal
        concert={rescheduleConcert}
        isOpen={Boolean(rescheduleConcert)}
        onClose={() => setRescheduleConcert(null)}
      />

      <DeclareIncidentModal
        initialConcert={incidentConcert}
        isOpen={isDeclareIncidentOpen}
        onClose={() => {
          setIsDeclareIncidentOpen(false);
          setIncidentConcert(null);
        }}
      />

      <CreateFestivalModal
        isOpen={isCreateFestivalOpen}
        onClose={() => setIsCreateFestivalOpen(false)}
      />

      <CreateStageModal
        isOpen={isCreateStageOpen}
        onClose={() => setIsCreateStageOpen(false)}
      />

      <CreateArtistModal
        isOpen={isCreateArtistOpen}
        onClose={() => setIsCreateArtistOpen(false)}
      />

      <PublishModal
        isOpen={isPublishOpen}
        onClose={() => setIsPublishOpen(false)}
      />

      {/* Toast Notifications */}
      <ToastContainer />
    </div>
  );
};

export default function App() {
  return (
    <FestivalProvider>
      <FestiPlanApp />
    </FestivalProvider>
  );
}

