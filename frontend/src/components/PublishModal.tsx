import React, { useState } from 'react';
import { useFestival } from '../context/FestivalContext';
import { X, Unlock, Lock, AlertTriangle, ShieldCheck, Sparkles } from 'lucide-react';

interface PublishModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const PublishModal: React.FC<PublishModalProps> = ({ isOpen, onClose }) => {
  const { currentFestival, publishFestival, concerts, stages } = useFestival();
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  if (!isOpen || !currentFestival) return null;

  const handleConfirm = async () => {
    setIsSubmitting(true);
    const success = await publishFestival();
    setIsSubmitting(false);
    if (success) {
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm animate-in fade-in">
      <div className="bg-hell-card border border-emerald-900/60 max-w-lg w-full rounded-2xl shadow-acid overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-4 bg-hell-surface border-b border-hell-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
              <Unlock className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-gothic font-bold text-lg text-white">Publier le Running Order</h3>
              <p className="text-xs text-hell-steel">Passage à l'état officiel & vérification des invariants</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-hell-steel hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          <div className="p-4 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-xs text-emerald-200">
            <div className="flex items-center gap-2 font-bold text-sm text-emerald-400 mb-1">
              <ShieldCheck className="w-4 h-4 shrink-0" />
              <span>Verrouillage Officiel du Festival (Règle R7)</span>
            </div>
            <p className="mt-1 leading-relaxed text-hell-steel-light">
              Vous vous apprêtez à publier la programmation officielle de{' '}
              <strong className="text-white">{currentFestival.name}</strong> ({concerts.length} concerts sur {stages.length} scènes).
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-amber-950/40 border border-amber-800/50 text-xs text-amber-200 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <p className="font-bold text-amber-300">Conséquences Métier (Tactical DDD) :</p>
              <ul className="list-disc pl-4 mt-1.5 space-y-1 text-amber-200/90 text-[11px]">
                <li>Le statut du festival passera de <code className="text-white bg-black/40 px-1 py-0.5 rounded">preparation</code> à <code className="text-emerald-400 bg-black/40 px-1 py-0.5 rounded">published</code>.</li>
                <li>Tout déplacement ou modification de concert sera <strong>strictement refusé</strong> par le domaine métier.</li>
                <li>Seules les annulations formelles et la déclaration d'incidents techniques resteront permises en régie.</li>
              </ul>
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-hell-border">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 rounded-lg bg-hell-surface border border-hell-border text-xs font-semibold text-hell-steel hover:text-white transition-all"
            >
              Annuler
            </button>

            <button
              type="button"
              onClick={handleConfirm}
              disabled={isSubmitting}
              className="flex items-center gap-2 px-5 py-2 rounded-lg bg-gradient-to-r from-emerald-600 to-hell-green text-white text-xs font-bold uppercase tracking-wider shadow-acid hover:brightness-110 disabled:opacity-50 transition-all cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Sparkles className="w-4 h-4 animate-spin" /> Publication...
                </>
              ) : (
                <>
                  <Lock className="w-4 h-4" /> Confirmer & Publier
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

