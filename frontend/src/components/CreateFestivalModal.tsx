import React, { useState } from 'react';
import { useFestival } from '../context/FestivalContext';
import { api, ApiError } from '../api/client';
import { X, Calendar, MapPin, Sparkles, PlusCircle, AlertTriangle } from 'lucide-react';

interface CreateFestivalModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CreateFestivalModal: React.FC<CreateFestivalModalProps> = ({ isOpen, onClose }) => {
  const { refreshData, setCurrentFestivalId, addToast } = useFestival();

  const [name, setName] = useState<string>('');
  const [location, setLocation] = useState<string>('');
  const [startDate, setStartDate] = useState<string>('2027-06-18T10:00');
  const [endDate, setEndDate] = useState<string>('2027-06-20T23:59');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    const start = new Date(startDate);
    const end = new Date(endDate);

    if (end <= start) {
      setErrorMessage('La date de fin doit être postérieure à la date de début.');
      return;
    }

    setIsSubmitting(true);
    try {
      const created = await api.createFestival({
        name: name.trim(),
        location: location.trim(),
        start_date: start.toISOString(),
        end_date: end.toISOString(),
      });

      addToast(`Festival "${created.name}" créé avec succès !`, 'success');
      await refreshData();
      setCurrentFestivalId(created.id);
      onClose();
    } catch (err: any) {
      const msg = err instanceof ApiError ? err.message : 'Erreur lors de la création du festival.';
      setErrorMessage(msg);
      addToast('Erreur création festival', 'error', msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-hell-card border border-hell-border max-w-lg w-full rounded-2xl shadow-2xl overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-4 bg-hell-surface border-b border-hell-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-hell-red/20 text-hell-red border border-hell-red/40">
              <PlusCircle className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-gothic font-bold text-lg text-white">Créer une Édition de Festival</h3>
              <p className="text-xs text-hell-steel">Nouvel événement musical</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-hell-steel hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {errorMessage && (
            <div className="p-3 rounded-lg bg-red-950/80 border border-red-800 text-xs text-red-200 flex items-start gap-2">
              <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-red-300">Erreur :</p>
                <p className="mt-0.5">{errorMessage}</p>
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5">
              Nom du Festival *
            </label>
            <input
              type="text"
              required
              placeholder="Ex: Hellforge Open Air 2027"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-hell-red"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5 flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5" /> Lieu / Site du Festival *
            </label>
            <input
              type="text"
              required
              placeholder="Ex: Clisson, Val de Moine"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-hell-red"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5 flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" /> Date d'Ouverture *
              </label>
              <input
                type="datetime-local"
                required
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-hell-red"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5 flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" /> Date de Clôture *
              </label>
              <input
                type="datetime-local"
                required
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-hell-red"
              />
            </div>
          </div>

          {/* Footer */}
          <div className="pt-4 border-t border-hell-border flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 rounded-lg bg-hell-surface border border-hell-border text-xs font-semibold text-hell-steel hover:text-white transition-all"
            >
              Annuler
            </button>

            <button
              type="submit"
              disabled={isSubmitting}
              className="flex items-center gap-2 px-5 py-2 rounded-lg bg-hell-red text-white text-xs font-bold uppercase tracking-wider shadow-flame hover:brightness-110 disabled:opacity-50 transition-all cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Sparkles className="w-4 h-4 animate-spin" /> Création...
                </>
              ) : (
                'Créer le Festival'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

