export const EQUIPMENT_LABELS: Record<string, string> = {
  large_rigging: 'Charpente Lourde (Rigging)',
  special_lighting: 'Éclairage & Lasers FX',
  pyrotechnics: 'Pyrotechnie / Lance-Flammes',
  sound_system_extreme: 'Mur de Son Haute Puissance',
  hydraulic_risers: 'Plateformes Hydrauliques',
  co2_cannons: 'Canons CO2 Cryo',
};

export function formatEquipment(eq: string): string {
  return EQUIPMENT_LABELS[eq] || eq;
}

export function formatDateFull(isoString: string): string {
  try {
    const d = new Date(isoString);
    return new Intl.DateTimeFormat('fr-FR', {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    }).format(d);
  } catch {
    return isoString;
  }
}

export function formatTime(isoString: string): string {
  try {
    const d = new Date(isoString);
    return new Intl.DateTimeFormat('fr-FR', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }).format(d);
  } catch {
    return isoString;
  }
}

export function formatTimeSlot(startIso: string, endIso: string): string {
  return `${formatTime(startIso)} - ${formatTime(endIso)}`;
}

export function getDayKey(isoString: string): string {
  try {
    const d = new Date(isoString);
    return d.toISOString().split('T')[0];
  } catch {
    return 'inconnu';
  }
}

export function checkEquipmentMatch(
  required: string[] = [],
  available: string[] = []
): { ok: boolean; missing: string[] } {
  const missing = required.filter((req) => !available.includes(req));
  return {
    ok: missing.length === 0,
    missing,
  };
}

export function toLocalDatetimeInput(isoString?: string): string {
  if (!isoString) return '';
  try {
    const d = new Date(isoString);
    // Format as YYYY-MM-DDThh:mm for HTML datetime-local input
    const pad = (n: number) => String(n).padStart(2, '0');
    const year = d.getFullYear();
    const month = pad(d.getMonth() + 1);
    const day = pad(d.getDate());
    const hours = pad(d.getHours());
    const minutes = pad(d.getMinutes());
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  } catch {
    return '';
  }
}

export function fromLocalDatetimeInputToISO(localStr: string): string {
  if (!localStr) return '';
  const d = new Date(localStr);
  return d.toISOString();
}

