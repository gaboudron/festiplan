import React, { useState } from 'react';
import { useFestival } from '../context/FestivalContext';
import { api, ApiError } from '../api/client';
import { X, Sparkles, Check, AlertTriangle, Users } from 'lucide-react';
import { EQUIPMENT_LABELS } from '../utils/formatters';

interface CreateArtistModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const COMMON_GENRES = [
  'Heavy metal',
  'Thrash metal',
  'Death metal',
  'Black metal',
  'Power metal',
  'Hardcore',
  'Metalcore',
  'Stoner',
  'Sludge',
  'Doom metal',
  'Punk rock',
  'Industrial metal',
];

const COMMON_EQUIPMENTS = [
  'large_rigging',
  'special_lighting',
  'pyrotechnics',
  'sound_system_extreme',
  'hydraulic_risers',
  'co2_cannons',
];

export const CreateArtistModal: React.FC<CreateArtistModalProps> = ({ isOpen, onClose }) => {
  const { refreshData, addToast } = useFestival();

  const [name, setName] = useState<string>('');
  const [genre, setGenre] = useState<string>('Heavy metal');
  const [selectedEquipments, setSelectedEquipments] = useState<string[]>([
    'special_lighting',
  ]);
  const [customEquip, setCustomEquip] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  const toggleEquipment = (eq: string) => {
    setSelectedEquipments((prev) =>
      prev.includes(eq) ? prev.filter((item) => item !== eq) : [...prev, eq]
    );
  };

  const handleAddCustom = (e: React.KeyboardEvent | React.MouseEvent) => {
    e.preventDefault();
    const clean = customEquip.trim().toLowerCase().replace(/\s+/g, '_');
    if (clean && !selectedEquipments.includes(clean)) {
      setSelectedEquipments((prev) => [...prev, clean]);
      setCustomEquip('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!name.trim()) {
      setErrorMessage("Le nom de l'artiste est requis.");
      return;
    }

    if (!genre.trim()) {
      setErrorMessage('Le genre musical est requis.');
      return;
    }

    setIsSubmitting(true);
    try {
      const created = await api.createArtist({
        name: name.trim(),
        genre: genre.trim(),
        required_equipment: selectedEquipments,
      });

      addToast(`Groupe "${created.name}" ajouté au Lineup !`, 'success');
      await refreshData();
      onClose();
    } catch (err: any) {
      const msg = err instanceof ApiError ? err.message : "Erreur lors de l'ajout de l'artiste.";
      setErrorMessage(msg);
      addToast('Erreur ajout artiste', 'error', msg);
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
              <Users className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-gothic font-bold text-lg text-white">Ajouter un Artiste au Lineup</h3>
              <p className="text-xs text-hell-steel">Fiche groupe & contraintes techniques</p>
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
              Nom du Groupe / Artiste *
            </label>
            <input
              type="text"
              required
              placeholder="Ex: Behemoth, Gojira, Judas Priest"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-hell-red"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5">
              Genre Musical *
            </label>
            <div className="flex flex-wrap gap-1.5 mb-2">
              {COMMON_GENRES.map((g) => (
                <button
                  key={g}
                  type="button"
                  onClick={() => setGenre(g)}
                  className={`px-2 py-0.5 rounded text-[11px] font-medium transition-all ${
                    genre === g
                      ? 'bg-hell-red text-white shadow-flame'
                      : 'bg-hell-surface text-hell-steel hover:text-white border border-hell-border'
                  }`}
                >
                  {g}
                </button>
              ))}
            </div>
            <input
              type="text"
              required
              placeholder="Ou saisir un sous-genre spécifique..."
              value={genre}
              onChange={(e) => setGenre(e.target.value)}
              className="w-full bg-hell-surface border border-hell-border rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-hell-red"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-hell-steel mb-1.5">
              Exigences Techniques (Rider / Équipements Requis)
            </label>
            <div className="flex flex-wrap gap-2 mb-2">
              {COMMON_EQUIPMENTS.map((eq) => {
                const isSelected = selectedEquipments.includes(eq);
                return (
                  <button
                    key={eq}
                    type="button"
                    onClick={() => toggleEquipment(eq)}
                    className={`px-2.5 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all ${
                      isSelected
                        ? 'bg-hell-red/20 text-red-300 border border-hell-red/60 shadow-sm'
                        : 'bg-hell-surface text-hell-steel hover:text-white border border-hell-border'
                    }`}
                  >
                    {isSelected && <Check className="w-3 h-3 text-hell-red" />}
                    <span>{EQUIPMENT_LABELS[eq] || eq}</span>
                  </button>
                );
              })}
            </div>

            {/* Custom equipment add */}
            <div className="flex gap-2 mt-2">
              <input
                type="text"
                placeholder="Autre besoin technique..."
                value={customEquip}
                onChange={(e) => setCustomEquip(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddCustom(e)}
                className="flex-1 bg-hell-surface border border-hell-border rounded-lg px-3 py-1.5 text-xs text-white placeholder-hell-steel focus:outline-none focus:border-hell-red"
              />
              <button
                type="button"
                onClick={handleAddCustom}
                className="px-3 py-1.5 rounded-lg bg-hell-surface border border-hell-border text-xs text-hell-steel hover:text-white hover:border-hell-steel"
              >
                Ajouter
              </button>
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
              className="flex items-center gap-2 px-5 py-2 rounded-lg bg-hell-red hover:bg-red-500 text-white text-xs font-bold uppercase tracking-wider shadow-flame hover:brightness-110 disabled:opacity-50 transition-all cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Sparkles className="w-4 h-4 animate-spin" /> Enregistrement...
                </>
              ) : (
                'Ajouter au Lineup'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

