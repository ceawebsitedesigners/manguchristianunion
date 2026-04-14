<script lang="ts">
    import { onMount } from "svelte";
    import { browser } from "$app/environment";
    import { eventsStore, getEventsFromLocal, saveEventsToLocal, type Event } from "$lib/stores";
    import { URLS } from "$lib/urls";

    // ── State ──────────────────────────────────────
    let events: Event[] = [];
    let loading: boolean = true;

    // Subscribe to store
    eventsStore.subscribe(value => {
        events = value;
        if (events.length > 0) {
            loading = false;
        }
    });

    if (browser) {
        const cached = getEventsFromLocal();
        if (cached && cached.length > 0) {
            eventsStore.init(cached);
        }
    }

    // ── Helpers ────────────────────────────────────

    /**
     * "2026-02-10" → "Mon, 10 Feb 2026"
     * Parses at noon UTC so the day never flips due to local offset.
     */
    function formatDate(iso: string): string {
        const date = new Date(iso + "T12:00:00Z");
        return date.toLocaleDateString("en-GB", {
            weekday: "short",
            day:     "numeric",
            month:   "short",
            year:    "numeric"
        });
    }

    // ── Lifecycle ──────────────────────────────────
    onMount(async () => {
        // Try to load from store first (populated from top level or previous navigation)
        if (events.length > 0) {
            loading = false;
            return;
        }

        try {
            const res = await fetch(URLS.events);
            if (res.ok) {
                const data = await res.json();
                
                const today = new Date();
                today.setHours(0, 0, 0, 0);

                const upcoming = data
                    .filter((event: Event) => new Date(event.eventdate + "T00:00:00") >= today)
                    .sort((a: Event, b: Event) => a.eventdate.localeCompare(b.eventdate));
                
                eventsStore.init(upcoming);
                saveEventsToLocal(upcoming);
            } else {
                console.error("Failed to fetch events");
            }
        } catch (err) {
            console.error("Error fetching events:", err);
        } finally {
            loading = false;
        }
    });
</script>

<!-- ────────────────────────────────────────────── -->
<section id="events-section">

    <div id="heading">
        <h1>Upcoming Events</h1>
        <p>See what's happening in our church community</p>
    </div>

    <div id="events">
        {#if loading}
            <div class="spinner-wrap">
                <div class="spinner"></div>
            </div>

        {:else if events.length === 0}
            <div class="empty-block">
                <span class="empty-icon">📅</span>
                <p class="empty">No upcoming events at the moment. Check back soon!</p>
            </div>

        {:else}
            <div class="event-grid">
                {#each events as event}
                    <div class="card">
                        <div class="card-date">
                            <span class="card-icon">📅</span>
                            <span>{formatDate(event.eventdate)}</span>
                        </div>
                        <h3>{event.eventname}</h3>
                        <p class="card-location">
                            <span class="location-icon">📍</span>
                            {event.eventlocation}
                        </p>
                    </div>
                {/each}
            </div>
        {/if}
    </div>

</section>

<style>
    /* ── Section wrapper ── */
    #events-section {
        width: 100%;
        padding: 7vh 5vw;
        background-color: #ffffff;
    }

    /* ── Heading ── */
    #heading {
        text-align: center;
        max-width: 540px;
        margin: 0 auto 4vh;
    }

    #heading h1 {
        color: #d4a017;
        font-size: clamp(2rem, 4.5vw, 3.2rem);
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.7rem;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    #heading p {
        font-size: clamp(0.95rem, 1.7vw, 1.05rem);
        color: #3a3838;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Events container ── */
    #events {
        max-width: 1100px;
        margin: 0 auto;
        min-height: 150px;
    }

    /* ── Card grid ── */
    .event-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.4rem;
    }

    /* ── Individual card ── */
    .card {
        background-color: #faf6ee;
        border: 1px solid #ede8dc;
        border-radius: 14px;
        padding: 1.6rem 1.4rem;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        transition: box-shadow 0.25s ease, transform 0.25s ease;
    }

    .card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.09);
        transform: translateY(-4px);
    }

    /* ── Date row ── */
    .card-date {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: clamp(0.78rem, 1.1vw, 0.85rem);
        color: #888;
        font-weight: 500;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Event title ── */
    .card h3 {
        font-size: clamp(1.05rem, 1.7vw, 1.25rem);
        color: #d4a017;
        font-weight: 600;
        margin: 0;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Location line ── */
    .card-location {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        font-size: clamp(0.85rem, 1.3vw, 0.95rem);
        color: #4a4848;
        margin: 0;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    .location-icon {
        flex-shrink: 0;
    }

    /* ── Loading spinner ── */
    .spinner-wrap {
        display: flex;
        justify-content: center;
        padding: 4vh 0;
    }

    .spinner {
        width: 44px;
        height: 44px;
        border: 4px solid #ede8dc;
        border-top: 4px solid #d4a017;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* ── Empty state ── */
    .empty-block {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.7rem;
        padding: 4vh 0;
    }

    .empty-icon {
        font-size: 2.2rem;
    }

    .empty {
        font-size: clamp(0.9rem, 1.5vw, 1rem);
        color: #888;
        text-align: center;
        max-width: 400px;
        margin: 0;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Responsive ── */
    @media (max-width: 900px) {
        .event-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 520px) {
        .event-grid {
            grid-template-columns: 1fr;
        }

        #events-section {
            padding: 6vh 6vw;
        }
    }
</style>
