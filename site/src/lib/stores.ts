import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// --- Types ---
export interface Event {
    eventname: string;
    eventdate: string;
    eventlocation: string;
}

export interface Leader {
    [key: string]: string | string[];
}

export interface YearData {
    theme: string;
    leaders: Leader;
}

// --- Events Store ---
function createEventsStore() {
    const { subscribe, set } = writable<Event[]>([]);

    return {
        subscribe,
        set,
        init: (data: Event[]) => set(data),
        clear: () => set([])
    };
}

export const eventsStore = createEventsStore();

// --- Leadership Store ---
function createLeadershipStore() {
    const { subscribe, update } = writable<Record<string, YearData>>({});

    return {
        subscribe,
        addYear: (year: string, data: YearData) => update(cache => ({ ...cache, [year]: data })),
        clear: () => update(() => ({}))
    };
}

export const leadershipStore = createLeadershipStore();

export function clearEventsCache() {
    eventsStore.clear();
    if (browser) {
        localStorage.removeItem(EVENTS_CACHE_KEY);
    }
}

export function clearLeadershipCache() {
    leadershipStore.clear();
    if (browser) {
        localStorage.removeItem(LEADERSHIP_CACHE_KEY);
    }
}

// --- LocalStorage Helpers (Optional but good for "reload") ---
const EVENTS_CACHE_KEY = 'mangu_cu_events_cache';
const LEADERSHIP_CACHE_KEY = 'mangu_cu_leadership_cache';

export function saveEventsToLocal(events: Event[]) {
    if (browser) {
        localStorage.setItem(EVENTS_CACHE_KEY, JSON.stringify({
            data: events,
            timestamp: Date.now()
        }));
    }
}

export function getEventsFromLocal(): Event[] | null {
    if (!browser) return null;
    const cached = localStorage.getItem(EVENTS_CACHE_KEY);
    if (!cached) return null;
    
    try {
        const { data, timestamp } = JSON.parse(cached);
        // Cache for 1 hour
        if (Date.now() - timestamp < 3600000) {
            return data;
        }
    } catch (e) {
        return null;
    }
    return null;
}

export function saveLeadershipToLocal(cache: Record<string, YearData>) {
    if (browser) {
        localStorage.setItem(LEADERSHIP_CACHE_KEY, JSON.stringify({
            data: cache,
            timestamp: Date.now()
        }));
    }
}

export function getLeadershipFromLocal(): Record<string, YearData> | null {
    if (!browser) return null;
    const cached = localStorage.getItem(LEADERSHIP_CACHE_KEY);
    if (!cached) return null;
    
    try {
        const { data, timestamp } = JSON.parse(cached);
        // Cache for 1 day
        if (Date.now() - timestamp < 86400000) {
            return data;
        }
    } catch (e) {
        return null;
    }
    return null;
}
