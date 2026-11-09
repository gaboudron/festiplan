import React from 'react';
import { ShieldCheck, Layers } from 'lucide-react';

export const ArchitectureInfoPanel: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-hell-green-dark/40 border border-hell-green/50 text-hell-green-acid">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h2 className="font-gothic font-bold text-xl text-white">
              Architecture Hexagonale & Tactical DDD
            </h2>
            <p className="text-xs text-hell-steel mt-0.5">
              Guide des 7 invariants métier et de l'isolation Ports & Adapters dans FestiPlan
            </p>
          </div>
        </div>
      </div>

      {/* Hexagonal Architecture Layers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Domain Layer */}
        <div className="bg-hell-card border border-hell-border rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2.5 h-2.5 rounded-full bg-hell-red" />
              <h3 className="font-gothic font-bold text-sm text-white">1. Cœur Domaine Métier</h3>
            </div>
            <p className="text-xs text-hell-steel leading-relaxed">
              Zéro dépendance vers FastAPI, SQLAlchemy ou Pydantic. Contient les entités pures (<code className="text-white">Festival</code>, <code className="text-white">Concert</code>, <code className="text-white">Stage</code>, <code className="text-white">Artist</code>, <code className="text-white">Incident</code>), les Value Objects (<code className="text-white">TimeRange</code>) et Domain Events.
            </p>
          </div>
          <span className="mt-3 text-[10px] text-hell-red font-mono font-bold bg-hell-surface px-2 py-1 rounded border border-hell-border block">
            app/domain/
          </span>
        </div>

        {/* Ports Layer */}
        <div className="bg-hell-card border border-hell-border rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-400" />
              <h3 className="font-gothic font-bold text-sm text-white">2. Ports (Contrats d'Entrée / Sortie)</h3>
            </div>
            <p className="text-xs text-hell-steel leading-relaxed">
              Définit les interfaces abstraites (<code className="text-white">Protocol</code>). Ports Inbound (<code className="text-white">ports/inbound/</code>) pour les cas d'usage et Ports Outbound (<code className="text-white">ports/outbound/</code>) pour la persistance et les notifications.
            </p>
          </div>
          <span className="mt-3 text-[10px] text-amber-400 font-mono font-bold bg-hell-surface px-2 py-1 rounded border border-hell-border block">
            app/ports/
          </span>
        </div>

        {/* Adapters Layer */}
        <div className="bg-hell-card border border-hell-border rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2.5 h-2.5 rounded-full bg-hell-green-acid" />
              <h3 className="font-gothic font-bold text-sm text-white">3. Adaptateurs Techniques</h3>
            </div>
            <p className="text-xs text-hell-steel leading-relaxed">
              Inbound : FastAPI, routeurs HTTP, DTOs Pydantic et gestionnaire d'exceptions unifié. Outbound : Mappers, repositories SQLAlchemy SQLite et bus d'événements.
            </p>
          </div>
          <span className="mt-3 text-[10px] text-hell-green-acid font-mono font-bold bg-hell-surface px-2 py-1 rounded border border-hell-border block">
            app/adapters/
          </span>
        </div>
      </div>

      {/* The 7 Domain Invariants */}
      <div className="bg-hell-card border border-hell-border rounded-xl p-5">
        <h3 className="font-gothic font-bold text-lg text-white mb-4 flex items-center gap-2">
          <Layers className="w-5 h-5 text-hell-red" />
          Les 7 Invariants Métier Garantis par le Domaine
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          {/* R1 */}
          <div className="p-3 rounded-lg bg-hell-surface border border-hell-border">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">Règle R1 : Invariant de Créneau Temporel</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-black/40 text-hell-red">InvalidTimeRangeError</span>
            </div>
            <p className="text-hell-steel leading-relaxed">
              La date de fin d'un concert ou d'un festival doit être strictement postérieure à la date de début. Encapsulé dans le Value Object immuable <code className="text-white">TimeRange</code>.
            </p>
          </div>

          {/* R2 */}
          <div className="p-3 rounded-lg bg-hell-surface border border-hell-border">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">Règle R2 : Conflit d'Occupation Scène</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-black/40 text-hell-red">StageOccupiedError (409)</span>
            </div>
            <p className="text-hell-steel leading-relaxed">
              Une scène ne peut jamais accueillir deux concerts simultanément sur des créneaux qui se chevauchent.
            </p>
          </div>

          {/* R3 */}
          <div className="p-3 rounded-lg bg-hell-surface border border-hell-border">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">Règle R3 : Conflit de Disponibilité Artiste</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-black/40 text-hell-red">ArtistAlreadyScheduledError (409)</span>
            </div>
            <p className="text-hell-steel leading-relaxed">
              Un artiste ne peut pas être programmé sur deux scènes en même temps sur des créneaux superposés.
            </p>
          </div>

          {/* R4 */}
          <div className="p-3 rounded-lg bg-hell-surface border border-hell-border">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">Règle R4 : Bornes du Festival</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-black/40 text-hell-red">ConcertOutsideFestivalDatesError</span>
            </div>
            <p className="text-hell-steel leading-relaxed">
              Tout concert doit se dérouler strictement entre la date de début et la date de fin du festival associé.
            </p>
          </div>

          {/* R5 */}
          <div className="p-3 rounded-lg bg-hell-surface border border-hell-border">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">Règle R5 : Appartenance de Scène</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-black/40 text-hell-red">StageDoesNotBelongToFestivalError</span>
            </div>
            <p className="text-hell-steel leading-relaxed">
              Un concert ne peut être programmé que sur une scène rattachée au festival concerné.
            </p>
          </div>

          {/* R6 */}
          <div className="p-3 rounded-lg bg-hell-surface border border-hell-border">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">Règle R6 : Adéquation Technique Scène / Artiste</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-black/40 text-hell-red">EquipmentMismatchError</span>
            </div>
            <p className="text-hell-steel leading-relaxed">
              La scène doit obligatoirement posséder l'ensemble des équipements techniques spécifiés dans le rider de l'artiste.
            </p>
          </div>

          {/* R7 */}
          <div className="p-3 rounded-lg bg-hell-surface border border-hell-border md:col-span-2">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-emerald-400">Règle R7 : Verrouillage du Festival Publié</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-black/40 text-emerald-400">FestivalAlreadyPublishedError (403)</span>
            </div>
            <p className="text-hell-steel leading-relaxed">
              Dès lors que le festival est publié (<code className="text-white">published</code>), aucun concert ne peut être déplacé ou modifié arbitrairement. Seules l'annulation formelle et la gestion d'incidents techniques sont autorisées.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
