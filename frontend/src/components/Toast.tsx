import React from 'react';
import { useFestival } from '../context/FestivalContext';
import { AlertTriangle, CheckCircle2, Flame, Info, X } from 'lucide-react';

export const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useFestival();

  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-5 right-5 z-50 flex flex-col gap-3 max-w-md w-full px-4 pointer-events-none">
      {toasts.map((toast) => {
        let borderClass = 'border-hell-border';
        let bgClass = 'bg-hell-card/95';
        let icon = <Info className="w-5 h-5 text-hell-steel-light shrink-0" />;

        if (toast.type === 'error') {
          borderClass = 'border-red-600 shadow-flame';
          bgClass = 'bg-[#180a0a]/95';
          icon = <Flame className="w-5 h-5 text-red-500 shrink-0 animate-pulse" />;
        } else if (toast.type === 'success') {
          borderClass = 'border-emerald-500 shadow-acid';
          bgClass = 'bg-[#061a12]/95';
          icon = <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />;
        } else if (toast.type === 'warning') {
          borderClass = 'border-amber-600';
          bgClass = 'bg-[#1c1407]/95';
          icon = <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0" />;
        }

        return (
          <div
            key={toast.id}
            className={`pointer-events-auto flex items-start gap-3 p-4 rounded-lg border backdrop-blur-md shadow-2xl transition-all duration-300 animate-in fade-in slide-in-from-bottom-3 ${borderClass} ${bgClass}`}
          >
            {icon}
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold tracking-wide text-hell-steel-bright">
                {toast.message}
              </p>
              {toast.detail && (
                <p className="text-xs text-hell-steel mt-1 leading-relaxed break-words">
                  {toast.detail}
                </p>
              )}
            </div>
            <button
              onClick={() => removeToast(toast.id)}
              className="text-hell-steel hover:text-white transition-colors p-1"
              aria-label="Fermer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        );
      })}
    </div>
  );
};

